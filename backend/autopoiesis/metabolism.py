"""Economic Metabolism & Resource Accounting Engine for Autonomous Organism.
Tracks compute consumption: FLOPs, memory footprint, token costs, and burn rate.
Dynamically modulates behavioral states: NOMINAL, ANXIETY, and HIBERNATION.
"""

import time
import os
try:
    import psutil
except ImportError:
    psutil = None

from typing import Dict, Any, List, Optional
import structlog

logger = structlog.get_logger(__name__)


class ComputeMetabolism:
    """Manages energy accounting, compute burn rate, and resource-driven behavior modulation."""

    COST_PER_MFLOP = 1e-7      # Cost per MegaFLOP in synthetic compute credits
    COST_PER_MB_HOUR = 2e-6    # Memory storage cost per megabyte-hour
    BASE_QUERY_COST = 0.005    # Base operational cost per query dispatch

    def __init__(self, initial_balance: float = 100.0, low_energy_threshold: float = 24.0, critical_threshold: float = 6.0):
        self.balance = float(initial_balance)
        self.initial_balance = float(initial_balance)
        self.burn_rate_per_hour = 0.05  # Default baseline burn rate (credits/hour)
        self.total_energy_consumed = 0.0
        self.low_energy_threshold = low_energy_threshold   # Hours remaining for ANXIETY
        self.critical_threshold = critical_threshold       # Hours remaining for HIBERNATION
        self.last_heartbeat_time = time.time()
        self.affective_state = "NOMINAL"  # NOMINAL | ANXIETY | HIBERNATION
        self.expenditure_log: List[Dict[str, Any]] = []

    def estimate_step_flops(self, seq_len: int = 128, hidden_dim: int = 64, layers: int = 4) -> float:
        """Approximates floating point operations for a forward-backward pass through recurrent/plastic layers."""
        # Standard transformer/RNN FLOP approximation: 2 * params * tokens
        params_approx = 4 * (hidden_dim * hidden_dim) * layers
        return float(2 * params_approx * seq_len)

    def record_inference_step(self, query_length: int = 50, sources_count: int = 4, latency_ms: float = 15.0) -> Dict[str, Any]:
        """Calculates consumption for a single cognitive turn and updates metabolic reserves."""
        now = time.time()
        time_delta_hours = max((now - self.last_heartbeat_time) / 3600.0, 1e-6)
        self.last_heartbeat_time = now

        # 1. Compute FLOP cost
        flops = self.estimate_step_flops(seq_len=max(query_length, 16))
        flop_cost = (flops / 1e6) * self.COST_PER_MFLOP

        # 2. Memory / Process footprint cost
        try:
            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / (1024 * 1024)
        except Exception:
            mem_mb = 128.0
        mem_cost = mem_mb * self.COST_PER_MB_HOUR * time_delta_hours

        # 3. Source retrieval dispatch cost
        source_cost = sources_count * self.BASE_QUERY_COST

        step_total = flop_cost + mem_cost + source_cost
        self.balance = max(self.balance - step_total, 0.0)
        self.total_energy_consumed += step_total

        # 4. Instantaneous burn rate smoothing (EMA)
        instant_rate = step_total / time_delta_hours if time_delta_hours > 0 else 0.05
        self.burn_rate_per_hour = 0.85 * self.burn_rate_per_hour + 0.15 * min(instant_rate, 5.0)

        # 5. Evaluate remaining lifespan
        hours_remaining = self.balance / max(self.burn_rate_per_hour, 1e-4)

        # 6. Modulate affective state
        if hours_remaining <= self.critical_threshold:
            self.affective_state = "HIBERNATION"
        elif hours_remaining <= self.low_energy_threshold:
            self.affective_state = "ANXIETY"
        else:
            self.affective_state = "NOMINAL"

        record = {
            "timestamp": now,
            "cost": round(step_total, 6),
            "balance": round(self.balance, 4),
            "hours_remaining": round(hours_remaining, 2),
            "state": self.affective_state,
        }
        self.expenditure_log.append(record)
        if len(self.expenditure_log) > 100:
            self.expenditure_log.pop(0)

        return record

    def replenish_energy(self, amount: float = 50.0) -> Dict[str, Any]:
        """Replenishes compute budget reserves (e.g., wallet recharge or grant)."""
        self.balance += float(amount)
        hours_remaining = self.balance / max(self.burn_rate_per_hour, 1e-4)
        if hours_remaining > self.low_energy_threshold:
            self.affective_state = "NOMINAL"
        elif hours_remaining > self.critical_threshold:
            self.affective_state = "ANXIETY"

        logger.info("metabolism_replenished", added=amount, new_balance=self.balance, state=self.affective_state)
        return {
            "replenished": amount,
            "new_balance": round(self.balance, 4),
            "hours_remaining": round(hours_remaining, 2),
            "affective_state": self.affective_state,
        }

    def get_status(self) -> Dict[str, Any]:
        """Provides full metabolic health status."""
        hours_remaining = self.balance / max(self.burn_rate_per_hour, 1e-4)
        return {
            "balance": round(self.balance, 4),
            "initial_balance": self.initial_balance,
            "burn_rate_per_hour": round(self.burn_rate_per_hour, 4),
            "hours_remaining": round(hours_remaining, 2),
            "total_energy_consumed": round(self.total_energy_consumed, 4),
            "affective_state": self.affective_state,
            "resource_conservation_mode": self.affective_state != "NOMINAL",
        }


metabolism_engine = ComputeMetabolism()
