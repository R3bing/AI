"""Unit tests for 3D Visualizers, Dual-Voice Dialectic, and DeepSeek synthesis traces."""

import pytest
from backend.quantum.bloch_sphere import create_bloch_sphere_figure
from backend.memory.graph_3d import create_3d_knowledge_graph_figure
from backend.synthesis.dual_voice import dual_voice_generator
from backend.synthesis.synthesizer import llm_synthesizer


def test_bloch_sphere_figure():
    fig = create_bloch_sphere_figure(
        particle_prob=0.7,
        wave_prob=0.3,
        entropy_score=0.45,
        dominant_state="Aql (Brain/Particle)",
    )
    assert fig is not None
    assert len(fig.data) >= 4  # Mesh, equator, z-axis, x/y-axes, statevector, tip


def test_3d_knowledge_graph_figure():
    test_graph = {
        "nodes": [
            {"id": "n1", "name": "Quantum Entanglement", "label": "Physics"},
            {"id": "n2", "name": "Wahdat al-Wujud", "label": "Philosophy"},
        ],
        "edges": [
            {"source": "n1", "relationship": "ANALOGOUS_TO", "target": "n2"}
        ],
    }
    fig = create_3d_knowledge_graph_figure(test_graph)
    assert fig is not None
    assert len(fig.data) >= 2  # Edges + Nodes


def test_dual_voice_dialogue_generation():
    query = "How does quantum superposition relate to spiritual unity?"
    aql_ans = "Quantum superposition describes states existing concurrently until measurement."
    qalb_ans = "Contemplation of unity reminds human consciousness of divine coherence."
    
    dialogue = dual_voice_generator.generate_dialogue(
        query=query,
        logical_answer=aql_ans,
        tafakkur_reflection=qalb_ans,
    )
    assert len(dialogue) == 6
    speakers = [d["speaker"] for d in dialogue]
    assert "Host (Quantum Synthesizer)" in speakers
    assert "Dr. Aql" in speakers
    assert "Shaykh Qalb" in speakers


def test_synthesizer_deepseek_reasoning_trace_attribute():
    assert hasattr(llm_synthesizer, "last_reasoning_trace")
    assert hasattr(llm_synthesizer, "last_provider_used")
