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
    if not result.success and ("timeout" in str(result.error).lower() or result.status_code == 500):
        pytest.skip("OpenAlex API transient network timeout")
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


def test_api_registry_expanded_to_21_repositories():
    from backend.apis.registry import registry
    api_ids = registry.list_api_ids()
    assert len(api_ids) == 21
    expected = [
        "wikipedia", "arxiv", "quran", "hadith", "pubmed", "nasa", "openalex", "pubchem",
        "google", "crossref", "openlibrary", "semanticscholar", "wikidata", "dbpedia",
        "worldbank", "openmeteo", "hackernews", "pypi", "osv", "bible", "gutendex"
    ]
    for exp in expected:
        assert exp in api_ids, f"Missing registered API client: {exp}"


@pytest.mark.asyncio
async def test_all_10_new_api_clients():
    from backend.apis.semanticscholar import SemanticScholarClient
    from backend.apis.wikidata import WikidataClient
    from backend.apis.dbpedia import DBpediaClient
    from backend.apis.worldbank import WorldBankClient
    from backend.apis.openmeteo import OpenMeteoClient
    from backend.apis.hackernews import HackerNewsClient
    from backend.apis.pypi import PyPIClient
    from backend.apis.osv import OSVClient
    from backend.apis.bible import BibleClient
    from backend.apis.gutendex import GutendexClient

    clients = [
        (SemanticScholarClient(), "quantum mechanics"),
        (WikidataClient(), "photosynthesis"),
        (DBpediaClient(), "chlorophyll"),
        (WorldBankClient(), "gdp economy"),
        (OpenMeteoClient(), "geneva weather"),
        (HackerNewsClient(), "quantum computing"),
        (PyPIClient(), "torch numpy"),
        (OSVClient(), "requests"),
        (BibleClient(), "creation light"),
        (GutendexClient(), "plato"),
    ]

    for client, q in clients:
        res = await client.search(q, limit=1)
        assert res.success is True, f"{client.api_id} search failed"
        assert len(res.citations) >= 1, f"{client.api_id} returned no citations"
        cit = res.citations[0]
        assert cit.title, f"{client.api_id} citation missing title"
        assert cit.snippet, f"{client.api_id} citation missing snippet"
        assert cit.url, f"{client.api_id} citation missing URL"


def test_retrieval_enhancer_deduplication_and_ranking():
    from backend.apis.retrieval_enhancer import retrieval_enhancer

    raw_citations = [
        {
            "title": "Quantum Exciton Coherence in Photosynthetic Systems",
            "source": "arxiv",
            "snippet": "Coherent energy transfer occurs in photosynthetic antennae with long-lived quantum coherence.",
            "url": "https://arxiv.org/abs/2001.0001",
            "doi": "10.1038/s41586-024-001",
        },
        {
            # Exact DOI duplicate from Crossref
            "title": "Quantum Exciton Coherence in Photosynthetic Systems (Journal Version)",
            "source": "crossref",
            "snippet": "Short summary",
            "url": "https://doi.org/10.1038/s41586-024-001",
            "doi": "10.1038/s41586-024-001",
        },
        {
            # Title near-duplicate
            "title": "Quantum Exciton Coherence in Photosynthetic Systems and Antennae",
            "source": "semanticscholar",
            "snippet": "Detailed analysis of FMO complex quantum exciton dynamics and energy transfer.",
            "url": "https://semanticscholar.org/paper/123",
            "doi": "",
        },
        {
            # Distinct citation
            "title": "Solar Energy Conversion by Natural Light-Harvesting Complexes",
            "source": "pubmed",
            "snippet": "Biochemical mechanisms of reaction center charge separation in purple bacteria.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/987654",
            "doi": "10.1016/j.cell.2023.01",
        },
    ]

    # Test deduplication
    deduped = retrieval_enhancer.deduplicate_citations(raw_citations)
    # The duplicate DOI and near-duplicate title should be merged/filtered out
    assert len(deduped) < len(raw_citations)
    assert len(deduped) == 2

    # Test re-ranking
    ranked = retrieval_enhancer.rank_and_score_citations(deduped, query="quantum exciton photosynthesis")
    assert len(ranked) == 2
    assert ranked[0]["composite_rank_score"] >= ranked[1]["composite_rank_score"]
    assert "composite_rank_score" in ranked[0]
