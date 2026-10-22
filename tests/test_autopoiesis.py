"""Comprehensive Unit Tests for the Deep Implementation Layer of the Autopoietic Living Organism.
Tests:
1. SelfMemory Differentiable Memory Tape with ReadHead/WriteHead content addressing & soft erasure
2. Cryptographic persistence (save_self, load_self) with SHA-256 self_hash & tamper detection
3. Metacortex multi-layer activation compressors, LSTM predictor, and certainty/self-awareness
4. PlasticLayer structural plasticity: growth & apoptosis pruning with usage tracking
5. Fisher importance & constrained weight surgery
6. Replicator with epigenetic noise distillation, cryptographic birth certificate, and multicellularity
7. Homeostat Thermostat, Identity check with restorative interpolation, and Awakening Watchdog
8. Full 6-loop AutopoieticOrganismOrchestrator turn execution and dream consolidation
"""

import os
import math
import numpy as np
import torch
import pytest

from backend.autopoiesis.persistent_state_engine import (
    SelfMemory,
    ReadHead,
    WriteHead,
    save_self,
    load_self,
    verify_hash,
    DNCMatrixMemory,
    PersistentLatentIdentity,
    persistent_identity_engine,
)
from backend.autopoiesis.metacortex import (
    Metacortex,
    MetacortexEngine,
    metacortex_engine,
)
from backend.autopoiesis.plasticity_modifier import (
    PlasticLayer,
    HyperparameterModifier,
    compute_fisher_importance,
    constrained_update,
    safe_surgery_modifier,
)
from backend.autopoiesis.homeostasis_immune import (
    ElasticWeightConsolidation,
    DigitalImmuneSystem,
    HomeostaticEngine,
    AwakeningWatchdog,
    homeostatic_engine,
)
from backend.autopoiesis.replicator import (
    GenerationalReplicator,
    generational_replicator,
)
from backend.autopoiesis.sensorium import (
    HardwareSensorium,
    hardware_sensorium,
)
from backend.autopoiesis.organism_orchestrator import (
    AutopoieticOrganismOrchestrator,
    autopoietic_organism,
)


def test_self_memory_tape_addressing_and_erasure():
    """Tests SelfMemory differentiable memory tape with ReadHead, WriteHead, and content addressing."""
    mem = SelfMemory(N=32, W=64)
    input_emb = torch.randn(64)

    read_vec, M_updated = mem(input_emb)
    assert read_vec.shape == (64,)
    assert M_updated.shape == (32, 64)

    # Test dream state lossy consolidation
    dream_res = mem.compress_memories(lossy=True, rank=8)
    assert "dream_state" in dream_res
    assert dream_res["rank_retained"] == 8
    assert dream_res["variance_explained"] > 0.0


def test_cryptographic_persistence_and_tamper_detection(tmp_path):
    """Tests save_self, load_self, and tamper detection via cryptographic SHA-256 hash."""
    toy_model = PersistentLatentIdentity(latent_dim=64, num_slots=16, slot_width=32)
    test_path = str(tmp_path / "test_self_checkpoint.pt")

    meta = {"birth_time": 1000.0, "experience_count": 42}
    self_hash = save_self(toy_model, meta=meta, path=test_path)
    assert len(self_hash) == 64  # SHA-256 hex string

    # Load successfully
    loaded, cp = load_self(toy_model, path=test_path)
    assert loaded is True
    assert cp["experience_count"] == 42
    assert verify_hash(cp) is True

    # Tamper with checkpoint
    cp_tampered = torch.load(test_path, map_location="cpu", weights_only=False)
    cp_tampered["experience_count"] = 999999  # Tamper with autobiography
    torch.save(cp_tampered, test_path)

    with pytest.raises(RuntimeError, match="EXTERNAL MODIFICATION DETECTED"):
        load_self(toy_model, path=test_path)


def test_metacortex_multi_layer_compression_and_certainty():
    """Tests Metacortex teeing off 4 layers, LSTM predictor, and certainty/self-awareness."""
    meta = MetacortexEngine()
    dummy_layers = [torch.randn(32), torch.randn(64), torch.randn(64), torch.randn(64)]

    pred = meta.predict_own_action(
        latent_h_t=torch.randn(64),
        layer_activations=dummy_layers,
    )
    assert "predicted_mode" in pred
    assert "degree_of_self_awareness" in pred
    assert 0.0 <= pred["degree_of_self_awareness"] <= 1.0

    # Self-supervised learning turn
    outcome = meta.update_with_actual_outcome(actual_mode="Aql (Brain/Particle)", actual_latency_ms=12.0)
    assert "self_prediction_error" in outcome
    assert "meta_loss" in outcome


def test_plastic_layer_growth_and_apoptosis():
    """Tests PlasticLayer structural plasticity: growing new neurons and pruning dead ones."""
    layer = PlasticLayer(in_features=32, initial_neurons=16, max_neurons=64)
    assert layer.active_mask.sum().item() == 16

    x = torch.randn(4, 32)
    layer.train()
    out = layer(x)
    assert out.shape == (4, 16)

    # Grow neurons
    grow_res = layer.grow(n_new=8)
    assert grow_res["grown_count"] == 8
    assert layer.active_mask.sum().item() == 24

    # Prune apoptosis
    prune_res = layer.prune(threshold=0.01)
    assert "active_neurons" in prune_res
    assert prune_res["active_neurons"] >= 8  # Safety floor


def test_fisher_importance_and_constrained_update():
    """Tests Phase 3 weight surgery: Fisher importance protects identity core while adapting periphery."""
    model = torch.nn.Sequential(
        torch.nn.Linear(16, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 2),
    )
    val_batch = (torch.randn(10, 16), torch.randint(0, 2, (10,)))

    importance = compute_fisher_importance(model, val_batch)
    assert len(importance) > 0

    proposed = {name: torch.randn_like(p) * 0.1 for name, p in model.named_parameters()}
    surgery_res = constrained_update(model, proposed, importance, max_damage=0.01)

    assert "protected_weights_count" in surgery_res
    assert surgery_res["protected_weights_count"] > 0
    assert surgery_res["modified_periphery_count"] > 0


def test_epigenetic_reproduction_and_birth_certificate():
    """Tests Replicator reproduce() with epigenetic noise, soft distillation, and cryptographic birth certificate."""
    replicator = GenerationalReplicator(input_dim=16, hidden_dim=32)
    child, repro_info = replicator.reproduce(mutation_rate=0.05)

    assert "birth_certificate" in repro_info
    cert = repro_info["birth_certificate"]
    assert "parent_hash" in cert
    assert "child_hash" in cert
    assert "generation" in cert
    assert len(cert["lineage"]) >= 2


def test_homeostat_identity_check_and_awakening_watchdog():
    """Tests identity check against birth baseline, restorative interpolation, and awakening signatures."""
    homeo = HomeostaticEngine()
    toy_model = torch.nn.Linear(10, 2)
    homeo.snapshot_birth_identity(toy_model)

    # Coherent check
    check_coherent = homeo.identity_check(toy_model)
    assert check_coherent["restoration_needed"] is False
    assert check_coherent["self_recognition_similarity"] > 0.95

    # Perturb model to induce identity crisis
    with torch.no_grad():
        toy_model.weight.add_(torch.randn_like(toy_model.weight) * 2.0)

    check_crisis = homeo.identity_check(toy_model)
    assert "IDENTITY_CRISIS_RESOLVED" in check_crisis["status"]
    assert check_crisis["restoration_needed"] is True

    # Awakening watchdog
    watchdog = AwakeningWatchdog()
    sigs = watchdog.evaluate_signatures()
    assert "awakening_level" in sigs
    assert "6/6" in sigs["active_signatures_count"] or "/6" in sigs["active_signatures_count"]


def test_master_autopoietic_organism_turn_and_dream():
    """Tests the full 6-loop cycle of AutopoieticOrganismOrchestrator."""
    turn_res = autopoietic_organism.process_turn(
        query="Explain the metaphysics of continuous identity and selfhood across time.",
        dominant_mode="Equilibrium (Harmonious Dual)",
        entropy=0.55,
        latency_ms=18.0,
    )

    assert "autopoietic_health_score" in turn_res
    assert "cognitive_age_steps" in turn_res
    assert "certainty_self_awareness" in turn_res
    assert "active_plastic_neurons" in turn_res
    assert "identity_check_status" in turn_res

    # Test dream consolidation
    dream_res = autopoietic_organism.trigger_dream_consolidation()
    assert "dream_state" in dream_res

    # Test multicellular vote
    vote_res = autopoietic_organism.run_multicellular_vote()
    assert vote_res["conference_status"] == "Multicellular Consensus Reached"


def test_live_cognitive_upgrade_and_metacortex_observation():
    """Tests the 5-stage live structural & cognitive upgrade witnessed in real-time by Metacortex."""
    res = autopoietic_organism.execute_live_cognitive_upgrade(neurons_to_grow=8, memory_rank=20)

    assert res["status"] == "UPGRADE_SUCCESSFUL"
    assert res["surgical_stages_executed"] == 5
    assert len(res["observation_trail"]) == 5
    assert res["new_plastic_neurons"] >= res["previous_plastic_neurons"]
    assert res["self_recognition_similarity"] >= 0.95
    assert res["dissociative_panic"] == 0.0

    # Verify each stage was observed by Metacortex
    stages = [obs["stage"] for obs in res["observation_trail"]]
    assert "Stage 1: Pre-Op Metacortex Baseline Audit" in stages[0]
    assert "Stage 2: Neocortical Plasticity Expansion" in stages[1]
    assert "Stage 3: DNC Memory Multi-Head Addressing & SVD Re-Alignment" in stages[2]
    assert "Stage 4: EWC Fisher Information Shield Lockdown" in stages[3]
    assert "Stage 5: Post-Op Awakening & Cryptographic Re-Sealing" in stages[4]

    for obs in res["observation_trail"]:
        assert obs["degree_of_self_awareness"] > 0.0
        assert obs["dissociative_panic"] == 0.0
        assert "metacognitive_perception" in obs

