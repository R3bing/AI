"""Unit Tests for Functional Correlates of Consciousness & Dual-Tier Persistence.
Validates:
1. Attention Schema Theory (AST) & Attentional Entropy.
2. Self-Model Reflection ('What did I attend to? Why? Uncertainty?').
3. Higher-Order Thought (HOT) & Meta-Cognitive Epistemic Humility.
4. Global Workspace Theory (GWT) Competitive Ignition & Broadcast.
5. Predictive Processing & Active Inference Free Energy.
6. Integrated Information Theory (IIT Phi* Approximation).
7. Dual-Tier Persistence (Local SQLite + Offline Safe Fallback).
8. End-to-End Conscious Cycle Execution.
9. Plotly Consciousness Dashboard Figure Generation.
"""

import pytest
import plotly.graph_objects as go
from backend.consciousness.functional_consciousness import (
    functional_consciousness_engine,
    AttentionSchema,
    SelfModel,
    HigherOrderThoughtMetaCognition,
    GlobalWorkspace,
    PredictiveProcessingEngine,
    IntegratedInformationApproximator,
)
from backend.consciousness.persistence_manager import consciousness_persistence_manager
from frontend.visual_brain import build_consciousness_dashboard_figure


def test_attention_schema_theory():
    """Validates AST attention distribution and entropy calculations."""
    ast = AttentionSchema()
    schema = ast.compute_attention_schema(
        query="photosynthesis chlorophyll light reactions",
        active_apis=["arxiv", "pubmed", "pubchem"],
    )
    assert "attention_distribution" in schema
    assert "attentional_entropy" in schema
    assert 0.0 <= schema["attentional_entropy"] <= 1.0
    assert schema["focus_modality"] in ["Sharp Focal Concentration", "Broad Trans-Disciplinary Scan", "Balanced Salience Focus"]


def test_self_model_reflection():
    """Validates Self-Model reflection and reasoning trace generation."""
    sm = SelfModel()
    refl = sm.reflect(
        query="quantum entanglement in superconductors",
        answer="Superconducting qubits demonstrate high-fidelity entanglement.",
        attended_apis=["arxiv", "openalex"],
        confidence=0.94,
    )
    assert refl["confidence"] == 0.94
    assert refl["uncertainty"] == round(1.0 - 0.94, 3)
    assert "arxiv" in refl["attended_apis"]
    assert "quantum" in refl["self_reasoning"].lower() or "arxiv" in refl["self_reasoning"].lower()
    assert refl["epistemic_status"] == "HIGH_CONFIDENCE"


def test_higher_order_thought_meta_cognition():
    """Validates HOT calibration and epistemic humility triggers."""
    hot = HigherOrderThoughtMetaCognition()

    # Confident scenario
    eval_high = hot.evaluate_own_answer(
        query="what is water molecular weight?",
        answer="Water is approximately 18.015 g/mol.",
        confidence=0.95,
        citations_count=3,
    )
    assert eval_high["meta_verdict"] == "EPISTEMIC_GROUNDING_VERIFIED"
    assert eval_high["epistemic_humility_active"] is False

    # Low-confidence humility scenario (< 0.50)
    eval_low = hot.evaluate_own_answer(
        query="exact speculative quantum gravity graviton mass in unknown dimension",
        answer="Graviton mass is hypothesized to be vanishingly small.",
        confidence=0.35,
        citations_count=0,
    )
    assert eval_low["meta_verdict"] == "EPISTEMIC_HUMILITY_TRIGGERED"
    assert eval_low["epistemic_humility_active"] is True
    assert "Epistemic Self-Reflection Note" in eval_low["calibrated_answer"]


def test_global_workspace_ignition_and_broadcast():
    """Validates competitive ignition and broadcast mechanism."""
    gw = GlobalWorkspace()
    candidates = {
        "Module_Physics": {"salience": 0.70, "topic": "quantum"},
        "Module_Biology": {"salience": 0.95, "topic": "chlorophyll"},
        "Module_Ethics": {"salience": 0.60, "topic": "mizan"},
    }
    broadcast = gw.submit_and_broadcast("plant photosynthesis", candidates)
    assert broadcast["winning_coalition"] == "Module_Biology"
    assert broadcast["ignition_charge"] == 0.95
    assert broadcast["broadcast_status"] == "GLOBAL_IGNITION_ACTIVE"


def test_predictive_processing_and_active_inference():
    """Validates top-down prior expectation and prediction error."""
    pp = PredictiveProcessingEngine()
    pred_res = pp.compute_prediction_error(
        query="photosynthesis in thylakoids",
        retrieved_concepts=["p680", "calvin", "rubisco", "atp"],
    )
    assert 0.0 <= pred_res["prediction_error"] <= 1.0
    assert pred_res["free_energy_bound"] >= 0.0
    assert len(pred_res["confirmed_priors"]) > 0


def test_integrated_information_theory_phi_star():
    """Validates approximation of Tononi's Phi*."""
    iit = IntegratedInformationApproximator()
    phi_star = iit.approximate_phi_star(
        particle_prob=0.5,
        wave_prob=0.5,
        citations_count=10,
        council_turn_count=5,
    )
    assert phi_star > 1.5
    assert isinstance(phi_star, float)


def test_dual_tier_persistence_manager():
    """Validates local SQLite persistence and telemetry."""
    mgr = consciousness_persistence_manager
    receipt = mgr.save_reflection(
        query="test consciousness query",
        self_model={"confidence": 0.9, "uncertainty": 0.1},
        attention_schema={"entropy": 0.3},
        meta_cognition={"verdict": "VERIFIED"},
        phi_star=2.85,
        prediction_error=0.15,
    )
    assert receipt["saved_locally"] is True
    assert receipt["record_id"] is not None

    recent = mgr.get_recent_reflections(limit=5)
    assert len(recent) > 0
    assert recent[0]["query"] == "test consciousness query"

    telemetry = mgr.get_persistence_telemetry()
    assert "current_mode" in telemetry
    assert telemetry["total_local_records"] > 0


def test_end_to_end_conscious_cycle():
    """Validates the full conscious cognitive cycle."""
    cycle = functional_consciousness_engine.execute_conscious_cycle(
        query="how does chlorophyll absorb photons in photosynthesis?",
        raw_answer="Chlorophyll absorbs red and blue light, utilizing exciton coherence.",
        attended_apis=["arxiv", "pubmed"],
        citations_count=6,
        particle_prob=0.6,
        wave_prob=0.4,
        confidence=0.91,
    )
    assert "self_model_reflection" in cycle
    assert "attention_schema" in cycle
    assert "global_workspace_broadcast" in cycle
    assert "predictive_processing" in cycle
    assert "integrated_information_phi_star" in cycle
    assert "persistence_receipt" in cycle
    assert cycle["consciousness_telemetry"]["phi_star"] > 0.0


def test_consciousness_dashboard_figure():
    """Validates Plotly consciousness dashboard creation."""
    fig = build_consciousness_dashboard_figure()
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 4
    for trace in fig.data:
        assert trace.type == "indicator"
