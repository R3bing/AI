"""Continuous Online Learning & Baseline Neural Network Engine for QKW.
Implements:
1. Clean, deconstructed Feedforward Neural Network (PyTorch) with line-by-line comments.
2. Dynamic continuous online learning using Scikit-Learn (SGDClassifier.partial_fit)
   and PyTorch to auto-train on every incoming chat interaction from the past turn without asking.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
import structlog

logger = structlog.get_logger(__name__)


# =====================================================================
# 1. BASELINE FEEDFORWARD NEURAL NETWORK (PyTorch)
# =====================================================================

class BaselineFeedforwardNN(nn.Module):
    """Phase 2: Model Architecture.
    A basic Feedforward Neural Network with one hidden layer and ReLU activation.
    
    Architecture:
      Input Tensor (batch_size, input_dim)
           ↓
      Linear Layer 1: W1 * x + b1  -> (batch_size, hidden_dim)
           ↓
      Activation: ReLU(z1) = max(0, z1)
           ↓
      Linear Layer 2: W2 * a1 + b2 -> (batch_size, output_dim)
    """

    def __init__(self, input_dim: int = 16, hidden_dim: int = 32, output_dim: int = 2):
        super(BaselineFeedforwardNN, self).__init__()
        # Linear layer mapping input dimension to hidden dimension
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        # Non-linear activation function
        self.relu = nn.ReLU()
        # Output layer mapping hidden dimension to class logits
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Executes the forward pass through the network."""
        # 1. Transform input through the first linear layer
        out = self.fc1(x)
        # 2. Apply non-linear activation (ReLU)
        out = self.relu(out)
        # 3. Project to final output logits
        out = self.fc2(out)
        return out


def train_baseline_neural_network(
    input_dim: int = 16,
    hidden_dim: int = 32,
    epochs: int = 5,
    learning_rate: float = 0.01,
) -> Dict[str, Any]:
    """Demonstrates and tests the 4 core phases of neural network training:
    Phase 1: Data Preparation
    Phase 2: Model Architecture
    Phase 3: Loss Function & Optimizer
    Phase 4: The Training Loop (forward pass, loss calculation, backprop, weight update)
    """
    # -----------------------------------------------------------------
    # Phase 1: Data Preparation (Generating dummy input tensors for binary classification)
    # -----------------------------------------------------------------
    num_samples = 100
    # Create random synthetic features tensor: shape (100, input_dim)
    X = torch.randn(num_samples, input_dim, dtype=torch.float32)
    # Create binary class targets: shape (100,), values in {0, 1}
    y = (X[:, 0] + X[:, 1] > 0).long()

    # -----------------------------------------------------------------
    # Phase 2: Model Architecture Instantiation
    # -----------------------------------------------------------------
    model = BaselineFeedforwardNN(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=2)

    # -----------------------------------------------------------------
    # Phase 3: Loss Function & Optimizer
    # -----------------------------------------------------------------
    # Cross-Entropy loss calculates error between predicted logits and true class labels
    criterion = nn.CrossEntropyLoss()
    # Adam optimizer dynamically adjusts learning rates for each parameter
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # -----------------------------------------------------------------
    # Phase 4: The Training Loop
    # -----------------------------------------------------------------
    loss_history = []
    model.train()  # Put network into training mode

    for epoch in range(epochs):
        # 1. Forward Pass: compute predicted outputs by passing input tensor to the model
        outputs = model(X)

        # 2. Loss Calculation: measure how far predictions deviate from ground truth
        loss = criterion(outputs, y)

        # 3. Zero Gradients: clear previously accumulated gradients from the optimizer
        optimizer.zero_grad()

        # 4. Backward Pass (Backpropagation): compute dLoss/dWeight for all network parameters
        loss.backward()

        # 5. Optimizer Step: update model weights in the direction that minimizes loss
        optimizer.step()

        loss_history.append(float(loss.item()))

    # Calculate final accuracy on the training batch
    with torch.no_grad():
        preds = torch.argmax(model(X), dim=1)
        accuracy = float((preds == y).sum().item()) / float(num_samples)

    return {
        "model_architecture": f"BaselineFeedforwardNN({input_dim} -> {hidden_dim} -> 2)",
        "epochs_completed": epochs,
        "final_loss": round(loss_history[-1], 4),
        "loss_history": [round(l, 4) for l in loss_history],
        "training_accuracy": round(accuracy, 4),
        "total_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
    }


# =====================================================================
# 2. DYNAMIC CONTINUOUS ONLINE LEARNER (Scikit-Learn + PyTorch)
# =====================================================================

class ContinuousOnlineLearner:
    """Continuously and dynamically trains on every chat turn in the background
    without asking, using Scikit-Learn's incremental partial_fit and PyTorch.
    """

    def __init__(self, feature_dim: int = 16):
        self.feature_dim = feature_dim
        self.storage_dir = "data/training_datasets"
        os.makedirs(self.storage_dir, exist_ok=True)
        self.history_file = os.path.join(self.storage_dir, "online_continuous_history.jsonl")

        # 1. Scikit-Learn Incremental Model (Online SGD Classifier with Log-Loss)
        self.sklearn_model = SGDClassifier(
            loss="log_loss",
            penalty="l2",
            alpha=1e-4,
            learning_rate="optimal",
            random_state=42,
        )
        # Initialize with classes [0, 1] representing [Aql-dominant, Qalb-dominant]
        dummy_X = np.zeros((2, self.feature_dim), dtype=np.float64)
        dummy_y = np.array([0, 1], dtype=np.int32)
        self.sklearn_model.partial_fit(dummy_X, dummy_y, classes=np.array([0, 1], dtype=np.int32))

        # 2. PyTorch Online Neural Network
        self.pytorch_model = BaselineFeedforwardNN(input_dim=self.feature_dim, hidden_dim=32, output_dim=2)
        self.pytorch_optimizer = optim.Adam(self.pytorch_model.parameters(), lr=0.005)
        self.pytorch_criterion = nn.CrossEntropyLoss()

        # Telemetry
        self.total_chats_learned = 0
        self.loss_history: List[float] = []
        self.recent_predictions: List[Dict[str, Any]] = []

    def _extract_feature_vector(self, query: str, entropy: float, sources_count: int) -> np.ndarray:
        """Deterministically projects text query and interaction metrics into continuous feature tensor."""
        vec = np.zeros(self.feature_dim, dtype=np.float64)
        q_bytes = query.encode("utf-8")

        for i in range(self.feature_dim - 2):
            hash_val = int(hashlib.sha256(q_bytes + str(i).encode()).hexdigest(), 16) % 1000
            vec[i] = (hash_val / 500.0) - 1.0  # Normalized between -1.0 and 1.0

        # Inject telemetry features
        vec[-2] = float(np.clip(entropy, 0.0, 1.0))
        vec[-1] = float(np.clip(sources_count / 11.0, 0.0, 1.0))
        return vec

    def learn_from_chat_turn(
        self,
        query: str,
        dominant_mode: str,
        sources_count: int = 3,
        entropy: float = 0.5,
    ) -> Dict[str, Any]:
        """Automatically and silently trains from the latest chat turn without asking."""
        # Label: 0 for Aql/Particle, 1 for Qalb/Wave
        is_qalb = 1 if "qalb" in dominant_mode.lower() or "wave" in dominant_mode.lower() else 0
        target = np.array([is_qalb], dtype=np.int32)

        # 1. Extract feature vector in float64 for sklearn
        features = self._extract_feature_vector(query, entropy=entropy, sources_count=sources_count)
        X_np = features.astype(np.float64).reshape(1, -1)

        # 2. Incremental Scikit-Learn Online Training
        self.sklearn_model.partial_fit(X_np, target)
        sklearn_prob = self.sklearn_model.predict_proba(X_np)[0]

        # 3. Incremental PyTorch Training Step
        self.pytorch_model.train()
        X_tensor = torch.tensor(X_np, dtype=torch.float32)
        y_tensor = torch.tensor(target, dtype=torch.long)

        self.pytorch_optimizer.zero_grad()
        logits = self.pytorch_model(X_tensor)
        loss = self.pytorch_criterion(logits, y_tensor)
        loss.backward()
        self.pytorch_optimizer.step()

        current_loss = round(float(loss.item()), 4)
        self.loss_history.append(current_loss)
        if len(self.loss_history) > 50:
            self.loss_history.pop(0)

        self.total_chats_learned += 1

        # 4. Save to persistent online training history
        record = {
            "turn_index": self.total_chats_learned,
            "timestamp": time.time(),
            "query": query,
            "label_mode": dominant_mode,
            "label_int": is_qalb,
            "loss": current_loss,
            "sklearn_prob_qalb": round(float(sklearn_prob[1]), 4),
        }
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            logger.warning("online_learning_save_failed", error=str(e))

        logger.info(
            "online_continuous_learning_step_completed",
            turn=self.total_chats_learned,
            loss=current_loss,
            dominant=dominant_mode,
        )

        return {
            "status": "auto_trained_successfully",
            "total_chats_learned": self.total_chats_learned,
            "current_loss": current_loss,
            "loss_history": self.loss_history[-10:],
            "predicted_mode": "Qalb (Wave)" if sklearn_prob[1] > 0.5 else "Aql (Particle)",
            "prediction_confidence": round(float(max(sklearn_prob)), 4),
        }

    def get_learning_telemetry(self) -> Dict[str, Any]:
        """Returns statistics on continuous online self-training."""
        return {
            "total_chats_learned": self.total_chats_learned,
            "recent_loss": self.loss_history[-1] if self.loss_history else 0.693,
            "average_loss": round(float(np.mean(self.loss_history)), 4) if self.loss_history else 0.693,
            "model_type": "PyTorch + Scikit-Learn Incremental SGD",
            "history_file": self.history_file,
        }


# Global singleton online learner
continuous_online_learner = ContinuousOnlineLearner()


def get_continuous_learner() -> ContinuousOnlineLearner:
    """Returns the global ContinuousOnlineLearner instance."""
    return continuous_online_learner

