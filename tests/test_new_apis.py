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
