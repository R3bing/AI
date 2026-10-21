"""Unit tests for NAS Controller AI, Search Space, and Architecture Sampling."""

import pytest
from backend.nas.models import (
    BlockType,
    ActivationType,
    NormType,
    SearchStrategy,
    ArchitectureProposalRequest,
)
from backend.nas.search_space import search_space
from backend.nas.controller import controller_ai, ControllerAI


def test_search_space_initialization():
    assert len(search_space.block_types) >= 6
    assert BlockType.DENSE in search_space.block_types
    assert BlockType.RESIDUAL_BLOCK in search_space.block_types
    assert BlockType.QUANTUM_VARIATIONAL in search_space.block_types
    assert len(search_space.hidden_dimensions) >= 4
    assert len(search_space.activations) >= 5
    assert len(search_space.optimizers) >= 3


def test_search_space_parameter_calculation():
    dense_params = search_space.calculate_block_parameters(
        block_type=BlockType.DENSE,
        in_features=128,
        out_features=256,
    )
    # W (128 * 256) + b (256) = 32768 + 256 = 33024
    assert dense_params == 33024

    attn_params = search_space.calculate_block_parameters(
        block_type=BlockType.MULTI_HEAD_ATTENTION,
        in_features=128,
        out_features=128,
        num_heads=4,
    )
    assert attn_params > dense_params


def test_autoregressive_rnn_controller_proposal():
    controller = ControllerAI(seed=42)
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        min_layers=4,
        max_layers=6,
        input_dim=128,
        output_dim=32,
        temperature=1.0,
    )
    candidate = controller.propose_architecture(req)

    assert candidate is not None
    assert candidate.arch_id.startswith("arch-")
    assert candidate.strategy_used == SearchStrategy.AUTOREGRESSIVE_RNN
    assert 4 <= len(candidate.blocks) <= 6
    assert candidate.blocks[0].in_features == 128
    assert candidate.blocks[-1].out_features == 32
    assert candidate.estimated_parameters > 0
    assert candidate.hyperparameters.learning_rate in search_space.learning_rates
    assert candidate.hyperparameters.optimizer in search_space.optimizers
    assert len(candidate.dag_topology) == len(candidate.blocks)


def test_transformer_structural_sampler():
    controller = ControllerAI(seed=101)
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.TRANSFORMER_SAMPLER,
        min_layers=3,
        max_layers=5,
        input_dim=64,
        output_dim=16,
    )
    candidate = controller.propose_architecture(req)

    assert candidate is not None
    assert candidate.strategy_used == SearchStrategy.TRANSFORMER_SAMPLER
    assert len(candidate.blocks) >= 3
    assert candidate.blocks[0].in_features == 64
    assert candidate.blocks[-1].out_features == 16


def test_evolutionary_mutation_and_crossover():
    controller = ControllerAI(seed=7)
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        min_layers=4,
        max_layers=4,
        input_dim=128,
        output_dim=64,
    )
    parent_a = controller.propose_architecture(req)
    parent_b = controller.propose_architecture(req)

    # Mutation test
    mutant = controller.mutate_architecture(parent_a)
    assert mutant is not None
    assert mutant.strategy_used == SearchStrategy.EVOLUTIONARY_GENETIC
    assert parent_a.arch_id in mutant.parent_ids
    assert len(mutant.blocks) == len(parent_a.blocks)

    # Crossover test
    child = controller.crossover(parent_a, parent_b)
    assert child is not None
    assert child.strategy_used == SearchStrategy.EVOLUTIONARY_GENETIC
    assert parent_a.arch_id in child.parent_ids
    assert parent_b.arch_id in child.parent_ids


def test_batch_sampling():
    controller = ControllerAI(seed=99)
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        num_candidates=3,
        min_layers=3,
        max_layers=5,
    )
    batch = controller.sample_batch(req)
    assert len(batch) == 3
    # Ensure candidates are distinct
    arch_ids = [c.arch_id for c in batch]
    assert len(set(arch_ids)) == 3


def test_mermaid_dag_and_pytorch_export():
    controller = ControllerAI(seed=12)
    candidate = controller.propose_architecture()

    # Mermaid DAG Export
    mermaid_str = controller.to_mermaid_dag(candidate)
    assert "graph TD" in mermaid_str
    assert candidate.blocks[0].block_id in mermaid_str

    # PyTorch Code Export
    pytorch_code = controller.to_pytorch_code(candidate)
    assert "import torch" in pytorch_code
    assert "class " in pytorch_code
    assert "def forward(" in pytorch_code
