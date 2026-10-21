"""Neural Architecture Search (NAS) & Controller AI Module.
Contains the complete 5-step closed-loop autonomous NAS framework:
1. Controller AI - Architecture Proposal
2. Child Model - Instantiation & Compilation
3. Model Training - Empirical Fitting
4. Evaluation - Accuracy & Efficiency Validation
5. Feedback Loop - Policy Gradient (REINFORCE) & Evolutionary Update
"""

from backend.nas.models import (
    BlockType,
    ActivationType,
    NormType,
    SearchStrategy,
    BlockSpec,
    Hyperparameters,
    ArchitectureCandidate,
    ArchitectureProposalRequest,
    TrainingMetrics,
    EvaluationMetrics,
    RewardFeedback,
    NASCycleResult,
    NASExperimentState,
)
from backend.nas.search_space import search_space, SearchSpace
from backend.nas.controller import controller_ai, ControllerAI
from backend.nas.child_network import ConcreteChildNetwork, instantiate_child_network
from backend.nas.trainer import child_trainer, ChildModelTrainer
from backend.nas.evaluator import child_evaluator, ChildModelEvaluator
from backend.nas.feedback import feedback_engine, FeedbackLoopEngine
from backend.nas.orchestrator import nas_orchestrator, NASCycleOrchestrator

__all__ = [
    "BlockType",
    "ActivationType",
    "NormType",
    "SearchStrategy",
    "BlockSpec",
    "Hyperparameters",
    "ArchitectureCandidate",
    "ArchitectureProposalRequest",
    "TrainingMetrics",
    "EvaluationMetrics",
    "RewardFeedback",
    "NASCycleResult",
    "NASExperimentState",
    "search_space",
    "SearchSpace",
    "controller_ai",
    "ControllerAI",
    "ConcreteChildNetwork",
    "instantiate_child_network",
    "child_trainer",
    "ChildModelTrainer",
    "child_evaluator",
    "ChildModelEvaluator",
    "feedback_engine",
    "FeedbackLoopEngine",
    "nas_orchestrator",
    "NASCycleOrchestrator",
]
