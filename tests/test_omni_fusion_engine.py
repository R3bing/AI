"""Tests for Omni-Resource Instantaneous Fusion Engine."""

import pytest
from backend.synthesis.omni_fusion_engine import omni_fusion_engine


@pytest.mark.asyncio
async def test_omni_fusion_engine_execution():
    test_query = "How do quantum physics, biomedical pharmacology, and prophetic traditions approach universal balance?"
    res = await omni_fusion_engine.fuse_and_synthesize(query=test_query)

    assert res is not None
    assert "markdown_text" in res
    assert len(res["markdown_text"]) > 500
    assert "Empirical Scientific & Logical Grounding" in res["markdown_text"]
    assert "Sacred Horizon & Ontological Contemplation" in res["markdown_text"]
    assert "Multi-AI Council Majlis" in res["markdown_text"]

    # Check Cosmic Web Graph is produced
    assert "cosmic_web_graph" in res
    assert "nodes" in res["cosmic_web_graph"]
    assert "filaments" in res["cosmic_web_graph"]

    # Check that multiple repositories were merged
    assert "apis_consulted" in res
    assert len(res["apis_consulted"]) >= 1

    # Check quantum and duality states
    assert "duality_state" in res
    assert "quantum_telemetry" in res

    # Check that continuous learning occurred
    assert "learning_stats" in res
    assert res["learning_stats"]["status"] == "auto_trained_successfully"
