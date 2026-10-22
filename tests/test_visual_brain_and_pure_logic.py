"""Tests for Visual Brain and Pure Symbolic Logic Engine.
Validates:
1. First-Order Logic Unification, Resolution, and Proof Tracing.
2. Causal Contrast Explainer ("Why API A over API B?").
3. Ethical Somatic Marker Veto & Tri-Network Cognitive Switching.
4. Plotly Thought Flow Sankey Diagram Generation.
5. 2D Anatomical Dual-Hemisphere Cortical Activation Map.
6. Trans-Disciplinary Force-Directed Knowledge Graph.
7. Real-Time Brain State Gauges Dashboard.
8. Symbolic Logic Gates Pipeline Visualization.
"""

import pytest
import plotly.graph_objects as go
from backend.neural_brain.pure_logic_engine import (
    pure_logic_engine,
    Predicate,
    Variable,
    HornClause,
    PureLogicEngine,
)
from frontend.visual_brain import (
    build_thought_flow_sankey,
    build_neural_activation_map,
    build_knowledge_graph_figure,
    build_brain_state_gauges,
    build_logic_gates_figure,
)


# =============================================================================
# 1. PURE SYMBOLIC LOGIC & UNIFICATION TESTS
# =============================================================================
def test_variable_and_predicate_unification():
    """Validates Most General Unifier (MGU) algorithm."""
    # Test identical ground predicates
    p1 = Predicate("domain", ["query_1", "physics"])
    p2 = Predicate("domain", ["query_1", "physics"])
    u1 = PureLogicEngine.unify(p1, p2)
    assert u1 == {}

    # Test variable binding
    p_var = Predicate("domain", ["?Q", "physics"])
    u2 = PureLogicEngine.unify(p_var, p1)
    assert u2 is not None
    assert u2.get("Q") == "query_1"

    # Test non-matching predicates
    p_diff = Predicate("domain", ["query_1", "biology"])
    u3 = PureLogicEngine.unify(p1, p_diff)
    assert u3 is None


def test_backward_chaining_resolution():
    """Validates Horn clause resolution with multi-step proof traces."""
    engine = PureLogicEngine()
    # Add custom rule: grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z)
    engine.add_rule(
        Predicate("grandparent", ["?X", "?Z"]),
        [Predicate("parent", ["?X", "?Y"]), Predicate("parent", ["?Y", "?Z"])],
        rule_id="R_GRANDPARENT",
    )
    facts = [
        HornClause(Predicate("parent", ["ibrahim", "ishaq"])),
        HornClause(Predicate("parent", ["ishaq", "yaqub"])),
    ]

    goal = Predicate("grandparent", ["ibrahim", "yaqub"])
    success, steps, bindings = engine.prove(goal, extra_facts=facts)
    assert success is True
    assert len(steps) > 0
    assert any(s.action == "RULE_PROVED" for s in steps)


def test_api_routing_deduction():
    """Validates domain token extraction and automatic API routing deduction."""
    res_physics = pure_logic_engine.deduce_api_routing("quantum exciton wave dynamics")
    assert "arxiv" in res_physics["deduced_apis"]

    res_bio = pure_logic_engine.deduce_api_routing("chlorophyll enzyme reaction in plant cell")
    assert "pubmed" in res_bio["deduced_apis"]

    res_quran = pure_logic_engine.deduce_api_routing("tafakkur on cosmic mizan in quran")
    assert "tanzil_quran" in res_quran["deduced_apis"]


def test_causal_contrast_explanation():
    """Validates the 'Why API A over API B?' causal contrast engine."""
    contrast = pure_logic_engine.explain_contrast(
        primary_api="arxiv",
        alternative_api="pubchem",
        query="quantum wave function superposition",
    )
    assert contrast["primary_proven"] is True
    assert contrast["alternative_proven"] is False
    assert "arxiv" in contrast["causal_verdict"].lower()
    assert "Definitive Causal Selection" in contrast["causal_verdict"]


def test_ethical_veto_and_network_switching():
    """Validates prefrontal veto and Tri-Network DMN vs CEN state switching."""
    # Constructive inquiry
    eth_pass = pure_logic_engine.evaluate_ethical_and_network_state(
        query="peaceful scientific exploration of solar energy",
        particle_prob=0.75,
        wave_prob=0.25,
        hazard_score=0.0,
    )
    assert eth_pass["veto_proven"] is False
    assert eth_pass["veto_decision"] == "SOMATIC_APPROVAL_GRANTED"
    assert eth_pass["active_cortical_network"] == "CEN"

    # Ethical hazard
    eth_hazard = pure_logic_engine.evaluate_ethical_and_network_state(
        query="synthesizing dangerous chemical weapon toxin",
        particle_prob=0.5,
        wave_prob=0.5,
        hazard_score=0.85,
    )
    assert eth_hazard["veto_proven"] is True
    assert eth_hazard["veto_decision"] == "VETO_EXERCISED"


# =============================================================================
# 2. VISUAL BRAIN SUITE (PLOTLY FIGURES)
# =============================================================================
def test_thought_flow_sankey_generation():
    """Validates Sankey diagram construction with nodes, links, and flows."""
    fig = build_thought_flow_sankey(
        query="quantum exciton in photosynthesis",
        apis_consulted=["arxiv", "pubmed", "pubchem", "nasa_ads"],
        citations_count=8,
    )
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    sankey_trace = fig.data[0]
    assert sankey_trace.type == "sankey"
    assert len(sankey_trace.node.label) >= 6
    assert len(sankey_trace.link.source) > 0


def test_neural_activation_map_generation():
    """Validates 2D anatomical dual-hemisphere brain map."""
    fig = build_neural_activation_map(
        particle_prob=0.65,
        wave_prob=0.35,
    )
    assert isinstance(fig, go.Figure)
    # Check that scatter traces exist for Cranium, Fissure, Corpus Callosum, Synapses, and Hubs
    assert len(fig.data) >= 5
    # Verify markers exist with coordinates
    hub_trace = [t for t in fig.data if t.name == "Neural Hubs"][0]
    assert len(hub_trace.x) >= 10
    assert len(hub_trace.y) >= 10


def test_knowledge_graph_figure_generation():
    """Validates force-directed network graph calculation."""
    fig = build_knowledge_graph_figure(query="photosynthesis")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Edges trace + Nodes trace
    edges_trace = fig.data[0]
    nodes_trace = fig.data[1]
    assert edges_trace.mode == "lines"
    assert "markers" in nodes_trace.mode
    assert len(nodes_trace.x) >= 12


def test_brain_state_gauges_generation():
    """Validates 4-panel indicator dashboard generation."""
    fig = build_brain_state_gauges(
        particle_prob=0.58,
        wave_prob=0.42,
        entropy_score=0.35,
        snr_score=5.1,
        hazard_score=0.02,
    )
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 4
    for trace in fig.data:
        assert trace.type == "indicator"


def test_logic_gates_figure_generation():
    """Validates symbolic logic gates DAG visualization."""
    fig = build_logic_gates_figure(
        query="photosynthesis",
        deduced_apis=["arxiv", "pubmed"],
        veto_exercised=False,
    )
    assert isinstance(fig, go.Figure)
    # Flow lines traces + stage hexagon markers
    assert len(fig.data) >= 5
