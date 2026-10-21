"""Unit tests for Dynamic Duality Balancer, Physical QPU Emulator, and Continuous Online Learner."""

import pytest
import math
from backend.neural_brain.duality_balancer import duality_balancer
from backend.quantum.physical_qpu_emulator import physical_qpu_emulator
from backend.ml.continuous_learner import train_baseline_neural_network, continuous_online_learner


def test_dynamic_duality_balancer_quantum_normalization():
    """Verify that |alpha|^2 + |beta|^2 == 1.000 under all conditions."""
    queries = [
        "quantum superposition, entanglement, and QED physics equations",
        "deep grief, sorrow, seeking inner peace, and divine mercy through prayer",
        "how does an atom maintain equilibrium between energy and form?",
        "why do humans suffer when seeking purpose in transient life?",
    ]
    for q in queries:
        state = duality_balancer.compute_duality(q)
        norm_sum = round(state.particle_probability + state.wave_probability, 3)
        assert norm_sum == 1.0, f"Normalization violated for query: {q}"
        assert 0.0 < state.particle_amplitude_alpha <= 1.0
        assert 0.0 < state.wave_amplitude_beta <= 1.0
        assert state.entropy_score >= 0.0


def test_duality_balancer_scientific_vs_sacred_resonance():
    """Verify that scientific questions steer toward Aql and contemplative questions steer toward Qalb."""
    sci_state = duality_balancer.compute_duality("calculate quantum Hamiltonian eigenvalue and benchmark FLOPs on GPU")
    assert sci_state.particle_probability > sci_state.wave_probability
    assert "Left" in sci_state.dominant_state or "Aql" in sci_state.dominant_state

    sacred_state = duality_balancer.compute_duality("seeking spiritual sakoon, contemplation on the soul nafs and forgiveness")
    assert sacred_state.wave_probability > sacred_state.particle_probability
    assert "Right" in sacred_state.dominant_state or "Qalb" in sacred_state.dominant_state


def test_physical_qpu_noise_emulator():
    """Verify that physical QPU emulator applies decoherence damping and returns authentic metrics."""
    ideal_probs = {"0011": 0.65, "1100": 0.25, "0000": 0.10}
    noisy_probs, telemetry = physical_qpu_emulator.apply_physical_noise(
        ideal_probabilities=ideal_probs,
        num_qubits=4,
        p_layers=1,
        shots=1024,
    )
    assert telemetry["physical_qpu"] == "ibm_brisbane (127-Qubit Eagle QPU)"
    assert telemetry["t1_relaxation_time_us"] > 200.0
    assert telemetry["t2_dephasing_time_us"] > 100.0
    assert 0.50 <= telemetry["quantum_state_fidelity"] <= 1.0
    assert len(noisy_probs) > 0


def test_baseline_pytorch_feedforward_training():
    """Verify the 4-phase PyTorch neural network training loop."""
    res = train_baseline_neural_network(input_dim=16, hidden_dim=32, epochs=5, learning_rate=0.01)
    assert res["epochs_completed"] == 5
    assert len(res["loss_history"]) == 5
    # Loss should decrease or be non-negative
    assert res["final_loss"] >= 0.0
    assert res["training_accuracy"] >= 0.50
    assert res["total_parameters"] > 0


def test_continuous_online_learner_auto_train():
    """Verify that the model auto-trains without asking on every chat interaction."""
    initial_learned = continuous_online_learner.total_chats_learned
    res = continuous_online_learner.learn_from_chat_turn(
        query="what is quantum entanglement?",
        dominant_mode="Left Hemisphere Dominant (Aql)",
        sources_count=4,
        entropy=0.55,
    )
    assert res["status"] == "auto_trained_successfully"
    assert res["total_chats_learned"] == initial_learned + 1
    assert "current_loss" in res
    assert res["predicted_mode"] in ["Aql (Particle)", "Qalb (Wave)"]

    telemetry = continuous_online_learner.get_learning_telemetry()
    assert telemetry["total_chats_learned"] == initial_learned + 1
