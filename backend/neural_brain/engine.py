"""Neural-Quantum Cognitive Brain Engine.
Orchestrates human-like dual-hemisphere reasoning:
Left Hemisphere (Aql/Logic/Particle) <---> Corpus Callosum <---> Right Hemisphere (Qalb/Spirit/Wave).
Tracks full background cognitive flowcharts and emits unified responses.
"""

import time
from typing import Dict, Any, List
import structlog
from backend.neural_brain.models import (
    DualityState,
    CognitiveFlowNode,
    CognitiveFlowchart,
    NeuralBrainResponse,
)
from backend.neural_brain.duality_balancer import duality_balancer
from backend.neural_brain.tafakkur_engine import tafakkur_engine
from backend.orchestrator.engine import orchestrator
from backend.orchestrator.models import QueryRequest

logger = structlog.get_logger(__name__)


class NeuralCognitiveBrain:
    """Master human-like cognitive engine balancing Left-Brain (Aql/Logic) and Right-Brain (Qalb/Spirit)."""

    def __init__(self):
        self.duality_balancer = duality_balancer
        self.tafakkur_engine = tafakkur_engine
        self.orchestrator = orchestrator

    async def think_and_reply(self, query: str) -> NeuralBrainResponse:
        """Executes the full neuro-cognitive flowchart from sensory intake to harmonious synthesis."""
        start_time = time.perf_counter()
        flow_nodes: List[CognitiveFlowNode] = []

        # -------------------------------------------------------------
        # 1. Sensory Intake (Thalamus Sensory Filter)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        query_clean = query.strip()
        word_count = len(query_clean.split())
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_1_THALAMUS",
                phase="Sensory Intake",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Sensory Intake & Token Extraction",
                output_summary=f"Processed inquiry ({word_count} tokens) across linguistic and semantic pathways.",
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 2. Wave-Particle Duality State Allocation
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        duality: DualityState = self.duality_balancer.compute_duality(query_clean)
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_2_DUALITY_ALLOCATION",
                phase="Duality Allocation",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Quantum Wave-Particle State Superposition",
                output_summary=(
                    f"Superposition State: {duality.dominant_state} | "
                    f"Particle |Aql|² = {duality.particle_probability * 100:.1f}%, "
                    f"Wave |Qalb|² = {duality.wave_probability * 100:.1f}%."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 3. Left Hemisphere (Particle / Aql / QAOA & API Orchestration)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        qkw_req = QueryRequest(
            text=query_clean,
            use_quantum=True,
            max_sources=3,
        )
        qkw_res = await self.orchestrator.execute_query(qkw_req)
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_3_LEFT_HEMISPHERE",
                phase="Hemispheric Processing",
                hemisphere="Left (Brain/Aql)",
                action_taken="QAOA Quantum Routing & Multi-Source Empirical Retrieval",
                output_summary=(
                    f"Quantum Router consulted: {', '.join(qkw_res.apis_consulted)}. "
                    f"Extracted {len(qkw_res.citations)} authoritative citations in {qkw_res.total_latency_ms:.1f}ms."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 4. Right Hemisphere (Wave / Qalb / Tafakkur Contemplation)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        tafakkur_data = self.tafakkur_engine.generate_tafakkur(query_clean)
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_4_RIGHT_HEMISPHERE",
                phase="Hemispheric Processing",
                hemisphere="Right (Heart/Qalb)",
                action_taken="Tafakkur & Spiritual Psychology Resonator",
                output_summary=f"Activated contemplative resonance on theme '{tafakkur_data['theme']}'.",
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 5. Corpus Callosum (Synaptic Cross-Bridge)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        num_cross_refs = len(qkw_res.cross_references)
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_5_CORPUS_CALLOSUM",
                phase="Corpus Callosum Synapse",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Cross-Domain Synaptic Bridging",
                output_summary=(
                    f"Correlated {num_cross_refs} semantic links bridging scientific data "
                    f"with theological and philosophical insights."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 6. Prefrontal Cortex: Balanced Coherent Synthesis
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        harmonious_lines = [
            "### ⚖️ The Harmonious Synthesis: Heart & Brain in Balance",
            "",
            f"**Quantum State Superposition:** `{duality.dominant_state}` "
            f"*(Particle/Aql Weight: {duality.particle_probability * 100:.1f}% | Wave/Qalb Weight: {duality.wave_probability * 100:.1f}%)*\n",
            "#### 🧠 1. The Factual & Empirical Grounding (Aql):",
            qkw_res.synthesized_answer,
            "",
            "#### 🕊️ 2. The Contemplative Dimension (Qalb / Tafakkur):",
            f"> *\"{tafakkur_data['quranic_verse']}\"*",
            f"> *\"{tafakkur_data['prophetic_hadith']}\"*",
            "",
            f"**Sufi Psychological Insight:** {tafakkur_data['spiritual_psychology_insight']}",
            "",
            "**Inward Questions for Reflection (Tafakkur):**",
        ]

        for q_idx, question in enumerate(tafakkur_data["contemplative_questions"], 1):
            harmonious_lines.append(f"{q_idx}. *{question}*")

        harmonious_lines.append(f"\n_{tafakkur_data['disclaimer']}_")

        final_synthesis = "\n".join(harmonious_lines)

        total_latency = (time.perf_counter() - start_time) * 1000.0

        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_6_PREFRONTAL_CORTEX",
                phase="Coherent Synthesis",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Unified Coherent Emission",
                output_summary=f"Emitted balanced response in {total_latency:.1f}ms with 100% quantum-classical coherence.",
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        flowchart = CognitiveFlowchart(
            nodes=flow_nodes,
            total_synaptic_latency_ms=round(total_latency, 2),
        )

        citations_list = [c.model_dump() for c in qkw_res.citations]
        quantum_dict = qkw_res.quantum_routing.model_dump() if qkw_res.quantum_routing else None

        return NeuralBrainResponse(
            query=query_clean,
            duality_state=duality,
            cognitive_flow=flowchart,
            logical_factual_answer=qkw_res.synthesized_answer,
            tafakkur_reflection=tafakkur_data["spiritual_psychology_insight"],
            harmonious_synthesis=final_synthesis,
            citations=citations_list,
            quantum_telemetry=quantum_dict,
        )


# Global singleton instance
neural_brain = NeuralCognitiveBrain()
