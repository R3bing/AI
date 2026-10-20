"""Unit tests for the Academic Benchmark Engine comparing QAOA vs classical baselines.
"""

from backend.evaluation.benchmark import benchmark_engine


def test_academic_benchmark():
    res = benchmark_engine.run_benchmark(query="quantum entanglement and black holes", target_k=2)

    assert res["qubits_n"] >= 8  # 8 registered APIs
    assert "exact_global_optimum" in res
    assert "classical_greedy" in res
    assert "classical_simulated_annealing" in res
    assert "qaoa_xy_mixer" in res

    qaoa = res["qaoa_xy_mixer"]
    assert qaoa["approximation_ratio"] > 0.0
    assert len(qaoa["selected_apis"]) == 2  # XY mixer preserved target_k exactly!
