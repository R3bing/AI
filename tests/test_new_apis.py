"""Unit tests for newly integrated knowledge APIs: NASA, OpenAlex, and PubChem.
"""

import pytest
from backend.apis.nasa import NasaClient
from backend.apis.openalex import OpenAlexClient
from backend.apis.pubchem import PubChemClient


@pytest.mark.asyncio
async def test_nasa_client():
    client = NasaClient()
    result = await client.search("hubble", limit=1)
    assert result.success is True
    assert len(result.citations) >= 1
    assert "NASA" in result.citations[0].source_name


@pytest.mark.asyncio
async def test_openalex_client():
    client = OpenAlexClient()
    result = await client.search("quantum computing", limit=1)
    assert result.success is True
    assert len(result.citations) >= 1
    assert "openalex" in result.citations[0].source_id


@pytest.mark.asyncio
async def test_pubchem_client():
    client = PubChemClient()
    result = await client.search("aspirin", limit=1)
    assert result.success is True
    assert len(result.citations) >= 1
    assert "CID" in result.citations[0].title or "aspirin" in result.citations[0].snippet.lower()


@pytest.mark.asyncio
async def test_google_data_client():
    from backend.apis.google_data import GoogleDataClient
    client = GoogleDataClient()
    result = await client.search("quantum physics", limit=1)
    assert result.success is True
    assert len(result.citations) >= 1
    assert result.citations[0].source_id == "google"
    assert "Google" in result.citations[0].source_name


@pytest.mark.asyncio
async def test_crossref_client():
    from backend.apis.crossref import CrossrefClient
    client = CrossrefClient()
    result = await client.search("quantum mechanics", limit=1)
    assert result.success is True
    assert len(result.citations) >= 1
    assert result.citations[0].source_id == "crossref"
    assert "10." in result.citations[0].url or "doi" in result.citations[0].url.lower()


@pytest.mark.asyncio
async def test_openlibrary_client():
    from backend.apis.openlibrary import OpenLibraryClient
    client = OpenLibraryClient()
    result = await client.search("physics", limit=1)
    assert result.success is True
    assert len(result.citations) >= 1
    assert result.citations[0].source_id == "openlibrary"


def test_antigravity_mimic_verdict():
    from backend.neural_brain.antigravity_mimic import antigravity_mimic
    from backend.neural_brain.models import DualityState
    from backend.orchestrator.models import SourceCitation

    duality = DualityState(
        particle_amplitude_alpha=0.707,
        wave_amplitude_beta=0.707,
        particle_probability=0.5,
        wave_probability=0.5,
        dominant_state="Equilibrium (Harmonious Dual)",
        entropy_score=0.9,
    )
    citations = [
        SourceCitation(source_id="google", source_name="Google Knowledge & News", title="Quantum Discoveries", snippet="Sample snippet"),
        SourceCitation(source_id="quran", source_name="Noble Quran", title="Surah Al-Hadid", snippet="Iron sent down"),
    ]
    tafakkur = {
        "quranic_verse": "And He is with you wherever you are (57:4)",
        "prophetic_hadith": "Actions are by intentions.",
        "spiritual_psychology_insight": "Inner tranquility through contemplation.",
        "contemplative_questions": ["What is true presence?", "How do parts unite?"],
        "disclaimer": "Academic reflection",
    }

    verdict, insights = antigravity_mimic.generate_verdict(
        query="What is quantum entanglement and unity?",
        duality=duality,
        citations=citations,
        cross_references=[],
        tafakkur_data=tafakkur,
    )

    assert "Antigravity Meta-Cognitive Verdict" in verdict
    assert "First-Principles" in verdict
    assert "first_principles" in insights
    assert "frontier_boundary" in insights
