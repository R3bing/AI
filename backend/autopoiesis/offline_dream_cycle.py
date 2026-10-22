"""Offline Dream Cycle & Memory Consolidation Engine.
Transfers experiences from short-term buffer (STM) to long-term memory matrix (LTM)
through weighted salience sampling, noise-distorted replay, counterfactual simulation,
memory reconsolidation via Metacortex reframing, and synaptic Lyapunov decay.
"""

import time
import math
import random
from typing import Dict, Any, List, Optional
import numpy as np
import torch
import torch.nn as nn
import structlog

from backend.autopoiesis.persistent_state_engine import persistent_identity_engine
from backend.autopoiesis.metacortex import metacortex_engine

logger = structlog.get_logger(__name__)


class ExperienceRecord:
    """Encapsulates a single cognitive experience step."""

    def __init__(
        self,
        query: str,
        sensory_vector: np.ndarray,
        dominant_mode: str,
        prediction_error: float,
        reward_valence: float,
        timestamp: Optional[float] = None,
    ):
        self.query = query
        self.sensory_vector = sensory_vector
        self.dominant_mode = dominant_mode
        self.prediction_error = float(prediction_error)
        self.reward_valence = float(reward_valence)
        self.salience = abs(self.prediction_error) + abs(self.reward_valence) + 1e-4
        self.timestamp = timestamp or time.time()


class OfflineDreamCycle:
    """Manages offline memory replay, counterfactual distillation, and synaptic downscaling."""

    def __init__(self, max_stm_capacity: int = 5000):
        self.stm: List[ExperienceRecord] = []
        self.max_stm_capacity = max_stm_capacity
        self.identity_engine = persistent_identity_engine
        self.metacortex = metacortex_engine
        self.total_sleep_cycles = 0
        self.total_experiences_consolidated = 0
        self.last_sleep_timestamp = time.time()

    def record_experience(
        self,
        query: str,
        sensory_vector: np.ndarray,
        dominant_mode: str,
        prediction_error: float = 0.25,
        reward_valence: float = 0.1,
    ):
        """Pushes an incoming waking experience into the short-term buffer."""
        exp = ExperienceRecord(
            query=query,
            sensory_vector=sensory_vector,
            dominant_mode=dominant_mode,
            prediction_error=prediction_error,
            reward_valence=reward_valence,
        )
        self.stm.append(exp)
        if len(self.stm) > self.max_stm_capacity:
            self.stm.pop(0)

    def compute_dream_buffer_entropy(self) -> float:
        """Measures the information entropy / unprocessed tension of the STM buffer."""
        if not self.stm:
            return 0.1

        errors = np.array([e.prediction_error for e in self.stm], dtype=np.float32)
        errors = np.clip(errors, 1e-4, 10.0)
        probs = errors / np.sum(errors)
        entropy = -float(np.sum(probs * np.log2(probs + 1e-9)))
        return round(float(np.clip(entropy, 0.05, 5.0)), 4)

    def sleep(self, duration_minutes: float = 0.5, batch_size: int = 32) -> Dict[str, Any]:
        """Executes the full 6-phase offline consolidation dream cycle.
        
        Phases:
        1. Salient Experience Sampling (weighted by prediction error + valence).
        2. Distorted Hallucination Replay (noise injection for invariant extraction).
        3. Low-Rate LTM Consolidation (gradual embedding into persistent memory tape M).
        4. Counterfactual Simulation ('what if alternative actions were chosen?').
        5. Memory Reconsolidation (metacortex reframes older memories with current self-model).
        6. Synaptic Downscaling (Lyapunov regularization to prevent saturation).
        """
        t_start = time.perf_counter()
        if not self.stm:
            # Generate baseline resting consolidation
            svd_res = self.identity_engine.dream_and_consolidate()
            return {
                "status": "Quiescent Sleep (Empty Buffer)",
                "dream_state": "SVD_CONSOLIDATION_COMPLETE",
                "variance_explained": svd_res.get("variance_explained", svd_res.get("energy_preserved", 0.95)),
                "experiences_consolidated": 0,
                "svd_energy_preserved": svd_res.get("energy_preserved", 0.95),
                "duration_seconds": round(time.perf_counter() - t_start, 3),
            }

        # -------------------------------------------------------------
        # PHASE 1: SALIENT EXPERIENCE SAMPLING
        # -------------------------------------------------------------
        n_sample = min(len(self.stm), batch_size)
        saliences = np.array([e.salience for e in self.stm], dtype=np.float32)
        sample_probs = saliences / np.sum(saliences)
        chosen_indices = np.random.choice(len(self.stm), size=n_sample, p=sample_probs, replace=len(self.stm) < n_sample)
        dream_batch = [self.stm[i] for i in chosen_indices]

        # -------------------------------------------------------------
        # PHASE 2: DISTORTED HALLUCINATION REPLAY (DATA AUGMENTATION)
        # -------------------------------------------------------------
        distorted_inputs = []
        noise_scale = 0.10
        for exp in dream_batch:
            raw_v = exp.sensory_vector.copy()
            noise = np.random.normal(0, noise_scale, size=raw_v.shape).astype(np.float32)
            distorted_v = np.clip(raw_v + noise, -2.0, 2.0)
            distorted_inputs.append((distorted_v, exp.query))

        # -------------------------------------------------------------
        # PHASE 3: CONSOLIDATION INTO LTM (SLOW LEARNING RATE)
        # -------------------------------------------------------------
        # Feed distorted replays through DNC memory write head with slow rate
        consolidated_slots = []
        with torch.no_grad():
            for dist_v, lbl in distorted_inputs:
                step_res = self.identity_engine.update_state(
                    sensory_input_vector=dist_v,
                    inquiry_label=f"Dream: {lbl[:20]}",
                )
                consolidated_slots.append(step_res["top_memory_label"])

        # -------------------------------------------------------------
        # PHASE 4: COUNTERFACTUAL REPLAY ("WHAT IF?")
        # -------------------------------------------------------------
        counterfactuals_evaluated = 0
        for exp in dream_batch[:8]:
            alt_mode = "Wave (Qalb)" if "aql" in exp.dominant_mode.lower() else "Particle (Aql)"
            alt_res = self.metacortex.update_with_actual_outcome(
                actual_mode=alt_mode,
                actual_latency_ms=random.uniform(5.0, 25.0),
            )
            counterfactuals_evaluated += 1

        # -------------------------------------------------------------
        # PHASE 5: MEMORY RECONSOLIDATION (METACORTEX REFRAMING)
        # -------------------------------------------------------------
        # Sample older memory slots from M and re-align them with current self-model
        with torch.no_grad():
            M = self.identity_engine.dnc_memory.memory
            random_slot_idx = random.randint(0, M.size(0) - 1)
            old_slot = M[random_slot_idx].clone()
            # Metacortex reframes old memory by soft scaling with certainty
            certainty = getattr(self.metacortex, "certainty", 0.75)
            reframed_slot = old_slot * float(certainty) + (1.0 - float(certainty)) * torch.randn_like(old_slot) * 0.05
            M[random_slot_idx].copy_(reframed_slot)

        # -------------------------------------------------------------
        # PHASE 6: SYNAPTIC PRUNING & LYAPUNOV DECAY
        # -------------------------------------------------------------
        # SVD Truncation + Lyapunov weight downscaling to prevent saturation
        svd_res = self.identity_engine.dream_and_consolidate(rank=16)

        # Apply soft Lyapunov weight decay (0.9995 factor)
        with torch.no_grad():
            for p in self.identity_engine.rnn_cell.parameters():
                p.data.mul_(0.9995)

        # -------------------------------------------------------------
        # PHASE 7: STM BUFFER FLUSH
        # -------------------------------------------------------------
        num_cleared = len(self.stm)
        self.stm.clear()
        self.total_sleep_cycles += 1
        self.total_experiences_consolidated += num_cleared
        self.last_sleep_timestamp = time.time()

        duration_sec = round(time.perf_counter() - t_start, 3)
        logger.info(
            "dream_cycle_completed",
            consolidated_count=num_cleared,
            counterfactuals=counterfactuals_evaluated,
            energy_preserved=svd_res.get("energy_preserved"),
            duration_s=duration_sec,
        )

        return {
            "status": "Consolidation Completed",
            "dream_state": "SVD_CONSOLIDATION_COMPLETE",
            "variance_explained": svd_res.get("variance_explained", svd_res.get("energy_preserved", 0.95)),
            "experiences_consolidated": num_cleared,
            "distorted_replays_synthesized": len(distorted_inputs),
            "counterfactuals_simulated": counterfactuals_evaluated,
            "svd_energy_preserved": svd_res.get("energy_preserved", 0.95),
            "total_sleep_cycles": self.total_sleep_cycles,
            "duration_seconds": duration_sec,
        }

    def get_dream_telemetry(self) -> Dict[str, Any]:
        """Provides state metrics for the dream and short-term memory buffers."""
        return {
            "stm_buffer_length": len(self.stm),
            "stm_max_capacity": self.max_stm_capacity,
            "dream_buffer_entropy": self.compute_dream_buffer_entropy(),
            "total_sleep_cycles": self.total_sleep_cycles,
            "total_experiences_consolidated": self.total_experiences_consolidated,
            "last_sleep_time_ago_sec": round(time.time() - self.last_sleep_timestamp, 1),
        }


dream_cycle_engine = OfflineDreamCycle()
