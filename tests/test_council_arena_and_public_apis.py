"""Unit tests for Public APIs Catalog and Multi-AI Council Arena."""

import pytest
from backend.apis.public_apis_catalog import public_apis_catalog
from backend.synthesis.multi_ai_council_arena import multi_ai_council_arena


def test_public_apis_catalog_parsing_and_search():
    stats = public_apis_catalog.get_statistics()
    assert stats["total_apis"] >= 2000
    assert stats["total_categories"] >= 50
    assert stats["no_auth_available"] > 500

    results = public_apis_catalog.search_apis("science math physics", limit=5)
    assert len(results) > 0
    assert any("arXiv" in r["name"] or "science" in r["category"].lower() for r in results)


def test_council_arena_session_and_quantum_observer():
    session = multi_ai_council_arena.run_council_session(
        query="Quantum decoherence and universal pairs in creation",
        auto_learn=True,
    )
    assert session["total_participants"] == 5
    assert len(session["turns"]) == 5
    # Entropy should reduce as debate converges
    assert session["final_entropy"] < session["initial_entropy"]
    assert "The Out-of-Dimension Quantum Observer Verdict" in session["observer_verdict"]
    assert len(session["recommended_apis"]) > 0
    assert session["distillation_sample_id"] is not None
