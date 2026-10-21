"""Child Model Training Engine (Step 3 of NAS Cycle).
Executes empirical fitting on target datasets using SGD, AdamW, and standard optimizers.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from backend.nas.models import (
    ArchitectureCandidate,
    TrainingMetrics,
)
from backend.nas.child_network import ConcreteChildNetwork


class DatasetFactory:
    """Provides target training and validation datasets for child model fitting."""

    @staticmethod
    def get_benchmark_dataset(
        num_samples: int = 400,
        input_dim: int = 128,
        num_classes: int = 10,
        seed: int = 42,
    ) -> Tuple[DataLoader, DataLoader]:
        """Generates a reproducible non-linear manifold classification dataset."""
        torch.manual_seed(seed)
        # Create non-linear clusters
        X = torch.randn(num_samples, input_dim)
        # True non-linear projection for class labels
        W_true = torch.randn(input_dim, num_classes)
        logits = torch.matmul(torch.sin(X), W_true) + 0.1 * torch.randn(num_samples, num_classes)
        y = torch.argmax(logits, dim=1)

        split_idx = int(0.75 * num_samples)
        train_ds = TensorDataset(X[:split_idx], y[:split_idx])
        val_ds = TensorDataset(X[split_idx:], y[split_idx:])

        train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)
        return train_loader, val_loader


class ChildModelTrainer:
    """Step 3: Empirical fitting trainer for Child Models."""

    def __init__(self, default_epochs: int = 4):
        self.default_epochs = default_epochs
        self.criterion = nn.CrossEntropyLoss()

    def train(
        self,
        model: ConcreteChildNetwork,
        train_loader: Optional[DataLoader] = None,
        epochs: Optional[int] = None,
    ) -> TrainingMetrics:
        """Trains the instantiated child model on the target dataset."""
        t_start = time.perf_counter()
        num_epochs = epochs or self.default_epochs
        hparams = model.candidate.hyperparameters

        # If train_loader not provided, generate matching dataset
        if train_loader is None:
            in_dim = model.candidate.blocks[0].in_features
            num_classes = model.candidate.blocks[-1].out_features
            train_loader, _ = DatasetFactory.get_benchmark_dataset(
                num_samples=320,
                input_dim=in_dim,
                num_classes=num_classes,
            )

        optimizer = self._build_optimizer(model, hparams.optimizer, hparams.learning_rate, hparams.weight_decay)

        loss_history: List[float] = []
        correct = 0
        total = 0

        model.train()
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            batches = 0
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                logits = model(batch_x)
                loss = self.criterion(logits, batch_y)
                loss.backward()

                # Gradient clipping to ensure numerical stability during NAS
                nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
                optimizer.step()

                epoch_loss += loss.item()
                batches += 1

                preds = torch.argmax(logits, dim=1)
                correct += (preds == batch_y).sum().item()
                total += batch_y.size(0)

            avg_loss = epoch_loss / max(1, batches)
            loss_history.append(float(round(avg_loss, 4)))

        train_accuracy = float(round(correct / max(1, total), 4))
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        return TrainingMetrics(
            epochs_trained=num_epochs,
            final_train_loss=loss_history[-1] if loss_history else 0.0,
            train_accuracy=train_accuracy,
            loss_history=loss_history,
            training_time_ms=elapsed_ms,
        )

    def _build_optimizer(self, model: nn.Module, opt_name: str, lr: float, wd: float) -> torch.optim.Optimizer:
        """Instantiates standard optimization method requested by controller hyperparameters."""
        opt_upper = opt_name.upper()
        if "SGD" in opt_upper:
            return torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=wd)
        elif "LION" in opt_upper or "ADAMW" in opt_upper:
            return torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
        elif "ADAM" in opt_upper:
            return torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
        # Default fallback
        return torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)


child_trainer = ChildModelTrainer()
