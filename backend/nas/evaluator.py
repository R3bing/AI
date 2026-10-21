"""Child Model Evaluation Engine (Step 4 of NAS Cycle).
Benchmarks accuracy, inference latency, parameter count, FLOPs, and multi-objective fitness.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from backend.nas.models import (
    ArchitectureCandidate,
    EvaluationMetrics,
)
from backend.nas.child_network import ConcreteChildNetwork
from backend.nas.trainer import DatasetFactory


class ChildModelEvaluator:
    """Step 4: Benchmarks trained child model on validation dataset for accuracy and efficiency."""

    def __init__(
        self,
        target_latency_ms: float = 15.0,
        target_parameters: int = 1_000_000,
    ):
        self.target_latency_ms = target_latency_ms
        self.target_parameters = target_parameters
        self.criterion = nn.CrossEntropyLoss()

    def evaluate(
        self,
        model: ConcreteChildNetwork,
        val_loader: Optional[DataLoader] = None,
        benchmark_runs: int = 10,
    ) -> EvaluationMetrics:
        """Evaluates trained child model accuracy, inference latency, and multi-objective fitness."""
        in_dim = model.candidate.blocks[0].in_features
        num_classes = model.candidate.blocks[-1].out_features

        if val_loader is None:
            _, val_loader = DatasetFactory.get_benchmark_dataset(
                num_samples=320,
                input_dim=in_dim,
                num_classes=num_classes,
            )

        model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                logits = model(batch_x)
                loss = self.criterion(logits, batch_y)
                total_loss += loss.item()

                preds = torch.argmax(logits, dim=1)
                correct += (preds == batch_y).sum().item()
                total += batch_y.size(0)

        val_accuracy = float(round(correct / max(1, total), 4))
        val_loss = float(round(total_loss / max(1, len(val_loader)), 4))

        # Measure Inference Latency (ms per batch)
        dummy_batch = torch.randn(32, in_dim)
        # Warmup
        with torch.no_grad():
            for _ in range(3):
                _ = model(dummy_batch)

        t_lat_start = time.perf_counter()
        with torch.no_grad():
            for _ in range(benchmark_runs):
                _ = model(dummy_batch)
        avg_latency_ms = float(round(((time.perf_counter() - t_lat_start) / benchmark_runs) * 1000.0, 3))

        # Exact Trainable Parameters
        param_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
        macs_count = param_count * 2

        # Multi-Objective Fitness Score Calculation
        # Balances classification accuracy with latency efficiency and parameter footprint
        latency_factor = min(1.0, (self.target_latency_ms / max(1.0, avg_latency_ms)) ** 0.1)
        param_factor = min(1.0, (self.target_parameters / max(1000, param_count)) ** 0.05)
        fitness_score = float(round(val_accuracy * latency_factor * param_factor, 4))

        return EvaluationMetrics(
            val_accuracy=val_accuracy,
            val_loss=val_loss,
            inference_latency_ms=avg_latency_ms,
            parameter_count=param_count,
            macs_count=macs_count,
            fitness_score=fitness_score,
        )


child_evaluator = ChildModelEvaluator()
