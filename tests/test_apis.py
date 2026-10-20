"""Unit tests for individual external API clients in QKW using mocks and live checks.
"""

import pytest
import responses
from backend.apis.wikipedia import WikipediaClient
from backend.apis.arxiv import ArxivClient
from backend.apis.hadith import HadithClient
from backend.apis.pubmed import PubMedClient
from backend.apis.quran import QuranClient


@pytest.mark.asyncio
async def test_hadith_curated_search():
    client = HadithClient()
    result = await client.search(query="intentions and deeds", limit=2)

    assert result.success is True
    assert len(result.citations) >= 1
    first = result.citations[0]
    assert "Bukhari" in first.title or "Hadith" in first.title
    assert "intentions" in first.snippet.lower()


@pytest.mark.asyncio
async def test_wikipedia_client_error_resilience():
    client = WikipediaClient()
    # Bad URL will gracefully return an error APIResult without crashing
    client.base_url = "https://invalid-non-existent-subdomain.wikipedia.org"
    result = await client.search(query="test", limit=1)

    assert result.success is False
    assert result.error is not None
    assert result.status_code != 200


@pytest.mark.asyncio
async def test_arxiv_xml_parsing(monkeypatch):
    client = ArxivClient()

    sample_atom_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <id>http://arxiv.org/abs/2301.00001v1</id>
        <title>Quantum QAOA for Graph Partitioning</title>
        <summary>We present a novel QAOA algorithm for multi-qubit systems.</summary>
        <author><name>Dr. Alice</name></author>
        <published>2023-01-01T00:00:00Z</published>
      </entry>
    </feed>
    """

    class MockResponse:
        status_code = 200
        text = sample_atom_xml
        def raise_for_status(self):
            pass

    async def mock_get(*args, **kwargs):
        return MockResponse()

    import httpx
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    citations = await client.fetch("quantum QAOA", limit=1)
    assert len(citations) == 1
    assert "Quantum QAOA" in citations[0].title
    assert "arxiv-2301.00001v1" == citations[0].source_id
