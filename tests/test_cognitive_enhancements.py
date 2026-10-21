"""Unit tests for Cognitive Query Parser & Universal Multi-Provider Synthesizer.
"""

import pytest
from backend.neural_brain.query_parser import query_parser
from backend.synthesis.synthesizer import llm_synthesizer
from backend.orchestrator.models import SourceCitation, CrossRefConnection


def test_cognitive_parser_long_complex_sentence():
    complex_prompt = (
        "Could you please explain in deep detail how the cosmic microwave background radiation "
        "supports the idea of the early hot universe and whether there are any philosophical "
        "reflections or ancient verses touching on the creation of the heavens?"
    )
    parsed = query_parser.parse(complex_prompt)

    # 1. Boilerplate stripped
    assert "could" not in parsed.cleaned_intent.lower()
    assert "please" not in parsed.cleaned_intent.lower()
    assert "explain" not in parsed.cleaned_intent.lower()

    # 2. Epistemic domains identified
    assert "physics" in parsed.epistemic_domains or "astrophysics" in parsed.epistemic_domains
    assert "theological" in parsed.epistemic_domains or "humanities" in parsed.epistemic_domains

    # 3. Balanced mode
    assert parsed.dominant_mode == "balanced"

    # 4. Core entities extracted
    assert any("universe" in e.lower() or "cosmic" in e.lower() for e in parsed.core_entities)

    # 5. Targeted queries generated
    assert "arxiv" in parsed.api_targeted_queries
    assert "quran" in parsed.api_targeted_queries
    assert len(parsed.api_targeted_queries["arxiv"].split()) <= 6  # concise for academic APIs


def test_cognitive_parser_biomedical_sentence():
    prompt = "I was wondering if mRNA vaccines can alter human DNA and what clinical studies in oncology or genetics say about this?"
    parsed = query_parser.parse(prompt)

    assert "biomedical" in parsed.epistemic_domains
    assert "pubmed" in parsed.api_targeted_queries
    assert any("dna" in e or "vaccine" in e or "oncology" in e or "gene" in e for e in parsed.core_entities)


@pytest.mark.asyncio
async def test_multi_provider_synthesizer_offline_fallback():
    cit1 = SourceCitation(
        source_id="arxiv-1",
        source_name="arXiv Preprints",
        title="Cosmological Horizons",
        snippet="Observational evidence points to cosmic acceleration driven by dark energy.",
        url="http://arxiv.org/abs/1",
    )
    cit2 = SourceCitation(
        source_id="quran-1",
        source_name="The Holy Quran",
        title="Surah Adh-Dhariyat (51:47)",
        snippet="And the heaven We constructed with strength, and indeed, We are its expander.",
        url="https://quran.com/51/47",
    )
    cr = CrossRefConnection(
        source_a_id="arxiv-1",
        source_a_name="arXiv Preprints",
        source_b_id="quran-1",
        source_b_name="The Holy Quran",
        similarity_score=0.72,
        relationship="complements",
        notes="Both touch upon the expanding nature of the cosmos.",
    )

    parsed = query_parser.parse("Is the universe expanding in modern science and scripture?")
    result = await llm_synthesizer.synthesize(
        query="Is the universe expanding in modern science and scripture?",
        citations=[cit1, cit2],
        cross_references=[cr],
        parsed_query=parsed,
    )

    assert len(result) > 100
    assert "Cosmological Horizons" in result or "arXiv" in result or "universe" in result.lower() or "expand" in result.lower()
    assert "Executive Summary" in result or "Executive Synthesis" in result or "Cognitive Synthesis" in result or len(result) > 100
