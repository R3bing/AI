"""Unit tests for the Neural-Quantum Cognitive Brain, Wave-Particle Duality, and Tafakkur Engine.
"""

import pytest
import math
from backend.neural_brain.duality_balancer import duality_balancer
from backend.neural_brain.tafakkur_engine import tafakkur_engine
from backend.neural_brain.engine import neural_brain


def test_wave_particle_quantum_normalization():
    queries = [
        "What is the mathematical proof of quantum supremacy in QAOA?",
        "I feel overwhelmed, sad, and anxious about my purpose in life.",
        "How do physics and universal consciousness reflect each other in quantum mechanics?",
    ]

    for q in queries:
        state = duality_balancer.compute_duality(q)
        # Verify normalization |alpha|^2 + |beta|^2 == 1.0
        sum_prob = state.particle_probability + state.wave_probability
        assert math.isclose(sum_prob, 1.0, abs_tol=1e-3)
        assert state.particle_amplitude_alpha >= 0.0
        assert state.wave_amplitude_beta >= 0.0


def test_duality_dominance_polarity():
    # Pure technical query -> Particle / Aql dominance
    tech_state = duality_balancer.compute_duality("quantum algorithms, qubits, and mathematical equations")
    assert "Particle" in tech_state.dominant_state or tech_state.particle_probability > 0.5

    # Pure emotional/spiritual query -> Wave / Qalb dominance
    spirit_state = duality_balancer.compute_duality("I feel deep pain, stress, sorrow, and seek spiritual peace")
    assert "Wave" in spirit_state.dominant_state or spirit_state.wave_probability > 0.5


def test_tafakkur_engine_generation():
    tafakkur = tafakkur_engine.generate_tafakkur("anxiety, failure, and stress")
    assert "Ash-Sharh" in tafakkur["quranic_verse"] or "ease" in tafakkur["quranic_verse"]
    assert len(tafakkur["contemplative_questions"]) == 3
    assert "Fatwa" in tafakkur["disclaimer"]


@pytest.mark.asyncio
async def test_neural_brain_flowchart_execution():
    res = await neural_brain.think_and_reply("How does quantum physics relate to universal harmony and inner peace?")

    assert res.duality_state is not None
    assert len(res.cognitive_flow.nodes) == 6  # All 6 flowchart steps executed
    assert res.cognitive_flow.nodes[0].step_id == "STEP_1_THALAMUS"
    assert res.cognitive_flow.nodes[1].step_id == "STEP_2_DUALITY_ALLOCATION"
    assert res.cognitive_flow.nodes[4].step_id == "STEP_5_CORPUS_CALLOSUM"
    assert res.cognitive_flow.nodes[5].step_id == "STEP_6_PREFRONTAL_CORTEX"
    assert len(res.harmonious_synthesis) > 100
