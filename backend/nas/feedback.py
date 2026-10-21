"""Feedback Loop Engine (Step 5 of NAS Cycle).
Executes Reinforcement Learning (Policy Gradient / REINFORCE) and Evolutionary
policy updates using child validation performance as the reward signal.
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from backend.nas.models import (
    SearchStrategy,
    ArchitectureCandidate,
    EvaluationMetrics,
    RewardFeedback,
)
from backend.nas.controller import ControllerAI


class FeedbackLoopEngine:
    """Step 5: Reinforcement Learning policy updater and evolutionary fitness feedback engine."""

    def __init__(self, baseline_decay: float = 0.85, policy_lr: float = 0.05):
        self.baseline_decay = baseline_decay
        self.policy_lr = policy_lr
        self.moving_baseline = 0.5  # Initial expectation baseline
        self.reward_history: List[float] = []
        self.advantage_history: List[float] = []

    def update_controller(
        self,
        controller: ControllerAI,
        candidate: ArchitectureCandidate,
        metrics: EvaluationMetrics,
    ) -> RewardFeedback:
        """Feeds validation accuracy and fitness back to Controller AI to update its generative policy."""
        # Multi-objective reward signal: 80% accuracy + 20% efficiency fitness
        raw_reward = (0.80 * metrics.val_accuracy) + (0.20 * metrics.fitness_score)

        # 1. Update Exponential Moving Average Baseline
        current_baseline = self.moving_baseline
        advantage = raw_reward - current_baseline
        self.moving_baseline = (self.baseline_decay * current_baseline) + ((1.0 - self.baseline_decay) * raw_reward)

        self.reward_history.append(raw_reward)
        self.advantage_history.append(advantage)

        policy_loss = 0.0
        updated = True

        # 2. Reinforcement Learning Update (REINFORCE Algorithm)
        if candidate.strategy_used in [SearchStrategy.AUTOREGRESSIVE_RNN, SearchStrategy.TRANSFORMER_SAMPLER]:
            # REINFORCE update: theta = theta + alpha * advantage * grad_log_prob
            # Simulated gradient direction based on sampled candidate block choices
            direction = 1.0 if advantage >= 0.0 else -1.0
            perturbation = direction * self.policy_lr * abs(advantage) * np.tanh(controller.W_rnn)

            # Apply policy gradient step to controller recurrent weights
            controller.W_rnn = controller.W_rnn + perturbation
            # Bound controller weights to prevent gradient explosion
            controller.W_rnn = np.clip(controller.W_rnn, -3.0, 3.0)

            # Approximate REINFORCE policy loss: - log_prob * (Reward - Baseline)
            approx_log_prob = -float(candidate.entropy * len(candidate.blocks))
            policy_loss = float(round(-approx_log_prob * advantage, 4))

        # 3. Evolutionary Fitness Feedback
        elif candidate.strategy_used == SearchStrategy.EVOLUTIONARY_GENETIC:
            # Store fitness in candidate metadata for future parent selection
            candidate.metadata["fitness_score"] = metrics.fitness_score
            candidate.metadata["val_accuracy"] = metrics.val_accuracy
            # Sort history so highest fitness candidates are sampled as mutation/crossover parents
            controller.proposal_history.sort(
                key=lambda c: c.metadata.get("fitness_score", 0.0),
                reverse=True,
            )

        return RewardFeedback(
            raw_metric=metrics.val_accuracy,
            baseline=float(round(current_baseline, 4)),
            advantage=float(round(advantage, 4)),
            latency_penalty=1.0,
            final_reward=float(round(raw_reward, 4)),
            policy_loss=policy_loss,
            policy_updated=updated,
        )


feedback_engine = FeedbackLoopEngine()
