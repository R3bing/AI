"""Unit tests for the Operating System Layer:
Metabolism, Dream Replay Cycle, Social Mesh (Pheromones & Crossover), and Boot Sequence.
"""

import pytest
import numpy as np
import time

from backend.autopoiesis.metabolism import ComputeMetabolism
from backend.autopoiesis.offline_dream_cycle import OfflineDreamCycle
from backend.autopoiesis.social_mesh import SocialMeshEngine
from backend.autopoiesis.boot_lifecycle import OrganismBootLifecycle
from backend.autopoiesis.organism_orchestrator import autopoietic_organism


def test_metabolism_accounting_and_transitions():
    """Verify compute consumption, burn rate, and state transitions."""
    metabolism = ComputeMetabolism(initial_balance=1.0, low_energy_threshold=24.0, critical_threshold=6.0)
    status = metabolism.get_status()
    assert status["balance"] == 1.0

    # Record steps
    for _ in range(5):
        rec = metabolism.record_inference_step(query_length=100, sources_count=4)
        assert "cost" in rec
        assert "balance" in rec

    # Force low balance to trigger ANXIETY and HIBERNATION
    metabolism.balance = 0.05
    metabolism.burn_rate_per_hour = 0.01  # 5 hours remaining -> HIBERNATION
    rec = metabolism.record_inference_step(query_length=20, sources_count=1)
    assert rec["state"] == "HIBERNATION"

    # Replenish energy
    rep = metabolism.replenish_energy(amount=50.0)
    assert rep["affective_state"] == "NOMINAL"
    assert rep["new_balance"] > 50.0


def test_offline_dream_cycle_consolidation():
    """Verify STM buffering, dream entropy, and 6-phase consolidation."""
    dream_cycle = OfflineDreamCycle(max_stm_capacity=50)

    # Initially empty
    assert dream_cycle.compute_dream_buffer_entropy() >= 0.05

    # Push experiences
    for i in range(10):
        v = np.random.randn(32).astype(np.float32)
        dream_cycle.record_experience(
            query=f"Query {i}",
            sensory_vector=v,
            dominant_mode="Left Hemisphere Dominant (Aql)",
            prediction_error=0.2 + 0.1 * i,
            reward_valence=0.15,
        )

    assert len(dream_cycle.stm) == 10
    entropy = dream_cycle.compute_dream_buffer_entropy()
    assert entropy > 0.5

    # Execute sleep consolidation
    res = dream_cycle.sleep(duration_minutes=0.1, batch_size=8)
    assert res["status"] == "Consolidation Completed"
    assert res["experiences_consolidated"] == 10
    assert res["counterfactuals_simulated"] > 0
    assert len(dream_cycle.stm) == 0  # Short term wiped after transfer to LTM


def test_social_mesh_pheromones_and_crossover():
    """Verify pheromone deposit/sensing and genetic crossover mating."""
    social = SocialMeshEngine()

    # Deposit pheromone signal
    dep = social.pheromone_layer.deposit(
        source_id="inst_alpha",
        location_hash="TASK_QUANTUM_COSMOLOGY",
        gradient_signal=[0.1] * 16,
        confidence=0.9,
    )
    assert dep["status"] == "deposited"

    # Sense nearby signal
    sensed = social.pheromone_layer.sense(location_hash="TASK_QUANTUM_COSMOLOGY")
    assert sensed["signals_detected"] >= 1
    assert len(sensed["consensus_gradient"]) == 16
    assert sensed["confidence_aggregate"] >= 0.8

    # Test Mating Crossover
    parent_a = {
        "id": "Parent_A",
        "signature": [1.0, 0.5, 0.2, 0.8] * 4,
        "fitness": 0.88,
        "confidence": 0.90,
        "generation": 1,
    }
    parent_b = {
        "id": "Parent_B",
        "signature": [0.95, 0.48, 0.22, 0.78] * 4,
        "fitness": 0.82,
        "confidence": 0.85,
        "generation": 1,
    }

    mate_res = social.mate_crossover(parent_a, parent_b)
    assert mate_res["success"] is True
    cert = mate_res["certificate"]
    assert cert["compatibility_score"] >= 0.70
    assert cert["dominant_genetic_donor"] == "Parent_A"
    assert cert["generation"] == 2

    # Incompatible parent test
    parent_incompatible = {
        "id": "Alien_C",
        "signature": [-1.0, -0.5, -0.2, -0.8] * 4,
        "fitness": 0.50,
        "confidence": 0.50,
    }
    incompat_res = social.mate_crossover(parent_a, parent_incompatible)
    assert incompat_res["success"] is False
    assert "incompatibility" in incompat_res["reason"].lower()


def test_boot_lifecycle_and_wake_triggers():
    """Verify wake triggers, self-activation boot, and tamper detection."""
    boot = OrganismBootLifecycle()

    # Trigger with sensor ping
    wake, reason = boot.evaluate_wake_conditions(external_sensor_ping=True)
    assert wake is True
    assert reason == "EXTERNAL_SENSOR_STIMULUS"

    # Boot cleanly
    boot_res = boot.boot()
    assert boot_res["status"] == "Awake & Operational"
    assert boot_res["integrity_verified"] is True
    assert boot.awake is True

    # Sleep
    sleep_res = boot.sleep()
    assert sleep_res["status"] == "Asleep (Consolidating)"
    assert boot.awake is False


def test_organism_orchestrator_turn_with_os_layer():
    """Verify end-to-end turn execution incorporates metabolism and dream queue."""
    res = autopoietic_organism.process_turn(
        query="What is the operating system lifecycle of self-modifying agents?",
        dominant_mode="Equilibrium (Harmonious Dual)",
        entropy=0.52,
        latency_ms=10.0,
    )

    assert "metabolism_balance" in res
    assert "metabolism_state" in res
    assert "metabolism_hours_remaining" in res
    assert "dream_buffer_entropy" in res

    dashboard = autopoietic_organism.get_organism_dashboard()
    assert "metabolism" in dashboard
    assert "dream_cycle" in dashboard
    assert "lifecycle" in dashboard
    assert "social" in dashboard
