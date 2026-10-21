"""Closed-Loop NAS Cycle Orchestrator.
Connects all 5 steps into an autonomous continuous optimization loop:
Step 1: Controller AI Architecture Proposal
Step 2: Child Model Concrete Instantiation & Compilation
Step 3: Model Training on Target Dataset (Empirical Fitting)
Step 4: Accuracy & Efficiency Evaluation
Step 5: Reinforcement Learning (REINFORCE) / Evolutionary Feedback Loop
"""

import time
import uuid
from typing import Dict, List, Any, Optional

from backend.nas.models import (
    SearchStrategy,
    ArchitectureCandidate,
    ArchitectureProposalRequest,
    TrainingMetrics,
    EvaluationMetrics,
    RewardFeedback,
    NASCycleResult,
    NASExperimentState,
)
from backend.nas.controller import controller_ai, ControllerAI
from backend.nas.child_network import instantiate_child_network, ConcreteChildNetwork
from backend.nas.trainer import child_trainer, ChildModelTrainer
from backend.nas.evaluator import child_evaluator, ChildModelEvaluator
from backend.nas.feedback import feedback_engine, FeedbackLoopEngine


class NASCycleOrchestrator:
    """Master orchestrator executing the 5-step closed-loop NAS cycle."""

    def __init__(
        self,
        controller: Optional[ControllerAI] = None,
        trainer: Optional[ChildModelTrainer] = None,
        evaluator: Optional[ChildModelEvaluator] = None,
        feedback: Optional[FeedbackLoopEngine] = None,
    ):
        self.controller = controller or controller_ai
        self.trainer = trainer or child_trainer
        self.evaluator = evaluator or child_evaluator
        self.feedback_engine = feedback or feedback_engine

        self.cycle_history: List[NASCycleResult] = []
        self.experiment_state = NASExperimentState(
            experiment_id=f"exp-{uuid.uuid4().hex[:8]}",
        )

    def run_single_cycle(
        self,
        request: Optional[ArchitectureProposalRequest] = None,
        epochs: int = 4,
    ) -> NASCycleResult:
        """Executes one complete 5-step cycle:
        1. Architecture Proposal (Controller)
        2. Child Model Instantiation (PyTorch Network)
        3. Model Training (Empirical Fitting)
        4. Evaluation (Accuracy, Latency, FLOPs)
        5. Feedback Loop (Policy Gradient REINFORCE Update)
        """
        cycle_idx = len(self.cycle_history) + 1
        t_start = time.perf_counter()

        # Step 1: Controller AI Architecture Proposal
        req = request or ArchitectureProposalRequest(
            strategy=SearchStrategy.AUTOREGRESSIVE_RNN,
            min_layers=3,
            max_layers=6,
        )
        candidate = self.controller.propose_architecture(req)

        # Step 2: Child Model Instantiation
        child_model, compilation_info = instantiate_child_network(candidate)

        # Step 3: Model Training (Empirical Fitting)
        training_metrics = self.trainer.train(child_model, epochs=epochs)

        # Step 4: Evaluation (Performance Measurement)
        eval_metrics = self.evaluator.evaluate(child_model)

        # Step 5: Feedback Loop (Controller Strategy Update)
        reward_feedback = self.feedback_engine.update_controller(
            controller=self.controller,
            candidate=candidate,
            metrics=eval_metrics,
        )

        total_time_ms = (time.perf_counter() - t_start) * 1000.0

        result = NASCycleResult(
            cycle_index=cycle_idx,
            step_1_proposal=candidate,
            step_2_instantiation=compilation_info,
            step_3_training=training_metrics,
            step_4_evaluation=eval_metrics,
            step_5_feedback=reward_feedback,
            total_cycle_time_ms=float(round(total_time_ms, 2)),
        )

        self.cycle_history.append(result)
        self._update_experiment_state(result)
        return result

    def run_experiment(
        self,
        num_cycles: int = 5,
        request: Optional[ArchitectureProposalRequest] = None,
        epochs_per_child: int = 3,
    ) -> NASExperimentState:
        """Runs an autonomous multi-cycle NAS experiment looping through steps 1-5."""
        for _ in range(num_cycles):
            self.run_single_cycle(request=request, epochs=epochs_per_child)
        return self.experiment_state

    def _update_experiment_state(self, res: NASCycleResult):
        """Updates cumulative Pareto frontier and reward tracking."""
        self.experiment_state.total_cycles_completed += 1
        acc = res.step_4_evaluation.val_accuracy
        fitness = res.step_4_evaluation.fitness_score
        cand = res.step_1_proposal

        self.experiment_state.reward_history.append(res.step_5_feedback.final_reward)
        self.experiment_state.accuracy_history.append(acc)

        # Update best candidate
        if fitness > self.experiment_state.best_fitness:
            self.experiment_state.best_fitness = fitness
            self.experiment_state.best_accuracy = acc
            self.experiment_state.best_candidate = cand

        # Add to Pareto frontier record
        self.experiment_state.pareto_frontier.append({
            "cycle": res.cycle_index,
            "arch_id": cand.arch_id,
            "name": cand.name,
            "val_accuracy": acc,
            "fitness": fitness,
            "latency_ms": res.step_4_evaluation.inference_latency_ms,
            "parameters": res.step_4_evaluation.parameter_count,
            "strategy": cand.strategy_used.value,
        })
        # Sort Pareto frontier by fitness descending
        self.experiment_state.pareto_frontier.sort(key=lambda x: x["fitness"], reverse=True)


nas_orchestrator = NASCycleOrchestrator()
