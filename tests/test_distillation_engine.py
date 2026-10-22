"""Tests for Knowledge Distillation, Active Model Extraction, LoRA, and SLERP Merging."""

import pytest
import torch
import torch.nn as nn
from backend.ml.distillation_engine import (
    LoRALinear,
    KnowledgeDistillationEngine,
    distillation_engine,
)


def test_lora_linear_forward_and_parameter_reduction():
    layer = LoRALinear(in_features=32, out_features=16, rank=4, lora_alpha=8.0, freeze_base=True)
    x = torch.randn(8, 32)
    out = layer(x)
    assert out.shape == (8, 16)

    # Base layer is frozen, only LoRA matrices require grad
    assert layer.base_layer.weight.requires_grad is False
    assert layer.lora_A.requires_grad is True
    assert layer.lora_B.requires_grad is True

    # Test dynamic injection into standard model
    model = nn.Sequential(
        nn.Linear(32, 64),
        nn.ReLU(),
        nn.Linear(64, 10),
    )
    meta = distillation_engine.inject_lora_into_model(model, rank=2)
    assert meta["trainable_params_after"] < meta["trainable_params_before"]
    assert meta["parameter_reduction_pct"] > 50.0


def test_hinton_distillation_loss():
    student_logits = torch.randn(10, 4)
    teacher_logits = torch.randn(10, 4)
    labels = torch.randint(0, 4, (10,))

    loss, soft_val, hard_val = KnowledgeDistillationEngine.compute_distillation_loss(
        student_logits=student_logits,
        teacher_logits=teacher_logits,
        labels=labels,
        temperature=3.0,
        alpha=0.7,
    )
    assert loss.item() > 0.0
    assert soft_val >= 0.0
    assert hard_val >= 0.0


def test_shannon_entropy_active_query_ranking():
    logits = torch.tensor([[10.0, -10.0, -10.0], [1.0, 1.0, 1.0]])
    entropy = KnowledgeDistillationEngine.compute_shannon_entropy(logits)
    # Uniform logits (1, 1, 1) must have higher entropy than confident logits
    assert entropy[1].item() > entropy[0].item()

    queries = [
        "What is quantum entanglement and how does it relate to divine consciousness?",
        "test query",
    ]
    ranked = distillation_engine.active_query_entropy_ranking(queries)
    assert len(ranked) == 2
    assert ranked[0]["epistemic_entropy"] >= ranked[1]["epistemic_entropy"]


def test_slerp_weight_merging():
    w1 = torch.tensor([1.0, 0.0, 0.0])
    w2 = torch.tensor([0.0, 1.0, 0.0])

    merged = KnowledgeDistillationEngine.slerp_merge_tensors(w1, w2, t=0.5)
    # Norm of orthogonal unit vectors at t=0.5 should be normalized along the arc
    assert torch.isclose(torch.norm(merged), torch.tensor(1.0), atol=1e-3)


def test_run_distillation_experiment():
    student = nn.Sequential(
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 4),
    )
    res = distillation_engine.run_distillation_experiment(
        student_model=student,
        epochs=3,
        temperature=2.5,
        alpha=0.6,
        use_lora=True,
        lora_rank=2,
    )
    assert res["epochs"] == 3
    assert len(res["loss_history"]) == 3
    assert res["dark_knowledge_fidelity"] >= 0.0
    assert res["lora_enabled"] is True
