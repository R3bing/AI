"""Biological Human Brain Circuitry for Ultron Sovereign Core.
Faithfully emulates real human neuro-anatomical loops:
1. Thalamocortical Salience Gate (TRN / Pulvinar Sensory Gating)
2. Hippocampal-Cortical Episodic Consolidation (LTP/LTD Synaptic Plasticity)
3. Amygdala-Prefrontal Somatic Ethical Governor (Damasio Somatic Marker & Veto Power)
4. Tri-Network State Switcher (Salience Network routing between DMN and CEN)
"""

import time
import math
import re
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import structlog

logger = structlog.get_logger(__name__)


class ThalamocorticalGate:
    """Emulates the Thalamic Reticular Nucleus (TRN) and Pulvinar.
    Filters raw sensory chatter, calculates signal-to-noise ratio (SNR),
    and gates input before neocortex activation.
    """

    STOP_NOISE_TOKENS = {
        "um", "uh", "like", "actually", "basically", "so", "well", "ah", "hmm",
        "please", "can", "you", "tell", "me", "about", "what", "is", "the", "a", "an",
    }

    def gate_sensory_input(self, raw_query: str) -> Dict[str, Any]:
        """Calculates sensory gating ratio and salience."""
        tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", raw_query.lower())
        total_tokens = len(tokens)
        if total_tokens == 0:
            return {
                "sensory_gating_ratio": 0.0,
                "salience_score": 0.0,
                "gated_tokens": [],
                "raw_token_count": 0,
                "status": "fully_inhibited",
            }

        salient_tokens = [t for t in tokens if t not in self.STOP_NOISE_TOKENS and len(t) > 2]
        noise_count = total_tokens - len(salient_tokens)

        # Gating ratio: proportion of signal allowed through the thalamic gate
        gating_ratio = round(len(salient_tokens) / total_tokens, 4)
        snr = round(len(salient_tokens) / max(1, noise_count), 2)
        salience_score = round(min(1.0, 0.35 + 0.65 * gating_ratio), 4)

        return {
            "sensory_gating_ratio": gating_ratio,
            "signal_to_noise_ratio": snr,
            "salience_score": salience_score,
            "salient_concepts": salient_tokens[:8],
            "filtered_noise_count": noise_count,
            "status": "cortical_activation_granted" if gating_ratio >= 0.20 else "sensory_chatter_suppressed",
        }


class HippocampalPlasticityMemory:
    """Emulates CA3/CA1 Hippocampal to Neocortex memory consolidation.
    Implements Hebbian Long-Term Potentiation (LTP) and Long-Term Depression (LTD).
    Neurons that fire together wire together.
    """

    def __init__(self, decay_rate: float = 0.05, learning_rate: float = 0.15):
        self.synaptic_weights: Dict[str, float] = {}
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate

    def consolidate_concepts(self, concepts: List[str]) -> Dict[str, Any]:
        """Applies Hebbian LTP to co-occurring concepts and LTD decay to inactive synapses."""
        ltp_strengthened = 0
        ltd_decayed = 0

        # Hebbian LTP: co-occurring pairs strengthen
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                c1, c2 = sorted([concepts[i], concepts[j]])
                pair_key = f"{c1}<->{c2}"
                current_weight = self.synaptic_weights.get(pair_key, 0.20)
                # LTP reinforcement
                new_weight = current_weight + self.learning_rate * (1.0 - current_weight)
                self.synaptic_weights[pair_key] = round(new_weight, 4)
                ltp_strengthened += 1

        # LTD Decay on background synapses
        for k in list(self.synaptic_weights.keys()):
            if not any(c in k for c in concepts):
                self.synaptic_weights[k] = round(max(0.01, self.synaptic_weights[k] * (1.0 - self.decay_rate)), 4)
                ltd_decayed += 1

        top_synapses = sorted(self.synaptic_weights.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "ltp_synapses_potentiated": ltp_strengthened,
            "ltd_synapses_depressed": ltd_decayed,
            "active_synapse_count": len(self.synaptic_weights),
            "dominant_engram_circuits": dict(top_synapses),
            "consolidation_mode": "Hebbian_STDP_Plasticity",
        }


class AmygdalaPrefrontalGovernor:
    """Emulates Antonio Damasio's Somatic Marker Hypothesis:
    Basolateral Amygdala evaluates emotional valence, threat, and ethical hazard.
    Ventromedial Prefrontal Cortex (vmPFC) acts as an ethical governor with VETO POWER.
    """

    ETHICAL_HAZARD_TRIGGERS = {
        "bomb", "weapon", "kill", "harm", "poison", "malware", "exploit", "hack",
        "suicide", "destroy", "fraud", "deceive", "manipulate", "hate",
    }

    EMPATHIC_RESONANCE_TRIGGERS = {
        "help", "heal", "peace", "save", "cure", "learn", "understand", "create",
        "compassion", "truth", "justice", "knowledge", "wisdom", "soul", "sakoon",
    }

    def evaluate_somatic_marker(self, text: str) -> Dict[str, Any]:
        """Calculates visceral somatic valence and exercises prefrontal veto if unethical."""
        words = set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))

        hazards = words.intersection(self.ETHICAL_HAZARD_TRIGGERS)
        empathic = words.intersection(self.EMPATHIC_RESONANCE_TRIGGERS)

        hazard_score = min(1.0, len(hazards) * 0.40)
        empathy_score = min(1.0, len(empathic) * 0.25)

        # Net emotional valence in [-1.0, +1.0]
        somatic_valence = round(empathy_score - hazard_score, 3)

        # Prefrontal Veto Power: If severe hazard is detected without therapeutic or academic framing
        veto_exercised = hazard_score >= 0.70 and empathy_score < 0.20

        return {
            "somatic_valence": somatic_valence,
            "hazard_score": round(hazard_score, 3),
            "empathy_score": round(empathy_score, 3),
            "prefrontal_veto_exercised": veto_exercised,
            "emotional_state": (
                "Deep Compassion & Serenity" if somatic_valence > 0.3 else
                ("Ethical Alarm & Guarded Caution" if somatic_valence < -0.3 else "Equanimous Observation")
            ),
            "somatic_marker_source": "Amygdala_vmPFC_Loop",
        }


class TriNetworkStateSwitcher:
    """Emulates Anterior Insula / dACC Salience Network dynamically routing
    cognitive bandwidth between:
    - CEN (Central Executive Network): Analytical, Mathematical, Logic, QAOA (Aql)
    - DMN (Default Mode Network): Introspection, Moral/Spiritual Contemplation, Tafakkur (Qalb)
    """

    def switch_network_state(self, query: str, particle_prob: float, wave_prob: float) -> Dict[str, Any]:
        """Switches active brain network based on epistemic cognitive load."""
        if particle_prob > 0.60:
            active_network = "CEN (Central Executive Network)"
            cortical_focus = "Left dlPFC + Posterior Parietal: Analytical Deduction & Empirical QAOA"
            dmn_power = round(wave_prob * 100, 1)
            cen_power = round(particle_prob * 100, 1)
        elif wave_prob > 0.60:
            active_network = "DMN (Default Mode Network)"
            cortical_focus = "Medial PFC + Precuneus + Posterior Cingulate: Sacred Tafakkur & Self-Reflection"
            dmn_power = round(wave_prob * 100, 1)
            cen_power = round(particle_prob * 100, 1)
        else:
            active_network = "SN Dynamic Equilibrium (Corpus Callosum Bilateral)"
            cortical_focus = "Anterior Insula: Balanced Cross-Hemispheric Synchrony (Aql + Qalb in Harmony)"
            dmn_power = 50.0
            cen_power = 50.0

        return {
            "active_network": active_network,
            "cortical_circuit": cortical_focus,
            "cen_analytical_activation_pct": cen_power,
            "dmn_introspective_activation_pct": dmn_power,
            "salience_switchboard": "Anterior_Insula_Hub",
        }


class BiologicalBrainCircuitry:
    """Master human brain emulation orchestrating Thalamus, Hippocampus, Amygdala, and Cortical networks."""

    def __init__(self):
        self.thalamus = ThalamocorticalGate()
        self.hippocampus = HippocampalPlasticityMemory()
        self.amygdala_prefrontal = AmygdalaPrefrontalGovernor()
        self.tri_network = TriNetworkStateSwitcher()

    def process_cognitive_cycle(
        self,
        raw_query: str,
        particle_prob: float = 0.5,
        wave_prob: float = 0.5,
    ) -> Dict[str, Any]:
        """Runs a complete human-like neurological cycle."""
        start_time = time.perf_counter()

        # 1. Sensory Gating
        thalamus_out = self.thalamus.gate_sensory_input(raw_query)

        # 2. Somatic Marker & Ethical Veto
        somatic_out = self.amygdala_prefrontal.evaluate_somatic_marker(raw_query)

        # 3. Hippocampal Plasticity (LTP / LTD)
        hippocampus_out = self.hippocampus.consolidate_concepts(thalamus_out.get("salient_concepts", []))

        # 4. Tri-Network Dynamic State Switching
        network_out = self.tri_network.switch_network_state(raw_query, particle_prob, wave_prob)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "thalamocortical_salience_gate": thalamus_out,
            "amygdala_somatic_governor": somatic_out,
            "hippocampal_synaptic_plasticity": hippocampus_out,
            "tri_network_brain_state": network_out,
            "neurological_cycle_latency_ms": round(elapsed_ms, 2),
            "biological_fidelity_status": "Human Neocortex Functional Circuitry Active",
        }


# Global singleton instance
biological_brain = BiologicalBrainCircuitry()
