"""Unit tests for NAS Closed-Loop Engine (Steps 1 through 5)."""

import pytest
import torch
from backend.nas.models import (
    SearchStrategy,
    ArchitectureProposalRequest,
)
from backend.nas.controller import controller_ai, ControllerAI
from backend.nas.child_network import instantiate_child_network, ConcreteChildNetwork
from backend.nas.trainer import child_trainer, DatasetFactory
from backend.nas.evaluator import child_evaluator
from backend.nas.feedback import feedback_engine, FeedbackLoopEngine
from backend.nas.orchestrator import NASCycleOrchestrator


def test_step_2_child_model_instantiation():
    controller = ControllerAI(seed=42)
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        min_layers=3,
        max_layers=4,
        input_dim=64,
        output_dim=10,
    )
    candidate = controller.propose_architecture(req)
    model, compile_info = instantiate_child_network(candidate)

    assert isinstance(model, ConcreteChildNetwork)
    assert compile_info["status"] == "compiled_successfully"
    assert compile_info["total_trainable_params"] > 0
    assert compile_info["output_shape"] == [2, 10]

    # Verify forward pass
    dummy_input = torch.randn(4, 64)
    output = model(dummy_input)
    assert output.shape == (4, 10)


def test_step_3_child_model_training():
    controller = ControllerAI(seed=12)
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        min_layers=3,
        max_layers=3,
        input_dim=32,
        output_dim=5,
    )
    candidate = controller.propose_architecture(req)
    model, _ = instantiate_child_network(candidate)

    train_loader, _ = DatasetFactory.get_benchmark_dataset(
        num_samples=100,
        input_dim=32,
        num_classes=5,
    )

    metrics = child_trainer.train(model, train_loader=train_loader, epochs=3)
    assert metrics.epochs_trained == 3
    assert len(metrics.loss_history) == 3
    assert metrics.training_time_ms > 0
    assert 0.0 <= metrics.train_accuracy <= 1.0


def test_step_4_child_model_evaluation():
    controller = ControllerAI(seed=99)
    req = ArchitectureProposalRequest(
        min_layers=3,
        max_layers=3,
        input_dim=32,
        output_dim=5,
    )
    candidate = controller.propose_architecture(req)
    model, _ = instantiate_child_network(candidate)

    _, val_loader = DatasetFactory.get_benchmark_dataset(
        num_samples=100,
        input_dim=32,
        num_classes=5,
    )

    eval_res = child_evaluator.evaluate(model, val_loader=val_loader, benchmark_runs=3)
    assert 0.0 <= eval_res.val_accuracy <= 1.0
    assert eval_res.inference_latency_ms > 0
    assert eval_res.parameter_count > 0
    assert 0.0 <= eval_res.fitness_score <= 1.0


def test_step_5_feedback_policy_update():
    controller = ControllerAI(seed=55)
    feedback = FeedbackLoopEngine(baseline_decay=0.8, policy_lr=0.05)
    cand = controller.propose_architecture()
    model, _ = instantiate_child_network(cand)
    eval_metrics = child_evaluator.evaluate(model)

    initial_baseline = feedback.moving_baseline
    w_before = controller.W_rnn.copy()

    res = feedback.update_controller(controller, cand, eval_metrics)
    assert res.policy_updated is True
    assert feedback.moving_baseline != initial_baseline
    # Check that weights were perturbed by policy gradient
    assert not (controller.W_rnn == w_before).all()


def test_full_closed_loop_cycle_orchestration():
    orchestrator = NASCycleOrchestrator()
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        min_layers=3,
        max_layers=4,
        input_dim=32,
        output_dim=5,
    )

    cycle_result = orchestrator.run_single_cycle(request=req, epochs=2)
    assert cycle_result.cycle_index == 1
    assert cycle_result.step_1_proposal is not None
    assert cycle_result.step_2_instantiation["status"] == "compiled_successfully"
    assert cycle_result.step_3_training.epochs_trained == 2
    assert cycle_result.step_4_evaluation.val_accuracy >= 0.0
    assert cycle_result.step_5_feedback.policy_updated is True
    assert cycle_result.total_cycle_time_ms > 0


def test_multi_cycle_nas_experiment():
    orchestrator = NASCycleOrchestrator()
    req = ArchitectureProposalRequest(
        strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
        min_layers=3,
        max_layers=3,
        input_dim=32,
        output_dim=4,
    )

    exp_state = orchestrator.run_experiment(num_cycles=2, request=req, epochs_per_child=2)
    assert exp_state.total_cycles_completed == 2
    assert len(exp_state.reward_history) == 2
    assert len(exp_state.accuracy_history) == 2
    assert len(exp_state.pareto_frontier) == 2
    assert exp_state.best_candidate is not None
