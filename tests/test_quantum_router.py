"""Unit tests for Quantum Router and QAOA QUBO optimization in QKW.
"""

import pytest
import numpy as np
from backend.quantum.qubo_formulator import QUBOFormulator
from backend.quantum.router import QAOARouter
from backend.quantum.grover_search import grover_search
from backend.quantum.vqe_simulator import vqe_simulator


def test_qubo_formulator_matrix():
    formulator = QUBOFormulator(relevance_weight=2.0, latency_weight=1.0, cardinality_penalty=2.0)
    apis_metadata = [
        {"id": "wikipedia", "domain_tags": ["general"], "avg_latency_ms": 150.0},
        {"id": "arxiv", "domain_tags": ["physics", "quantum"], "avg_latency_ms": 400.0},
        {"id": "pubmed", "domain_tags": ["medicine"], "avg_latency_ms": 300.0},
    ]
    Q, api_ids, rel_scores = formulator.build_qubo_matrix(
        query="quantum physics research",
        apis_metadata=apis_metadata,
        target_k=2,
    )

    assert Q.shape == (3, 3)
    assert len(api_ids) == 3
    assert "arxiv" in rel_scores
    assert rel_scores["arxiv"] > rel_scores["pubmed"]


def test_qaoa_router_execution():
    router = QAOARouter(p_steps=1)
    apis_metadata = [
        {"id": "wikipedia", "domain_tags": ["general"], "avg_latency_ms": 150.0},
        {"id": "arxiv", "domain_tags": ["quantum"], "avg_latency_ms": 400.0},
        {"id": "quran", "domain_tags": ["theology"], "avg_latency_ms": 200.0},
    ]
    selected, details = router.route_query(
        query="quantum entanglement",
        apis_metadata=apis_metadata,
        target_k=1,
    )

    assert len(selected) >= 1
    assert details.qubits_count == 3
    assert details.algorithm.startswith("QAOA")
    assert "arxiv" in selected or "wikipedia" in selected


def test_grover_search():
    items = [{"id": f"node_{i}", "name": f"item_{i}"} for i in range(8)]
    items[3]["name"] = "target_entity"

    res = grover_search.search(items, predicate_fn=lambda x: x["name"] == "target_entity")
    assert res["marked_count"] == 1
    assert res["grover_iterations"] >= 1
    assert res["total_items"] == 8


def test_vqe_simulation():
    res = vqe_simulator.simulate_ground_state(bond_distance=0.74)
    assert "vqe_ground_state_energy_hartree" in res
    assert res["absolute_error_hartree"] < 0.2  # VQE ansatz is close to FCI
