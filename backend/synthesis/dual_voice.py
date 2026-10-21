"""Dual-Voice Dialectical Dialogue Engine for Quantum Knowledge Weaver.
Generates an interactive dialectic between Dr. Aql (Empirical Scientist)
and Shaykh Qalb (Contemplative Sage / Sufi Philosopher).
"""

from typing import List, Dict, Any


class DualVoiceGenerator:
    """Generates a structured multi-turn conversation reconciling science and spirituality."""

    def generate_dialogue(
        self,
        query: str,
        logical_answer: str,
        tafakkur_reflection: str,
        harmonious_synthesis: str = "",
    ) -> List[Dict[str, str]]:
        """Constructs an evocative 5-turn dialogue between Dr. Aql and Shaykh Qalb."""
        # Clean summaries for spoken cadence
        aql_clean = " ".join(logical_answer.replace("#", "").split()[:75])
        qalb_clean = " ".join(tafakkur_reflection.replace("#", "").split()[:75])

        dialogue = [
            {
                "speaker": "Host (Quantum Synthesizer)",
                "role": "Moderator",
                "voice_pitch": 1.0,
                "voice_rate": 1.0,
                "text": f"Welcome to the Quantum Knowledge Weaver. Today, we contemplate the inquiry: '{query[:90]}...'. Let us witness the dialogue between empirical intellect and contemplative heart.",
            },
            {
                "speaker": "Dr. Aql",
                "role": "The Empirical Scientist (Particle Nature)",
                "voice_pitch": 1.15,
                "voice_rate": 1.05,
                "text": f"Looking strictly through empirical observation and physical measurement: {aql_clean}. The laws of nature demonstrate mathematically rigorous structure and invariant symmetry.",
            },
            {
                "speaker": "Shaykh Qalb",
                "role": "The Contemplative Sage (Wave Nature)",
                "voice_pitch": 0.85,
                "voice_rate": 0.92,
                "text": f"SubhanAllah. While the intellect calculates the mechanisms, the heart perceives the underlying purpose: {qalb_clean}. These empirical symmetries are not empty equations; they are signs, inviting human consciousness into stillness and awe.",
            },
            {
                "speaker": "Dr. Aql",
                "role": "The Empirical Scientist (Particle Nature)",
                "voice_pitch": 1.15,
                "voice_rate": 1.05,
                "text": "Indeed, modern physics itself reveals that observer and observed cannot be wholly disentangled. At the quantum scale, matter dissolves into possibilities and probability amplitudes until measured.",
            },
            {
                "speaker": "Shaykh Qalb",
                "role": "The Contemplative Sage (Wave Nature)",
                "voice_pitch": 0.85,
                "voice_rate": 0.92,
                "text": "And that is where our faculties unite. When Aql recognizes its boundaries, it transforms into humility. The particle and the wave are one reality under the single Sustainer of the cosmos.",
            },
            {
                "speaker": "Host (Quantum Synthesizer)",
                "role": "Moderator",
                "voice_pitch": 1.0,
                "voice_rate": 1.0,
                "text": "Measurement collapsed into harmony. |Psi⟩ achieves equilibrium: where scientific rigor confirms cosmic order, and contemplation infuses life with meaning.",
            },
        ]
        return dialogue


dual_voice_generator = DualVoiceGenerator()
