"""Integration tests for the Master Orchestrator Engine.
"""

import pytest
from backend.orchestrator.engine import orchestrator
from backend.orchestrator.models import QueryRequest


@pytest.mark.asyncio
async def test_orchestrator_execution_and_caching():
    req = QueryRequest(
        text="What are the benefits of cleanliness and intentions in actions?",
        use_quantum=True,
        force_apis=["hadith"],
        max_sources=2,
    )

    # First run (Cache Miss)
    response_1 = await orchestrator.execute_query(req)
    assert response_1.cached is False
    assert len(response_1.citations) >= 1
    assert response_1.synthesized_answer != ""
    assert response_1.total_latency_ms > 0

    # Second run (Cache Hit)
    response_2 = await orchestrator.execute_query(req)
    assert response_2.cached is True
    assert len(response_2.citations) >= 1
