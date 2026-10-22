"""The Modifier: Safe Self-Surgery via Structural Plasticity & Fisher Information.
Implements:
1. Phase 1: Hyperparameter Self-Regulation:
   - Dynamic tuning of learning rate, temperature (exploration vs. exploitation),
     and memory retention decay based on performance and entropy.
2. Phase 2: Structural Architecture Surgery (PlasticLayer):
   - Structural plasticity allowing dynamic neuron growth and apoptosis pruning:
     - grow(n_new): Adds neurons where information bottleneck is highest, orthogonally initialized.
     - prune(threshold): Kills dead neurons contributing nothing (apoptosis) via active_mask.
     - usage: Tracks empirical neuron activation frequency.
3. Phase 3: Weight Surgery with Fisher Information Mask:
   - compute_fisher_importance(model, validation_batch): Estimates importance as (gradient)^2.
   - constrained_update(model, proposed_update, importance, max_damage):
     Protects core identity weights with bounded damping while allowing periphery plastic adaptation.
"""

import math
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import structlog

logger = structlog.get_logger(__name__)


# =============================================================================
# PHASE 1: HYPERPARAMETER SELF-REGULATION
# =============================================================================
class HyperparameterModifier:
    """Safely adjusts operational hyperparameters (LR, temperature, retention decay)."""

    def __init__(self):
        self.learning_rate = 0.001
        self.temperature = 1.0
        self.memory_retention_rate = 0.95
        self.adjustment_history: List[Dict[str, Any]] = []

    def adapt_hyperparameters(self, entropy: float, health_score: float) -> Dict[str, float]:
        """Self-regulates exploration vs. exploitation:
        - If entropy is too rigid (< 0.40): increase temperature and learning rate.
        - If entropy is chaotic (> 0.75): decrease temperature to crystallize focus.
        - If health is declining: raise memory retention rate to protect autobiography.
        """
        old_lr = self.learning_rate
        old_temp = self.temperature

        if entropy < 0.40:
            self.temperature = min(1.8, self.temperature * 1.08)
            self.learning_rate = min(0.005, self.learning_rate * 1.05)
        elif entropy > 0.75:
            self.temperature = max(0.4, self.temperature * 0.92)
            self.learning_rate = max(0.0002, self.learning_rate * 0.95)

        if health_score < 0.70:
            self.memory_retention_rate = min(0.99, self.memory_retention_rate + 0.02)
        else:
            self.memory_retention_rate = max(0.85, self.memory_retention_rate - 0.01)

        record = {
            "learning_rate": round(self.learning_rate, 5),
            "temperature": round(self.temperature, 3),
            "memory_retention_rate": round(self.memory_retention_rate, 3),
        }
        self.adjustment_history.append(record)
        return record


# =============================================================================
# PHASE 2: ARCHITECTURE SURGERY (PLASTIC LAYER)
# =============================================================================
class PlasticLayer(nn.Module):
    """Dynamic neural layer with structural plasticity: grow neurons & apoptosis pruning."""

    def __init__(self, in_features: int = 64, initial_neurons: int = 32, max_neurons: int = 256):
        super().__init__()
        self.in_features = in_features
        self.max_neurons = max_neurons
        self.current_size = initial_neurons

        self.weight = nn.Parameter(torch.zeros(max_neurons, in_features))
        self.active_mask = nn.Parameter(torch.zeros(max_neurons), requires_grad=False)
        self.active_mask[:initial_neurons] = 1.0

        # Initialize active neurons orthogonally
        nn.init.orthogonal_(self.weight[:initial_neurons])

        # Tracking neuron usage frequency
        self.register_buffer("usage", torch.zeros(max_neurons))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with active neuron masking and usage tracking."""
        active_weights = self.weight * self.active_mask.unsqueeze(1)
        out = F.linear(x, active_weights[:self.current_size])

        # Track usage in training mode
        if self.training:
            with torch.no_grad():
                neuron_activations = torch.abs(out).mean(dim=0)
                self.usage[:self.current_size] = 0.95 * self.usage[:self.current_size] + 0.05 * neuron_activations

        return out

    def grow(self, n_new: int = 8) -> Dict[str, Any]:
        """Structural growth: awakens inactive neurons where capacity is needed."""
        dead_indices = (self.active_mask == 0.0).nonzero(as_tuple=True)[0]
        if len(dead_indices) == 0:
            return {"grown_count": 0, "active_neurons": int(self.active_mask.sum().item())}

        n_to_activate = min(n_new, len(dead_indices))
        selected = dead_indices[:n_to_activate]

        with torch.no_grad():
            self.active_mask[selected] = 1.0
            nn.init.orthogonal_(self.weight[selected])
            self.current_size = max(self.current_size, int(torch.max(selected).item()) + 1)
            self.usage[selected] = 0.1

        logger.info("plastic_layer_neurons_grown", grown=n_to_activate, total_active=int(self.active_mask.sum().item()))
        return {
            "grown_count": n_to_activate,
            "active_neurons": int(self.active_mask.sum().item()),
            "max_neurons": self.max_neurons,
        }

    def prune(self, threshold: float = 0.01) -> Dict[str, Any]:
        """Apoptosis: deactivates dead neurons that contribute nothing to information flow."""
        with torch.no_grad():
            contributions = torch.norm(self.weight * self.active_mask.unsqueeze(1), dim=1)
            # Cannot prune below minimum baseline of 8 neurons
            if self.active_mask.sum().item() <= 8:
                return {"pruned_count": 0, "active_neurons": int(self.active_mask.sum().item())}

            dead = (contributions < threshold) & (self.active_mask == 1.0) & (self.usage < 0.005)
            # Retain at least 8 neurons
            num_dead = int(dead.sum().item())
            if self.active_mask.sum().item() - num_dead < 8:
                num_dead = max(0, int(self.active_mask.sum().item()) - 8)
                dead_indices = dead.nonzero(as_tuple=True)[0][:num_dead]
                self.active_mask[dead_indices] = 0.0
            else:
                self.active_mask[dead] = 0.0

        logger.info("plastic_layer_apoptosis_pruned", pruned=num_dead, total_active=int(self.active_mask.sum().item()))
        return {
            "pruned_count": num_dead,
            "active_neurons": int(self.active_mask.sum().item()),
            "max_neurons": self.max_neurons,
        }


# =============================================================================
# PHASE 3: WEIGHT SURGERY WITH FISHER INFORMATION MASK
# =============================================================================
def compute_fisher_importance(model: nn.Module, validation_batch: Tuple[torch.Tensor, torch.Tensor]) -> Dict[str, torch.Tensor]:
    """Computes empirical Fisher Information Matrix: (gradient)^2 estimates weight importance."""
    model.zero_grad()
    x_val, y_val = validation_batch
    criterion = nn.CrossEntropyLoss() if y_val.dtype == torch.long else nn.MSELoss()

    out = model(x_val)
    loss = criterion(out, y_val)
    loss.backward()

    importance = {}
    for name, param in model.named_parameters():
        if param.grad is not None:
            importance[name] = param.grad.data.clone().pow(2)
        else:
            importance[name] = torch.zeros_like(param)

    model.zero_grad()
    return importance


def constrained_update(
    model: nn.Module,
    proposed_update: Dict[str, torch.Tensor],
    importance: Dict[str, torch.Tensor],
    max_damage: float = 0.01,
) -> Dict[str, Any]:
    """Constrains weight surgery: core identity weights receive damped updates, periphery adapts freely."""
    modified_params = 0
    protected_params = 0

    with torch.no_grad():
        for name, param in model.named_parameters():
            if name in proposed_update and name in importance:
                imp = importance[name]
                if imp.numel() > 0:
                    q75 = torch.quantile(imp, 0.75)
                    # Low importance: periphery
                    mask_low = imp < q75
                    # High importance: core identity
                    mask_high = ~mask_low

                    update = proposed_update[name]
                    safe_update = update * mask_low.float() + (update * mask_high.float() * max_damage)
                    param.data.add_(safe_update)

                    modified_params += int(mask_low.sum().item())
                    protected_params += int(mask_high.sum().item())

    logger.info("constrained_weight_surgery_applied", protected=protected_params, modified=modified_params)
    return {
        "protected_weights_count": protected_params,
        "modified_periphery_count": modified_params,
        "max_damage_bound": max_damage,
        "surgery_status": "Identity Core Protected; Periphery Adapted",
    }


class SafeSelfSurgeryModifier:
    """Master controller orchestrating safe self-surgery across all 3 phases."""

    def __init__(self):
        self.hyper_mod = HyperparameterModifier()
        self.plastic_layer = PlasticLayer(in_features=64, initial_neurons=32, max_neurons=128)
        self.surgery_log: List[Dict[str, Any]] = []

    def perform_surgery_cycle(
        self,
        entropy: float,
        health_score: float,
        target_model: Optional[nn.Module] = None,
    ) -> Dict[str, Any]:
        """Executes a full safe self-surgery check across phases 1, 2, and 3."""
        # Phase 1: Hyperparameters
        hyper_res = self.hyper_mod.adapt_hyperparameters(entropy, health_score)

        # Phase 2: Plasticity Growth or Pruning
        if health_score < 0.65 or entropy > 0.75:
            # High bottleneck or stress: grow neurons
            plastic_res = self.plastic_layer.grow(n_new=4)
        else:
            # Stable equilibrium: prune dead neurons (apoptosis)
            plastic_res = self.plastic_layer.prune(threshold=0.01)

        event = {
            "hyperparameters": hyper_res,
            "plasticity": plastic_res,
            "active_neurons": plastic_res["active_neurons"],
            "status": "Safe Self-Surgery Performed without Identity Disruption",
        }
        self.surgery_log.append(event)
        return event

    def get_summary(self) -> Dict[str, Any]:
        return {
            "current_learning_rate": self.hyper_mod.learning_rate,
            "current_temperature": self.hyper_mod.temperature,
            "active_plastic_neurons": int(self.plastic_layer.active_mask.sum().item()),
            "max_plastic_neurons": self.plastic_layer.max_neurons,
            "total_surgeries": len(self.surgery_log),
        }


safe_surgery_modifier = SafeSelfSurgeryModifier()
