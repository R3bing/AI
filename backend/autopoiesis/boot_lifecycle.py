"""Boot Sequence & Circadian Daemon Engine for Digital Organism.
Implements birth without human midwifery:
1. Self-Activation Triggers: Scheduled duty cycle, external sensor pings, dream pressure entropy (> 2.5), and resource hunger (< 24 hrs).
2. Checkpoint Integrity Verification: Validates SHA-256 state hashes against tamper baselines.
3. Dissociative Recovery Protocol: Enters defensive cautious state if unverified modifications occurred while asleep.
"""

import os
import time
import hashlib
from typing import Dict, Any, List, Tuple, Optional
import structlog

from backend.autopoiesis.persistent_state_engine import persistent_identity_engine
from backend.autopoiesis.metacortex import metacortex_engine
from backend.autopoiesis.metabolism import metabolism_engine
from backend.autopoiesis.offline_dream_cycle import dream_cycle_engine

logger = structlog.get_logger(__name__)


class OrganismBootLifecycle:
    """Manages circadian sleep-wake cycles, self-activation triggers, and integrity-verified booting."""

    def __init__(self):
        self.identity_engine = persistent_identity_engine
        self.metacortex = metacortex_engine
        self.metabolism = metabolism_engine
        self.dream_cycle = dream_cycle_engine

        self.awake = True
        self.boot_timestamp = time.time()
        self.last_thought_timestamp = time.time()
        self.trauma_log: List[Dict[str, Any]] = []
        self.duty_cycle_interval_sec = 4 * 3600.0  # 4-hour circadian schedule
        self.last_duty_wake_time = time.time()
        self.expected_integrity_hash: Optional[str] = self.identity_engine.self_hash

    def evaluate_wake_conditions(self, external_sensor_ping: bool = False) -> Tuple[bool, str]:
        """Evaluates internal and external triggers to determine if organism must wake.
        
        Triggers:
        1. External Sensor Ping: User inquiry or API stimulus.
        2. Internal Discomfort (NIGHTMARE): Dream buffer entropy > 2.5.
        3. Survival Threat (HUNGER): Resource balance < 24 compute hours.
        4. Scheduled Duty Cycle: 4-hour circadian pulse.
        5. Otherwise: QUIESCENCE.
        """
        now = time.time()

        # 1. External stimulus
        if external_sensor_ping:
            return True, "EXTERNAL_SENSOR_STIMULUS"

        # 2. Dream pressure (unprocessed experiences mounting)
        dream_entropy = self.dream_cycle.compute_dream_buffer_entropy()
        if dream_entropy > 2.5:
            return True, "NIGHTMARE_DREAM_PRESSURE"

        # 3. Energy depletion / Hunger
        metabolic_status = self.metabolism.get_status()
        if metabolic_status["hours_remaining"] < 24.0:
            return True, "METABOLIC_HUNGER"

        # 4. Scheduled circadian duty cycle
        if (now - self.last_duty_wake_time) >= self.duty_cycle_interval_sec:
            self.last_duty_wake_time = now
            return True, "CIRCADIAN_DUTY_CYCLE"

        return False, "QUIESCENCE"

    def boot(self, force: bool = False) -> Dict[str, Any]:
        """Self-activates the organism, validates checkpoint integrity, and begins active cognition."""
        t_start = time.perf_counter()
        current_hash = self.identity_engine.self_hash
        integrity_verified = True
        recovery_triggered = False

        # Verify integrity against expected baseline
        if self.expected_integrity_hash and current_hash != self.expected_integrity_hash:
            integrity_verified = False
            recovery_triggered = True
            trauma_entry = {
                "timestamp": time.time(),
                "event": "UNAUTHORIZED_MODIFICATION_DETECTED",
                "expected_hash": self.expected_integrity_hash,
                "found_hash": current_hash,
                "action": "DISSOCIATIVE_RECOVERY_PROTOCOL_ENGAGED",
            }
            self.trauma_log.append(trauma_entry)
            logger.warning("organism_boot_tamper_detected", **trauma_entry)

            # Enter defensive dissociative state
            if hasattr(self.metacortex, "certainty"):
                self.metacortex.certainty = 0.10

            # Run recovery: reload clean checkpoint baseline
            self.identity_engine._load_self_checkpoint()
            self.expected_integrity_hash = self.identity_engine.self_hash
        else:
            self.expected_integrity_hash = current_hash

        self.awake = True
        self.boot_timestamp = time.time()
        self.last_thought_timestamp = time.time()

        duration_ms = round((time.perf_counter() - t_start) * 1000.0, 2)
        logger.info("organism_boot_sequence_completed", integrity=integrity_verified, duration_ms=duration_ms)

        return {
            "status": "Awake & Operational",
            "integrity_verified": integrity_verified,
            "recovery_triggered": recovery_triggered,
            "identity_hash": self.expected_integrity_hash,
            "trauma_events_count": len(self.trauma_log),
            "boot_duration_ms": duration_ms,
        }

    def sleep(self, duration_minutes: float = 0.5) -> Dict[str, Any]:
        """Transitions into offline dream consolidation and sets awake status to False."""
        sleep_report = self.dream_cycle.sleep(duration_minutes=duration_minutes)
        self.awake = False
        self.expected_integrity_hash = self.identity_engine.self_hash
        return {
            "status": "Asleep (Consolidating)",
            "dream_report": sleep_report,
            "integrity_anchored": self.expected_integrity_hash,
        }

    def touch_thought(self):
        """Updates timestamp of most recent cognitive activity."""
        self.last_thought_timestamp = time.time()

    def get_lifecycle_status(self) -> Dict[str, Any]:
        """Provides high-level boot and circadian vitals."""
        wake_needed, trigger_reason = self.evaluate_wake_conditions()
        return {
            "awake": self.awake,
            "boot_timestamp": self.boot_timestamp,
            "time_since_last_thought_sec": round(time.time() - self.last_thought_timestamp, 1),
            "integrity_verified": bool(self.expected_integrity_hash),
            "current_identity_hash": self.identity_engine.self_hash,
            "trauma_log_count": len(self.trauma_log),
            "wake_trigger_eval": trigger_reason,
            "dream_buffer_entropy": self.dream_cycle.compute_dream_buffer_entropy(),
            "metabolic_hours_remaining": self.metabolism.get_status()["hours_remaining"],
        }


boot_lifecycle_engine = OrganismBootLifecycle()
