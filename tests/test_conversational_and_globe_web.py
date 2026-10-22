"""Tests for Sovereign Conversational AI Engine & 3D Neural Globe Web Visualizer."""

import pytest
from backend.neural_brain.neural_globe_web import (
    NEURAL_BLOCKS,
    NEURAL_PATHWAYS,
    create_neural_globe_web_figure,
)
from backend.neural_brain.conversational_ai import sovereign_conversational_ai


def test_neural_blocks_structure():
    assert len(NEURAL_BLOCKS) == 9
    for b_id, b_info in NEURAL_BLOCKS.items():
        assert "name" in b_info
        assert "math_formula" in b_info
        assert "tensor_shapes" in b_info
        assert "sub_nodes" in b_info
        assert len(b_info["sub_nodes"]) >= 3
        for sn in b_info["sub_nodes"]:
            assert "name" in sn
            assert "formula" in sn
            assert "telemetry" in sn


def test_neural_pathways_graph():
    assert len(NEURAL_PATHWAYS) >= 10
    block_ids = set(NEURAL_BLOCKS.keys())
    for path in NEURAL_PATHWAYS:
        assert path["source"] in block_ids
        assert path["target"] in block_ids
        assert "label" in path


def test_neural_globe_web_figure_generation():
    fig = create_neural_globe_web_figure(selected_block_id="B1_THALAMUS")
    assert fig is not None
    # Check that traces include wireframe lines and nodes
    assert len(fig.data) >= 5


def test_sovereign_conversational_ai_formatting():
    mock_brain_data = {
        "duality_state": {
            "dominant_state": "Equilibrium (Harmonious Dual)",
            "particle_probability": 0.55,
            "wave_probability": 0.45,
            "entropy_score": 0.52,
        },
        "logical_factual_answer": "Penicillin inhibits bacterial cell wall peptidoglycan cross-linking by binding to DD-transpeptidases.",
        "tafakkur_reflection": "Contemplation instills inner peace (Sakoon).",
        "harmonious_synthesis": "Harmonized synthesis between biomedical chemistry and sacred contemplation.",
        "apis_consulted": ["pubmed", "pubchem", "arxiv", "quran"],
        "citations": [
            {
                "title": "Beta-lactam Antibiotic Mechanisms",
                "source": "pubmed",
                "snippet": "Penicillin acylates the active site serine of transpeptidase.",
                "url": "https://pubmed.ncbi.nlm.nih.gov/123456",
                "doi": "10.1038/s41586-020-0001",
            }
        ],
        "tafakkur_details": {
            "theme": "Healing and Divine Mercy",
            "quranic_verse": "And when I am ill, it is He who heals me. (Surah Ash-Shu'ara 26:80)",
            "surah_reference": "Quran 26:80",
            "tafseer_insight": "Al-Razi explains that divine healing manifests through both natural biological remedies and inward spiritual serenity.",
            "prophetic_hadith": "There is no disease that Allah has sent down except that He has sent down its treatment.",
            "hadith_reference": "Sahih al-Bukhari 5678",
            "comparative_tradition": "Universal Stoic & Classical Philosophy",
            "comparative_scripture": "The physician treats, but nature heals.",
            "spiritual_psychology_insight": "Physical illness is an opportunity to reflect on bodily vulnerability and cultivate gratitude (Shukr).",
            "contemplative_questions": ["How do molecular remedies reflect the order in biological design?"],
            "disclaimer": "Non-fatwa contemplative guidance.",
        },
        "multi_ai_dialogue": {
            "dialogue_turns": [
                {"ai_name": "DeepSeek-R1", "role": "Logic", "avatar": "💭", "content": "Axiomatic proof valid."},
            ]
        },
        "reasoning_trace": "1. Analyzing beta-lactam core.\n2. Verifying enzyme kinetics.",
    }

    result = sovereign_conversational_ai.format_vigorous_conversation(
        query="Explain penicillin and divine healing",
        brain_data=mock_brain_data,
    )

    assert "markdown_text" in result
    text = result["markdown_text"]
    assert "Hey! Let's explore this together" in text or "Salam" in text
    assert "The Core Intuition" in text
    assert "The Research Papers Backing This" in text
    assert "The Cosmic & Contemplative Horizon" in text
    assert "Where Should We Travel Next" in text or "Next Step" in text
    assert len(result["citations"]) == 1

    # Test Hinglish vibe detection
    hinglish_result = sovereign_conversational_ai.format_vigorous_conversation(
        query="batao yaar penicillin kaise kaam karta hai",
        brain_data=mock_brain_data,
    )
    assert hinglish_result["vibe"] == "hinglish"
    assert "Chalo baat karte hain" in hinglish_result["markdown_text"]


def test_cosmic_web_engine_and_visualizer():
    from backend.neural_brain.cosmic_web_engine import cosmic_web_engine
    from frontend.cosmic_web_visualizer import create_cosmic_web_3d_figure

    # 1. Test long query decomposition
    long_q = "Explain the quantum exciton transfer in photosynthetic antennae, how it connects to cellular ATP production, and what space telescopes reveal about exoplanet biosignatures?"
    clauses = cosmic_web_engine.decompose_long_query(long_q)
    assert len(clauses) >= 2
    domains = [c["domain"] for c in clauses]
    assert any("Quantum" in d for d in domains)
    assert any("Bio" in d or "Cosmic" in d for d in domains)

    # 2. Test building the cosmic neural web
    mock_citations = [
        {"title": "Exciton Coherence in Photosystem", "source": "nature", "snippet": "Coherent energy transfer.", "url": "https://doi.org/10", "doi": "10.1038/s1"}
    ]
    mock_council = [
        {"speaker": "Gemini 2.5", "role": "Empiricist", "content": "Empirical evidence is conclusive.", "color": "#10b981"}
    ]
    cosmic_graph = cosmic_web_engine.build_cosmic_neural_web(
        query=long_q,
        citations=mock_citations,
        council_turns=mock_council,
        matched_apis=[{"name": "NASA Exoplanet Archive"}],
        duality_state={"particle_probability": 0.6},
    )

    assert "nodes" in cosmic_graph
    assert "filaments" in cosmic_graph
    assert "topology_meta" in cosmic_graph
    nodes = cosmic_graph["nodes"]
    assert "COSMIC_CORE" in nodes
    assert "CLUST_QUANTUM" in nodes
    assert "CLUST_BIO" in nodes
    assert "CLUST_COSMIC" in nodes
    assert "CLUST_SACRED" in nodes
    assert len(cosmic_graph["filaments"]) >= 15

    # 3. Test Hebbian learning
    learning_stats = cosmic_web_engine.learn_and_reinforce_synapses(cosmic_graph["filaments"], long_q)
    assert learning_stats["active_synapses_reinforced"] > 0
    assert learning_stats["total_learned_synapses"] > 0

    # 4. Test 3D Plotly Figure Generation
    fig = create_cosmic_web_3d_figure(cosmic_graph)
    assert fig is not None
    assert len(fig.data) >= 3  # Stars, filaments, nodes, halo
