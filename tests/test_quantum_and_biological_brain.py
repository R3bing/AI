"""Comprehensive Test Suite for Phase 2 (Quantum QAOA, ZNE, VQE, Kernel)
and Phase 3 (Biological Brain Circuitry, Maqamat al-Qalb, CRAG, Universe KG).
"""

import pytest
import numpy as np
import asyncio

from backend.quantum.router import quantum_router
from backend.quantum.physical_qpu_emulator import physical_qpu_emulator
from backend.quantum.vqe_molecular_engine import vqe_molecular_engine
from backend.quantum.quantum_kernel import quantum_kernel_engine
from backend.neural_brain.biological_brain_circuitry import biological_brain
from backend.neural_brain.ontological_spiritual_engine import ontological_spiritual_engine
from backend.cross_reference.hyde_crag_engine import hyde_generator, crag_evaluator
from backend.memory.universe_knowledge_graph import universe_knowledge_graph
from backend.neural_brain.engine import neural_brain
from backend.orchestrator.models import SourceCitation


def test_qaoa_cvar_and_circuit_exporters():
    """Validates QAOA with CVaR objective, Google Cirq, and AWS Braket OpenQASM export."""
    Q = np.array([
        [-1.2, 0.4, 0.0],
        [0.4, -0.9, 0.3],
        [0.0, 0.3, -1.5],
    ])
    # 1. QAOA optimization with CVaR alpha=0.25
    gamma, beta, std_energy, cvar_energy = quantum_router.optimize_qaoa(
        Q, target_k=2, p=1, mixer_type="xy_mixer", cvar_alpha=0.25
    )
    assert len(gamma) == 1
    assert len(beta) == 1
    assert cvar_energy <= std_energy + 1e-5  # CVaR focuses on lowest tail

    # 2. Google Cirq export
    cirq_circuit = quantum_router.to_cirq_circuit(Q, gamma, beta)
    assert cirq_circuit is not None
    assert len(list(cirq_circuit.all_qubits())) == 3

    # 3. AWS Braket OpenQASM 3.0 export
    qasm_str = quantum_router.to_braket_openqasm(Q, gamma, beta)
    assert "OPENQASM 3.0;" in qasm_str
    assert "qubit[3] q;" in qasm_str
    assert "measure" in qasm_str


def test_physical_qpu_noise_and_zne():
    """Validates physical IBM QPU noise emulation and Richardson ZNE mitigation."""
    ideal_probs = {"110": 0.60, "101": 0.30, "011": 0.10}
    noisy_probs, telemetry = physical_qpu_emulator.apply_physical_noise(
        ideal_probabilities=ideal_probs,
        num_qubits=3,
        p_layers=1,
        shots=512,
    )
    assert "quantum_state_fidelity" in telemetry
    assert "zne_mitigated_fidelity" in telemetry
    assert telemetry["zne_mitigated_fidelity"] >= telemetry["quantum_state_fidelity"]
    assert "ibm_brisbane" in telemetry["physical_qpu"]


def test_vqe_molecular_engine():
    """Validates VQE molecular ground state calculation for H2 and CO2."""
    # 1. H2 Molecule
    h2_res = vqe_molecular_engine.solve_ground_state("H2", bond_distance=0.74, max_iter=60)
    assert h2_res["molecule"] == "H2"
    assert h2_res["qubits_used"] == 2
    assert h2_res["vqe_ground_state_hartree"] < -1.0
    assert "zne_mitigated_energy_hartree" in h2_res

    # 2. CO2 Photosynthesis molecule
    co2_res = vqe_molecular_engine.solve_ground_state("CO2", max_iter=30)
    assert co2_res["molecule"] == "CO2"
    assert co2_res["qubits_used"] == 4
    assert co2_res["vqe_ground_state_hartree"] < -30.0


def test_quantum_kernel_similarity():
    """Validates non-linear semantic cross-referencing via ZZFeatureMap quantum kernel."""
    citations = [
        {"source_id": "arxiv", "title": "Quantum Exciton Coherence", "snippet": "Energy transfer in photosynthetic systems"},
        {"source_id": "pubmed", "title": "Cellular Respiration in Chloroplasts", "snippet": "Biochemical phosphorylation pathways"},
    ]
    results = quantum_kernel_engine.cross_reference_quantum_kernel("photosynthesis mechanism", citations)
    assert len(results) == 2
    for r in results:
        assert 0.0 <= r["quantum_kernel_fidelity"] <= 1.0
        assert "quantum_advantage_delta" in r
        assert r["hilbert_space_dimension"] == 16


def test_biological_brain_circuitry():
    """Validates the 4 biological brain loops: Thalamus, Somatic Governor, Hippocampus, Tri-Network."""
    # 1. Analytical query -> CEN activation
    res_cen = biological_brain.process_cognitive_cycle(
        "derive the quantum hamiltonian eigenvalue for carbon fixation",
        particle_prob=0.85,
        wave_prob=0.15,
    )
    thalamus = res_cen["thalamocortical_salience_gate"]
    assert thalamus["sensory_gating_ratio"] > 0.30
    assert thalamus["status"] == "cortical_activation_granted"
    assert res_cen["tri_network_brain_state"]["active_network"].startswith("CEN")
    assert res_cen["hippocampal_synaptic_plasticity"]["ltp_synapses_potentiated"] > 0

    # 2. Contemplative query -> DMN activation
    res_dmn = biological_brain.process_cognitive_cycle(
        "inner peace, grief, and finding purpose in suffering",
        particle_prob=0.15,
        wave_prob=0.85,
    )
    assert res_dmn["tri_network_brain_state"]["active_network"].startswith("DMN")
    somatic = res_dmn["amygdala_somatic_governor"]
    assert somatic["prefrontal_veto_exercised"] is False


def test_maqamat_al_qalb():
    """Validates the 7 Spiritual Stations of the Heart in OntologicalSpiritualEngine."""
    assert len(ontological_spiritual_engine.MAQAMAT) == 7

    # Test Peace / Sakoon mapping
    station_peace = ontological_spiritual_engine.determine_maqam("seeking inner peace and tranquility of the heart")
    assert "Itminan" in station_peace["station"]

    # Test Cosmic Reflection mapping
    station_refl = ontological_spiritual_engine.determine_maqam("contemplating the stars, cosmos, and quantum laws")
    assert "Tafakkur" in station_refl["station"]

    resonance = ontological_spiritual_engine.match_resonance("how to deal with grief and anxiety", 0.2, 0.8)
    assert "spiritual_station_maqam" in resonance
    assert "maqam_details" in resonance


def test_hyde_and_crag_evaluator():
    """Validates HyDE document generation and Self-RAG/CRAG evaluation."""
    doc = hyde_generator.generate_hypothetical_document("quantum entanglement in superconductors")
    assert "Hamiltonian" in doc or "quantum" in doc

    citations = [
        SourceCitation(source_id="arxiv", title="Superconductivity and Entanglement", snippet="Experimental evidence in cuprates"),
        SourceCitation(source_id="nasa", title="Astrophysical Entanglement", snippet="Cosmic ray observation"),
    ]
    crag_report = crag_evaluator.evaluate_retrieval("quantum entanglement", citations)
    assert crag_report["crag_action"] in ["CORRECT", "AMBIGUOUS", "INCORRECT"]
    assert crag_report["retrieval_confidence_score"] > 0.0


def test_universe_knowledge_graph():
    """Validates multi-source Knowledge Graph merging and GraphRAG path traversal."""
    universe_knowledge_graph.ingest_wikidata_entity("Q11053", "Chlorophyll", "Green pigment for photosynthesis")
    universe_knowledge_graph.ingest_dbpedia_relation("Chlorophyll", "substanceOf", "Plant_Cell")
    universe_knowledge_graph.ingest_openalex_work("10.1038/nature12345", "Quantum Biology of LHCII", 450, ["Chlorophyll", "Photosynthesis"])

    stats = universe_knowledge_graph.get_graph_stats()
    assert stats["total_nodes"] >= 7
    assert stats["total_edges"] >= 3

    paths = universe_knowledge_graph.query_multihop_path("Chlorophyll", "Mizan", max_hops=3)
    assert isinstance(paths, list)


@pytest.mark.asyncio
async def test_full_neuro_quantum_cycle():
    """Validates full end-to-end think_and_reply pipeline with all Phase 2 & 3 integrations."""
    response = await neural_brain.think_and_reply(
        query="photosynthesis and quantum exciton coherence",
        target_k=3,
        force_apis=["wikipedia", "openalex", "wikidata"],
        use_quantum=True,
    )
    assert response.query == "photosynthesis and quantum exciton coherence"
    assert response.biological_brain_telemetry is not None
    assert response.crag_retrieval_evaluation is not None
    assert response.vqe_molecular_simulation is not None
    assert response.vqe_molecular_simulation["molecule"] in ["CO2", "H2"]
    assert response.quantum_kernel_analysis is not None
    assert response.universe_knowledge_graph_stats is not None
    assert response.quantum_telemetry is not None
    assert "cvar_alpha" in response.quantum_telemetry
    assert len(response.cognitive_flow.nodes) >= 6
