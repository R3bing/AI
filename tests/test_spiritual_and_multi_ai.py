"""Unit tests for Ontological & Spiritual Equilibrium Engine and Multi-AI Inter-Dialogue Council."""

import pytest
from backend.neural_brain.ontological_spiritual_engine import ontological_spiritual_engine
from backend.synthesis.multi_ai_dialogue import multi_ai_dialogue


def test_ontological_spiritual_engine_quantum_theme():
    """Verify that quantum/physics queries match cosmic signs and Quran/Gita resonance."""
    res = ontological_spiritual_engine.match_resonance("quantum superposition and cosmic stars")
    assert "signs" in res["quranic_verse"].lower() or "horizons" in res["quranic_verse"].lower()
    assert "41:53" in res["surah_reference"]
    assert "Ibn Kathir" in res["tafseer_scholarly_insight"]
    assert "Bhagavad Gita" in res["comparative_tradition"]
    assert len(res["contemplative_questions"]) == 3
    assert res["confidence_score"] >= 0.7


def test_ontological_spiritual_engine_anxiety_theme():
    """Verify that hardship/pain queries match ease verses and Psalm/Sakoon resonance."""
    res = ontological_spiritual_engine.match_resonance("severe anxiety, stress and emotional pain")
    assert "ease" in res["quranic_verse"].lower()
    assert "94:5-6" in res["surah_reference"]
    assert "Al-Jalalayn" in res["tafseer_scholarly_insight"]
    assert "Psalms" in res["comparative_tradition"] or "Zabur" in res["comparative_tradition"]
    assert "Bukhari" in res["hadith_reference"]
    assert len(res["contemplative_questions"]) == 3


def test_ontological_spiritual_engine_purpose_and_wu_wei():
    """Verify purpose and balance themes."""
    res_purpose = ontological_spiritual_engine.match_resonance("what is the true purpose and ethical intention of life")
    assert "67:2" in res_purpose["surah_reference"]
    assert "Nishkama Karma" in res_purpose["comparative_tradition"]

    res_balance = ontological_spiritual_engine.match_resonance("inner peace, breath, meditation and equilibrium")
    assert "Balance" in res_balance["quranic_verse"] or "55:7-8" in res_balance["surah_reference"]
    assert "Tao Te Ching" in res_balance["comparative_tradition"]


@pytest.mark.asyncio
async def test_multi_ai_dialogue_execution():
    """Verify that the 4-phase Inter-AI dialogue executes and returns structured consensus."""
    query = "What is the nature of consciousness across quantum physics and ontology?"
    res = await multi_ai_dialogue.run_inter_ai_dialogue(query=query)

    assert "gemini_output" in res and res["gemini_output"]
    assert "deepseek_output" in res and res["deepseek_output"]
    assert "deepseek_reasoning" in res and res["deepseek_reasoning"]
    assert "groq_output" in res and res["groq_output"]
    assert "consensus" in res and "Multi-AI" in res["consensus"]

    turns = res["dialogue_turns"]
    assert len(turns) == 4
    ai_names = [t["ai_name"] for t in turns]
    assert "Google Gemini 2.5" in ai_names
    assert "DeepSeek-R1" in ai_names
    assert "Groq LPU (120B)" in ai_names
    assert "QKW Quantum Arbitrator" in ai_names
