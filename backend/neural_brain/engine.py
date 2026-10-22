"""Neural-Quantum Cognitive Brain Engine.
Orchestrates human-like dual-hemisphere reasoning:
Left Hemisphere (Aql/Logic/Particle) <---> Corpus Callosum <---> Right Hemisphere (Qalb/Spirit/Wave).
Tracks full background cognitive flowcharts and emits unified responses.
"""

import time
from typing import Dict, Any, List, Optional
import structlog
from backend.neural_brain.models import (
    DualityState,
    CognitiveFlowNode,
    CognitiveFlowchart,
    NeuralBrainResponse,
)
from backend.neural_brain.duality_balancer import duality_balancer
from backend.neural_brain.tafakkur_engine import tafakkur_engine
from backend.neural_brain.antigravity_mimic import antigravity_mimic
from backend.orchestrator.engine import orchestrator
from backend.orchestrator.models import QueryRequest

logger = structlog.get_logger(__name__)


class NeuralCognitiveBrain:
    """Master human-like cognitive engine balancing Left-Brain (Aql/Logic) and Right-Brain (Qalb/Spirit)."""

    def __init__(self):
        self.duality_balancer = duality_balancer
        self.tafakkur_engine = tafakkur_engine
        self.antigravity_mimic = antigravity_mimic
        self.orchestrator = orchestrator

    async def think_and_reply(
        self,
        query: str,
        target_k: int = 4,
        force_apis: Optional[List[str]] = None,
        use_quantum: bool = True,
        mixer_type: str = "xy_mixer",
        api_keys: Optional[Dict[str, str]] = None,
        llm_provider: Optional[str] = None,
        deepseek_api_key: Optional[str] = None,
    ) -> NeuralBrainResponse:
        """Executes the full neuro-cognitive flowchart from sensory intake to harmonious synthesis."""
        start_time = time.perf_counter()
        flow_nodes: List[CognitiveFlowNode] = []

        # -------------------------------------------------------------
        # -------------------------------------------------------------
        # 1. Biological Brain Circuitry: Sensory Gating & Salience (Thalamocortical Loop)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        query_clean = query.strip()
        word_count = len(query_clean.split())
        from backend.neural_brain.query_parser import query_parser
        parsed_query = query_parser.parse(query_clean)

        # -------------------------------------------------------------
        # 2. Wave-Particle Duality State Allocation
        # -------------------------------------------------------------
        duality: DualityState = self.duality_balancer.compute_duality(query_clean)

        # Execute full biological human brain cycle (TRN Gating, Somatic Governor, Hippocampal LTP/LTD, Tri-Network DMN/CEN)
        from backend.neural_brain.biological_brain_circuitry import biological_brain
        bio_brain_telemetry = biological_brain.process_cognitive_cycle(
            raw_query=query_clean,
            particle_prob=duality.particle_probability,
            wave_prob=duality.wave_probability,
        )

        entities_summary = ", ".join(parsed_query.core_entities[:4]) if parsed_query.core_entities else "General inquiry"
        domains_summary = ", ".join(parsed_query.epistemic_domains) if parsed_query.epistemic_domains else "Universal"
        gating_ratio = bio_brain_telemetry["thalamocortical_salience_gate"]["sensory_gating_ratio"]

        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_1_THALAMUS_SENSORY_GATE",
                phase="Sensory Intake",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Thalamocortical Sensory Gating & Salience Filter",
                output_summary=(
                    f"TRN Gating Ratio: {gating_ratio*100:.1f}% (Signal:Noise = {bio_brain_telemetry['thalamocortical_salience_gate']['signal_to_noise_ratio']}). "
                    f"Dissected ({word_count} tokens) into concepts [{entities_summary}] spanning {domains_summary}."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_2_DUALITY_TRI_NETWORK",
                phase="Duality Allocation",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Quantum Wave-Particle Superposition & Tri-Network Brain Switch",
                output_summary=(
                    f"Superposition: {duality.dominant_state} (|Aql|² = {duality.particle_probability * 100:.1f}%, |Qalb|² = {duality.wave_probability * 100:.1f}%). "
                    f"Active Cortical Network: {bio_brain_telemetry['tri_network_brain_state']['active_network']}."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 3. Left Hemisphere (Particle / Aql / QAOA + CVaR + ZNE & API Orchestration)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        qkw_req = QueryRequest(
            text=query_clean,
            use_quantum=use_quantum,
            max_sources=target_k,
            force_apis=force_apis,
            mixer_type=mixer_type,
            api_keys=api_keys,
            llm_provider=llm_provider,
            deepseek_api_key=deepseek_api_key,
        )
        qkw_res = await self.orchestrator.execute_query(qkw_req)

        # VQE Molecular ground state calculation if molecular / chemical query
        vqe_molecular_sim = None
        q_lower = query_clean.lower()
        if any(w in q_lower for w in ["photosynthesis", "chlorophyll", "co2", "h2", "lih", "molecule", "chemical", "atp"]):
            try:
                from backend.quantum.vqe_molecular_engine import vqe_molecular_engine
                target_mol = "CO2" if "co2" in q_lower or "photo" in q_lower else ("LIH" if "lih" in q_lower else "H2")
                vqe_molecular_sim = vqe_molecular_engine.solve_ground_state(target_mol)
            except Exception as e:
                logger.warning("vqe_molecular_solver_exception", error=str(e))

        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_3_LEFT_HEMISPHERE",
                phase="Hemispheric Processing",
                hemisphere="Left (Brain/Aql)",
                action_taken="QAOA (CVaR + ZNE) Quantum Routing & Empirical Retrieval",
                output_summary=(
                    f"QAOA consulted: {', '.join(qkw_res.apis_consulted)}. "
                    f"Extracted {len(qkw_res.citations)} citations in {qkw_res.total_latency_ms:.1f}ms"
                    + (f" | VQE Ground State {vqe_molecular_sim['molecule']}: {vqe_molecular_sim['vqe_ground_state_hartree']} Ha" if vqe_molecular_sim else "")
                    + "."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 4. Right Hemisphere (Wave / Qalb / Sacred Tafakkur & Maqamat al-Qalb)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        tafakkur_data = self.tafakkur_engine.generate_tafakkur(
            query_clean,
            particle_prob=duality.particle_probability,
            wave_prob=duality.wave_probability,
        )
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_4_RIGHT_HEMISPHERE",
                phase="Hemispheric Processing",
                hemisphere="Right (Heart/Qalb)",
                action_taken="Sacred Tafakkur & 7 Spiritual Stations of the Heart",
                output_summary=(
                    f"Resonance theme: '{tafakkur_data['theme']}' | "
                    f"Spiritual Station (Maqam): {tafakkur_data.get('spiritual_station_maqam', 'Tafakkur')}."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 5. Corpus Callosum (Synaptic Cross-Bridge, Quantum Kernel & CRAG)
        # -------------------------------------------------------------
        t0 = time.perf_counter()

        # Quantum Kernel Non-Linear Feature Map
        from backend.quantum.quantum_kernel import quantum_kernel_engine
        q_kernel_results = quantum_kernel_engine.cross_reference_quantum_kernel(
            query_clean, [c.model_dump() for c in qkw_res.citations]
        )

        # Self-RAG & Corrective RAG (CRAG) Evaluation
        from backend.cross_reference.hyde_crag_engine import crag_evaluator
        crag_report = crag_evaluator.evaluate_retrieval(query_clean, qkw_res.citations, qkw_res.cross_references)

        # Universe Knowledge Graph Ingestion & Topological Sync
        from backend.memory.universe_knowledge_graph import universe_knowledge_graph
        universe_knowledge_graph.merge_citations(qkw_res.citations, query_clean)
        ukg_stats = universe_knowledge_graph.get_graph_stats()

        num_cross_refs = len(qkw_res.cross_references)
        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_5_CORPUS_CALLOSUM",
                phase="Corpus Callosum Synapse",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Cross-Domain Synaptic Bridging, Quantum Kernel & CRAG Evaluator",
                output_summary=(
                    f"Correlated {num_cross_refs} semantic links. "
                    f"CRAG Grade: {crag_report['factuality_grade']} ({crag_report['crag_action']}) | "
                    f"Universe KG: {ukg_stats['total_nodes']} nodes, {ukg_stats['total_edges']} edges."
                ),
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 6. Prefrontal Cortex: Antigravity Meta-Cognitive Synthesis
        # -------------------------------------------------------------
        t0 = time.perf_counter()

        # Generate Antigravity's signature First-Principles & Philosophical Verdict
        antigravity_verdict, antigravity_insights = self.antigravity_mimic.generate_verdict(
            query=query_clean,
            duality=duality,
            citations=qkw_res.citations,
            cross_references=qkw_res.cross_references,
            tafakkur_data=tafakkur_data,
        )

        harmonious_lines = [
            "### ⚖️ The Harmonious Synthesis: Heart & Brain in Balance",
            "",
            f"**Quantum State Superposition:** `{duality.dominant_state}` "
            f"*(Particle/Aql Weight: {duality.particle_probability * 100:.1f}% | Wave/Qalb Weight: {duality.wave_probability * 100:.1f}%)*\n",
            antigravity_verdict,
            "",
            "---",
            "#### 🧠 1. The Factual & Empirical Grounding (Aql):",
            qkw_res.synthesized_answer,
            "",
            "#### 🕊️ 2. Ontological & Spiritual Equilibrium (The Heart's Resonance / Qalb):",
            f"> 📖 **Sacred Verse:** *\"{tafakkur_data['quranic_verse']}\"*",
            f"> 💡 **Scholarly Tafseer:** {tafakkur_data.get('tafseer_insight', '')}",
            f"> 📜 **Prophetic Tradition:** *\"{tafakkur_data['prophetic_hadith']}\"*",
            f"> 🌐 **Universal World Scripture ({tafakkur_data.get('comparative_tradition', 'Universal')}):** *\"{tafakkur_data.get('comparative_scripture', '')}\"*",
            "",
            f"**Sufi Soul Psychology (Nafs Analysis):** {tafakkur_data['spiritual_psychology_insight']}",
            "",
            "**Inward Inquiries for Contemplative Reflection (Tafakkur):**",
        ]

        for q_idx, question in enumerate(tafakkur_data["contemplative_questions"], 1):
            harmonious_lines.append(f"{q_idx}. *{question}*")

        harmonious_lines.append(f"\n_{tafakkur_data['disclaimer']}_")

        final_synthesis = "\n".join(harmonious_lines)

        # -------------------------------------------------------------
        # 6. Inter-AI Neural Conversation Pathway (Gemini ➔ DeepSeek ➔ Groq ➔ QKW)
        # -------------------------------------------------------------
        try:
            from backend.synthesis.multi_ai_dialogue import multi_ai_dialogue
            dialogue_res = await multi_ai_dialogue.run_inter_ai_dialogue(
                query=query_clean,
                citations_summary=qkw_res.synthesized_answer,
                runtime_keys=api_keys,
            )
        except Exception as e:
            logger.warning("inter_ai_dialogue_failed", error=str(e))
            dialogue_res = None

        total_latency = (time.perf_counter() - start_time) * 1000.0

        flow_nodes.append(
            CognitiveFlowNode(
                step_id="STEP_6_PREFRONTAL_CORTEX",
                phase="Coherent Synthesis",
                hemisphere="Both (Corpus Callosum)",
                action_taken="Antigravity Meta-Cognitive Synthesis & Inter-AI Dialogue Consensus",
                output_summary=f"Emitted definitive verdict across {len(qkw_res.apis_consulted)} databases & 3 AI models in {total_latency:.1f}ms.",
                activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
            )
        )

        # -------------------------------------------------------------
        # 7. Autonomous Continuous Online Learning (Scikit-Learn + PyTorch)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        try:
            from backend.ml.continuous_learner import continuous_online_learner
            online_stats = continuous_online_learner.learn_from_chat_turn(
                query=query_clean,
                dominant_mode=duality.dominant_state,
                sources_count=len(qkw_res.citations),
                entropy=duality.entropy_score,
                grounded_synthesis=final_synthesis,
                citations=[c.model_dump() for c in qkw_res.citations],
            )
            flow_nodes.append(
                CognitiveFlowNode(
                    step_id="STEP_7_CONTINUOUS_LEARNING",
                    phase="Coherent Synthesis",
                    hemisphere="Both (Corpus Callosum)",
                    action_taken="Incremental Online Learning (Scikit-Learn SGD + PyTorch Backprop)",
                    output_summary=(
                        f"Auto-trained on interaction #{online_stats['total_chats_learned']} "
                        f"(Loss: {online_stats['current_loss']}, Predicted: {online_stats['predicted_mode']})."
                    ),
                    activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
                )
            )
        except Exception as e:
            logger.warning("continuous_learning_step_failed", error=str(e))
            online_stats = None

        # -------------------------------------------------------------
        # 8. Autopoietic Organism Cycle (h_t, DNC Memory, Metacortex)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        try:
            from backend.autopoiesis.organism_orchestrator import autopoietic_organism
            autopoietic_stats = autopoietic_organism.process_turn(
                query=query_clean,
                dominant_mode=duality.dominant_state,
                entropy=duality.entropy_score,
                latency_ms=total_latency,
            )
            flow_nodes.append(
                CognitiveFlowNode(
                    step_id="STEP_8_AUTOPOIETIC_CYCLE",
                    phase="Coherent Synthesis",
                    hemisphere="Both (Corpus Callosum)",
                    action_taken="Autopoietic Latent Identity Update & Metacortex Self-Prediction",
                    output_summary=(
                        f"Step #{autopoietic_stats['cognitive_age_steps']} | Gen {autopoietic_stats['active_generation']} | "
                        f"Health: {autopoietic_stats['autopoietic_health_score']*100:.1f}% | "
                        f"Self-Pred Error: {autopoietic_stats['self_prediction_error']:.3f} | "
                        f"Immune: {autopoietic_stats['immune_status']}"
                    ),
                    activation_energy=round((time.perf_counter() - t0) * 1000.0, 2),
                )
            )
        except Exception as e:
            logger.warning("autopoietic_cycle_failed", error=str(e))
            autopoietic_stats = None

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
            cross_references=[cr.model_dump() for cr in qkw_res.cross_references],
            apis_consulted=qkw_res.apis_consulted,
            quantum_telemetry=quantum_dict,
            antigravity_verdict=antigravity_verdict,
            antigravity_insights=antigravity_insights,
            parsed_query=parsed_query.model_dump(),
            reasoning_trace=qkw_res.reasoning_trace or (dialogue_res.get("deepseek_reasoning") if dialogue_res else None),
            llm_provider_used=qkw_res.llm_provider_used,
            tafakkur_details=tafakkur_data,
            multi_ai_dialogue=dialogue_res,
            continuous_learning_telemetry=online_stats,
            autopoietic_telemetry=autopoietic_stats,
            biological_brain_telemetry=bio_brain_telemetry,
            crag_retrieval_evaluation=crag_report,
            vqe_molecular_simulation=vqe_molecular_sim,
            quantum_kernel_analysis=q_kernel_results,
            universe_knowledge_graph_stats=ukg_stats,
        )


# Global singleton instance
neural_brain = NeuralCognitiveBrain()
