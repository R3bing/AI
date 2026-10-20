"""Wave-Particle Duality Balancer for the Neural-Quantum Cognitive Brain.
Mimics the quantum duality of matter and energy:
|Psi> = alpha |Aql (Particle/Logic)> + beta |Qalb (Wave/Heart)>
Ensures strict quantum normalization: |alpha|^2 + |beta|^2 = 1.
"""

import math
import numpy as np
from backend.neural_brain.models import DualityState


class DualityBalancer:
    """Balances Particle (Logic, Physics, Proof) and Wave (Heart, Spirit, Contemplation) amplitudes."""

    # Lexical resonant frequencies
    PARTICLE_KEYWORDS = {
        "quantum", "physics", "algorithm", "qubit", "math", "code", "equation", "proof",
        "calculate", "data", "how", "latency", "speed", "hardware", "chemistry", "biology",
        "formula", "optimum", "function", "variable", "mechanism", "science", "experiment",
    }

    WAVE_KEYWORDS = {
        "heart", "soul", "qalb", "spirit", "tafakkur", "peace", "sad", "stress", "anxiety",
        "hope", "purpose", "why", "death", "life", "pain", "love", "mercy", "repentance",
        "forgiveness", "reflect", "contemplate", "universe", "wisdom", "morality", "god", "allah",
    }

    def compute_duality(self, text: str) -> DualityState:
        """Calculates normalized quantum amplitudes alpha (Particle) and beta (Wave)."""
        clean_tokens = set(text.lower().replace("?", "").replace(",", "").replace(".", "").split())

        # Baseline vacuum fluctuations
        raw_particle = 1.0
        raw_wave = 1.0

        # Particle (Aql) resonance
        particle_hits = len(clean_tokens.intersection(self.PARTICLE_KEYWORDS))
        raw_particle += particle_hits * 2.5

        # Wave (Qalb) resonance
        wave_hits = len(clean_tokens.intersection(self.WAVE_KEYWORDS))
        raw_wave += wave_hits * 2.5

        # Information entropy metric
        total_words = max(1, len(clean_tokens))
        entropy = - sum((1 / total_words) * math.log2(1 / total_words) for _ in clean_tokens)

        # Quantum state normalization: |alpha|^2 + |beta|^2 = 1
        norm_factor = raw_particle + raw_wave
        prob_particle = raw_particle / norm_factor
        prob_wave = raw_wave / norm_factor

        alpha = math.sqrt(prob_particle)
        beta = math.sqrt(prob_wave)

        # Dominant classification
        if prob_particle > 0.62:
            dominant = "Aql (Brain/Particle)"
        elif prob_wave > 0.62:
            dominant = "Qalb (Heart/Wave)"
        else:
            dominant = "Equilibrium (Harmonious Dual)"

        return DualityState(
            particle_amplitude_alpha=round(alpha, 4),
            wave_amplitude_beta=round(beta, 4),
            particle_probability=round(prob_particle, 4),
            wave_probability=round(prob_wave, 4),
            dominant_state=dominant,
            entropy_score=round(entropy, 4),
        )


duality_balancer = DualityBalancer()
