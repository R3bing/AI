"""Streamlit Interactive Frontend for Quantum Knowledge Weaver (QKW).
Unified Dual-Hemisphere Neural-Quantum Cognitive Brain.
Merges empirical logic (Particle/Aql) with spiritual contemplation (Wave/Qalb)
through a 6-stage neuro-cognitive flowchart.
"""

import sys
import os
import time
import requests
import streamlit as st
import pandas as pd

# Add workspace root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(
    page_title="Quantum Knowledge Weaver (QKW) — Cognitive Brain",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for rich aesthetics
st.markdown(
    """
    <style>
    .main {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    .stMetric {
        background: rgba(30, 41, 59, 0.7);
        padding: 12px;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.15);
    }
    .quantum-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .citation-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-corroborate {
        background-color: #065f46;
        color: #6ee7b7;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
    }
    .badge-contradict {
        background-color: #991b1b;
        color: #fca5a5;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
    }
    .badge-complement {
        background-color: #1e40af;
        color: #93c5fd;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.image("https://img.icons8.com/nolan/96/quantum-computing.png", width=70)
st.sidebar.title("Quantum Brain")
st.sidebar.caption("Unified Dual-Hemisphere Cognitive Architecture")

api_backend_url = st.sidebar.text_input("Backend API Endpoint", value="http://localhost:8000")

# Check backend health
backend_online = False
health_info = {}
try:
    health_resp = requests.get(f"{api_backend_url}/health", timeout=1.5)
    if health_resp.status_code == 200:
        backend_online = True
        health_info = health_resp.json()
except Exception:
    backend_online = False

if backend_online:
    st.sidebar.success(f"● Backend Connected (v{health_info.get('version', '0.1.0')})")
    llm_badge = "🟢 Ready" if health_info.get("llm_connected") else "🟡 Offline / Fallback"
    st.sidebar.markdown(f"**Local LLM (Ollama):** {llm_badge}")
    st.sidebar.markdown(f"**Quantum Engine:** `{health_info.get('quantum_engine', 'QAOA')}`")
else:
    st.sidebar.warning("○ Backend Standalone (Direct Neural Engine Active)")

st.sidebar.markdown("---")
st.sidebar.subheader("Quantum Router (QAOA)")
use_quantum = st.sidebar.checkbox("Enable QAOA Routing", value=True)
max_sources = st.sidebar.slider("Target API Budget (K)", min_value=1, max_value=11, value=4)
mixer_type = st.sidebar.selectbox(
    "QAOA Mixer Hamiltonian",
    options=["xy_mixer", "standard"],
    index=0,
    format_func=lambda x: "XY-Mixer (Excitation-Preserving Dicke State)" if x == "xy_mixer" else "Standard Transverse Mixer (X)",
    help="XY-Mixer mathematically guarantees exactly K APIs are chosen without penalty tuning.",
)

# 11 Registered Knowledge Repositories
available_apis = ["wikipedia", "arxiv", "quran", "hadith", "pubmed", "nasa", "openalex", "pubchem", "google", "crossref", "openlibrary"]
force_selection = st.sidebar.multiselect(
    "Force Specific APIs (Optional)",
    options=available_apis,
    default=[],
    help="Leave empty for autonomous QAOA optimization",
)

# Main Title & Presentation
st.title("⚛️ Quantum Knowledge Weaver — Cognitive Brain")
st.markdown(
    "A unified hybrid quantum-classical architecture that balances **Empirical Science (Particle / Aql)** "
    "with **Spiritual Contemplation (Wave / Qalb)** across 11 public repositories: "
    "**Wikipedia**, **arXiv**, **Quran**, **Hadith**, **PubMed**, **NASA**, **OpenAlex**, **PubChem**, **Google Knowledge**, **Crossref**, and **Open Library**."
)

# Interactive Example Prompts
st.markdown("##### 💡 Explore with a Core Prompt:")
col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
sample_query = None

if col_ex1.button("🔬 Quantum Physics & Unity", use_container_width=True):
    sample_query = "What does modern physics say about quantum entanglement and interconnectedness, and how does classical thought or theology reflect on universal unity?"

if col_ex2.button("🏥 Medicine, Hygiene & Sunnah", use_container_width=True):
    sample_query = "How do modern medical research and prophetic traditions approach medicine, hygiene, and disease treatment?"

if col_ex3.button("🌌 NASA Astrophysics & Cosmos", use_container_width=True):
    sample_query = "What are the latest observations and discoveries about black holes, galaxies, and cosmology from space telescopes?"

if col_ex4.button("🧪 Molecular Drugs & Biology", use_container_width=True):
    sample_query = "What is the molecular formula, synthesis, and mechanism of action of penicillin in treating bacterial infections?"

# Main Query Input
query_text = st.text_input(
    "Enter your research or contemplation inquiry:",
    value=sample_query if sample_query else "",
    placeholder="Ask anything across science, medicine, existential philosophy, cosmology, or theology...",
)

col_btn, _ = st.columns([1, 6])
execute_search = col_btn.button("🔍 Weave Knowledge", type="primary", use_container_width=True)

if execute_search and query_text.strip():
    with st.spinner("Executing Neuro-Cognitive Flowchart & Wave-Particle Quantum Superposition..."):
        brain_response = None
        error_msg = None

        # 1. Try FastAPI Backend
        if backend_online:
            try:
                payload = {
                    "text": query_text.strip(),
                    "max_sources": max_sources,
                    "force_apis": force_selection if force_selection else None,
                    "use_quantum": use_quantum,
                    "mixer_type": mixer_type,
                }
                res = requests.post(f"{api_backend_url}/brain/think", json=payload, timeout=40.0)
                if res.status_code == 200:
                    brain_response = res.json()
                else:
                    error_msg = f"HTTP {res.status_code}: {res.text}"
            except Exception as e:
                error_msg = str(e)

        # 2. In-Process Direct Fallback
        if not brain_response:
            try:
                import asyncio
                from backend.neural_brain.engine import neural_brain
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res_obj = loop.run_until_complete(
                    neural_brain.think_and_reply(
                        query=query_text.strip(),
                        target_k=max_sources,
                        force_apis=force_selection if force_selection else None,
                        use_quantum=use_quantum,
                        mixer_type=mixer_type,
                    )
                )
                brain_response = res_obj.model_dump()
            except Exception as e:
                error_msg = f"In-process cognitive execution error: {str(e)}"

        if error_msg and not brain_response:
            st.error(f"Execution Error: {error_msg}")

        elif brain_response:
            duality = brain_response.get("duality_state", {})
            flow = brain_response.get("cognitive_flow", {})
            citations = brain_response.get("citations", [])
            cross_refs = brain_response.get("cross_references", [])
            q_details = brain_response.get("quantum_telemetry", {})

            # -------------------------------------------------------------
            # Top Heads-Up Display (HUD): Quantum Wave-Particle Superposition
            # -------------------------------------------------------------
            st.markdown(
                f"""
                <div class="quantum-card">
                    <h3 style="margin-top:0; color: #c084fc;">⚛️ Quantum Wave-Particle Superposition State: |Ψ⟩ = α|Aql⟩ + β|Qalb⟩</h3>
                    <p style="color: #cbd5e1; margin-bottom: 0;">
                        Mimicking the fundamental duality of matter & energy: balancing <b>Particle (Aql / Empirical Logic / Fact)</b>
                        with <b>Wave (Qalb / Contemplation / Spiritual Sakoon)</b> under strict quantum normalization (<b>|α|² + |β|² = 1.000</b>).
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Metric Cards
            dm1, dm2, dm3, dm4 = st.columns(4)
            dm1.metric("Dominant Resonance", duality.get("dominant_state", "Equilibrium"))
            dm2.metric("Particle |Aql|² (Logic & Fact)", f"{duality.get('particle_probability', 0) * 100:.1f}%")
            dm3.metric("Wave |Qalb|² (Spirit & Meaning)", f"{duality.get('wave_probability', 0) * 100:.1f}%")
            dm4.metric("Cognitive Latency", f"{flow.get('total_synaptic_latency_ms', 0):.1f} ms")

            # Dynamic Wave-Particle Balance Progress Meter
            particle_pct = duality.get("particle_probability", 0.5)
            st.markdown(f"**Aql (Particle / Logic) vs. Qalb (Wave / Contemplation) Balance:**")
            st.progress(
                float(particle_pct),
                text=f"Left: Aql/Brain {particle_pct*100:.1f}% ⟵ Harmonious Equilibrium ⟶ Right: Qalb/Heart {(1-particle_pct)*100:.1f}%",
            )

            # -------------------------------------------------------------
            # 7 Master Tabs: Merged with Perfection
            # -------------------------------------------------------------
            tab_syn, tab_flow, tab_quantum, tab_tafakkur, tab_citations, tab_graph, tab_bench = st.tabs([
                "⚖️ 1. Harmonious Synthesis",
                "🧠 2. Neuro-Cognitive Flowchart",
                "⚛️ 3. Quantum QAOA Telemetry",
                "🕊️ 4. Tafakkur & Spiritual Dimension",
                "📚 5. Citations & Cross-References",
                "🕸️ 6. Knowledge Graph & Quantum Lab",
                "📊 7. Academic Benchmark & Paper Lab",
            ])

            # Tab 1: Harmonious Synthesis
            with tab_syn:
                st.markdown("### ⚖️ The Harmonious Synthesis: Intellectual Rigor & Spiritual Sakoon")

                # Antigravity Meta-Cognitive Verdict
                verdict_text = brain_response.get("antigravity_verdict")
                if verdict_text:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, rgba(88, 28, 135, 0.35) 0%, rgba(15, 23, 42, 0.95) 100%);
                                    border: 2px solid #a855f7; border-radius: 12px; padding: 22px; margin-bottom: 25px;
                                    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.25);">
                            <span style="background: #a855f7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;">
                                🌟 ANTIGRAVITY COGNITIVE MATRIX • META-COGNITIVE VERDICT
                            </span>
                            <div style="margin-top: 15px; color: #f1f5f9; font-size: 0.98rem; line-height: 1.7;">
                                {verdict_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                col_left, col_right = st.columns(2)

                with col_left:
                    st.markdown(
                        f"""
                        <div style="background: rgba(30, 58, 138, 0.25); border: 1px solid rgba(59, 130, 246, 0.4);
                                    border-radius: 10px; padding: 18px; margin-bottom: 15px; height: 100%;">
                            <h4 style="margin-top:0; color: #60a5fa;">🧠 Left Hemisphere: Empirical Aql (Particle)</h4>
                            <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
                                {brain_response.get("logical_factual_answer", "")}
                            </p>
                            <small style="color: #93c5fd;">APIs Consulted: <b>{', '.join(brain_response.get('apis_consulted', []))}</b></small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col_right:
                    st.markdown(
                        f"""
                        <div style="background: rgba(6, 78, 59, 0.25); border: 1px solid rgba(16, 185, 129, 0.4);
                                    border-radius: 10px; padding: 18px; margin-bottom: 15px; height: 100%;">
                            <h4 style="margin-top:0; color: #34d399;">🕊️ Right Hemisphere: Contemplative Qalb (Wave)</h4>
                            <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
                                {brain_response.get("tafakkur_reflection", "")}
                            </p>
                            <small style="color: #a7f3d0;">Framework: <b>Ghazalian Hikmah & Sufi Nafs Psychology</b></small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("---")
                st.markdown(brain_response.get("harmonious_synthesis", ""))

            # Tab 2: Cognitive Flowchart Trace
            with tab_flow:
                st.markdown("### 🧠 Background Neuro-Cognitive Reasoning Architecture")
                st.markdown(
                    "Real-time trace of the brain's internal reasoning from sensory intake (Thalamus) through "
                    "parallel dual-hemispheric processing and corpus callosum synaptic bridge:"
                )

                # Visual Mermaid Diagram
                st.markdown(
                    """
```mermaid
graph TD
    classDef intake fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef duality fill:#7c3aed,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef leftBrain fill:#1d4ed8,stroke:#60a5fa,stroke-width:2px,color:#fff;
    classDef rightBrain fill:#047857,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef bridge fill:#b45309,stroke:#fbbf24,stroke-width:2px,color:#fff;
    classDef cortex fill:#7e22ce,stroke:#e879f9,stroke-width:2px,color:#fff;

    A["1. Sensory Intake (Thalamus Filter)"]:::intake --> B["2. Wave-Particle Duality Balancer<br>|Ψ⟩ = α|Aql⟩ + β|Qalb⟩"]:::duality
    B -->|Particle Stream α| C1["3. Left Hemisphere (Aql / Logic)<br>QAOA 8-API Quantum Retrieval"]:::leftBrain
    B -->|Wave Stream β| C2["4. Right Hemisphere (Qalb / Spirit)<br>Tafakkur Contemplation & Nafs Resonator"]:::rightBrain
    C1 --> D["5. Corpus Callosum Synaptic Bridge<br>NLI Semantic Cross-Referencing"]:::bridge
    C2 --> D
    D --> E["6. Prefrontal Cortex<br>Harmonious Balanced Synthesis"]:::cortex
```
                    """
                )

                st.markdown("#### Detailed Synaptic Step-by-Step Trace:")
                nodes = flow.get("nodes", [])
                for node in nodes:
                    hem = node.get("hemisphere", "Both")
                    badge_color = "#3b82f6" if "Left" in hem else ("#10b981" if "Right" in hem else "#a855f7")

                    st.markdown(
                        f"""
                        <div style="background: #1e293b; border-left: 4px solid {badge_color};
                                    border-radius: 6px; padding: 12px 16px; margin-bottom: 10px;">
                            <span style="background: {badge_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">
                                {node.get('phase', '').upper()} • {hem}
                            </span>
                            <strong style="margin-left: 8px; color: #f8fafc;">{node.get('action_taken')}</strong>
                            <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 0.9rem;">{node.get('output_summary')}</p>
                            <small style="color: #64748b;">Synaptic Latency: {node.get('activation_energy', 0):.2f} ms</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # Tab 3: Quantum QAOA Telemetry
            with tab_quantum:
                st.markdown("### ⚛️ QAOA API Selection Optimization")
                if q_details:
                    qc1, qc2, qc3 = st.columns(3)
                    qc1.metric("Qubits Used", q_details.get("qubits_count", 0))
                    qc2.metric("Quantum Energy <H_C>", f"{q_details.get('quantum_energy', 0):.4f}")
                    qc3.metric("QAOA Latency", f"{q_details.get('execution_time_ms', 0):.2f} ms")

                    st.markdown(f"**Quantum Algorithm:** `{q_details.get('algorithm')}`")
                    st.markdown(f"**Quantum Backend:** `{q_details.get('backend_used')}`")
                    st.markdown(f"**Candidate APIs (8-Qubit Register):** {', '.join(q_details.get('qubo_variables', []))}")
                    st.markdown(f"**Winning APIs Selected ($x_i=1$):** {', '.join(q_details.get('selected_apis', []))}")

                    probs = q_details.get("solution_probabilities", {})
                    if probs:
                        st.markdown("#### Measurement Basis State Probabilities:")
                        df_probs = pd.DataFrame([
                            {"Bitstring (|x>)": k, "Probability": v}
                            for k, v in probs.items()
                        ])
                        st.bar_chart(df_probs.set_index("Bitstring (|x>)"))
                else:
                    st.info("Quantum routing executed in manual override mode.")

            # Tab 4: Tafakkur & Spiritual Psychology
            with tab_tafakkur:
                st.markdown("### 🕊️ Tafakkur: Contemplative Spiritual Psychology")
                st.markdown(
                    f"""
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(16, 185, 129, 0.3);
                                border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                        <h4 style="margin-top:0; color: #34d399;">Spiritual Grounding & Reflection</h4>
                        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.7;">
                            {brain_response.get("tafakkur_reflection", "")}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.info(
                    "The Tafakkur engine synthesizes Islamic psychology, Ghazalian hikmah, and Sufi nafs models "
                    "(Nafs al-Ammarah, Lawwamah, and Mutma'innah) to provide emotional grounding, self-awareness, and spiritual tranquility (Sakoon)."
                )

            # Tab 5: Citations & Cross References
            with tab_citations:
                st.markdown("### 📚 Authoritative Citations (Retrieved from 8 APIs)")
                if not citations:
                    st.info("No direct citations were returned for this query.")
                else:
                    for i, cit in enumerate(citations, 1):
                        with st.expander(f"[{i}] {cit.get('source_name')} — {cit.get('title')}", expanded=True):
                            st.markdown(f"**Snippet:** *\"{cit.get('snippet')}\"*")
                            if cit.get("url"):
                                st.markdown(f"🔗 **URL:** [{cit.get('url')}]({cit.get('url')})")
                            st.caption(f"Relevance Score: {cit.get('relevance_score', 0):.2f}")

                if cross_refs:
                    st.markdown("---")
                    st.markdown("### 🔗 Semantic Cross-Referencing & NLI Contradiction Analysis")
                    for cr in cross_refs:
                        rel = cr.get("relationship", "complements")
                        badge_class = "badge-corroborate" if rel == "corroborates" else ("badge-contradict" if rel == "contradicts" else "badge-complement")
                        badge_label = rel.upper()

                        st.markdown(
                            f"""
                            <div class="citation-card">
                                <span class="{badge_class}">{badge_label}</span>
                                <strong> {cr.get('source_a_name')}</strong> ⟷ <strong>{cr.get('source_b_name')}</strong><br>
                                <small>Cosine Similarity: <b>{cr.get('similarity_score', 0) * 100:.1f}%</b></small><br>
                                <p style="margin-top: 6px; font-size: 0.9rem;">{cr.get('notes')}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            # Tab 6: Knowledge Graph & Quantum Lab
            with tab_graph:
                st.markdown("### 🕸️ Knowledge Graph & Interactive Quantum Lab")
                from backend.memory.neo4j_store import graph_memory
                graph_data = graph_memory.get_graph_data()

                nodes = graph_data.get("nodes", [])
                edges = graph_data.get("edges", [])

                gc1, gc2 = st.columns(2)
                with gc1:
                    st.markdown(f"**Total Entities / Nodes in Memory:** {len(nodes)}")
                    if nodes:
                        st.dataframe(pd.DataFrame(nodes)[["id", "label", "name"]], height=200, use_container_width=True)
                with gc2:
                    st.markdown(f"**Total Relationships:** {len(edges)}")
                    if edges:
                        st.dataframe(pd.DataFrame(edges)[["source", "relationship", "target"]], height=200, use_container_width=True)

                st.markdown("---")
                st.markdown("### 🔬 Interactive Quantum Algorithms Demonstrator")

                demo_choice = st.radio("Choose Quantum Module Demo:", ["Grover Search on Graph", "VQE Molecular Simulation"], horizontal=True)

                if demo_choice == "Grover Search on Graph":
                    st.markdown("#### Grover's Quadratic Speedup $O(\\sqrt{N})$ Unstructured Search")
                    search_query = st.text_input("Entity or concept to search in graph:", value="quantum")
                    if st.button("Run Grover Quantum Search"):
                        from backend.quantum.grover_search import grover_search
                        res = grover_search.search(
                            items=nodes if nodes else [{"id": "n1", "name": "quantum"}, {"id": "n2", "name": "physics"}],
                            predicate_fn=lambda item: search_query.lower() in item.get("name", "").lower(),
                        )
                        st.json(res)

                elif demo_choice == "VQE Molecular Simulation":
                    st.markdown("#### Variational Quantum Eigensolver (VQE) for $H_2$ Ground State")
                    bond_dist = st.slider("Interatomic Bond Distance (Ångström)", min_value=0.3, max_value=2.5, value=0.74, step=0.05)
                    if st.button("Calculate Ground State Energy via VQE"):
                        from backend.quantum.vqe_simulator import vqe_simulator
                        res = vqe_simulator.simulate_ground_state(bond_distance=bond_dist)
                        st.success(f"VQE Ground State Energy: {res['vqe_ground_state_energy_hartree']} Hartree (Error: {res['absolute_error_hartree']} Ha)")
                        st.json(res)

            # Tab 7: Academic Benchmark & Paper Lab
            with tab_bench:
                st.markdown("### 📊 Quantum Advantage & Academic Benchmark Suite")
                st.markdown(
                    "Rigorous performance evaluation comparing **QAOA (XY-Mixer with Dicke states)** against "
                    "classical baselines (**Greedy**, **Simulated Annealing**, and **Exact Brute Force**)."
                )

                if st.button("🚀 Run Comparative Benchmark for this Query", key="bench_master_btn"):
                    with st.spinner("Executing QAOA vs Classical Solvers..."):
                        from backend.evaluation.benchmark import benchmark_engine
                        bench_res = benchmark_engine.run_benchmark(query=query_text.strip(), target_k=max_sources)

                        b_qaoa = bench_res["qaoa_xy_mixer"]
                        b_opt = bench_res["exact_global_optimum"]
                        b_greedy = bench_res["classical_greedy"]
                        b_sa = bench_res["classical_simulated_annealing"]

                        st.success(bench_res["quantum_advantage_summary"])

                        # Comparison metrics cards
                        bm1, bm2, bm3 = st.columns(3)
                        bm1.metric("QAOA Approx Ratio (α)", f"{b_qaoa['approximation_ratio'] * 100:.1f}%")
                        bm2.metric("QAOA Cost Energy", f"{b_qaoa['cost']:.4f}")
                        bm3.metric("Global Optimum Cost", f"{b_opt['cost']:.4f}")

                        # Comparison Table
                        df_bench = pd.DataFrame([
                            {
                                "Algorithm": "QAOA (XY-Mixer)",
                                "Solution Bitstring": b_qaoa["bitstring"],
                                "Cost Value (Lower is Better)": b_qaoa["cost"],
                                "Latency (ms)": b_qaoa["latency_ms"],
                                "APIs Selected": ", ".join(b_qaoa["selected_apis"]),
                            },
                            {
                                "Algorithm": "Exact Global (Brute Force)",
                                "Solution Bitstring": b_opt["bitstring"],
                                "Cost Value (Lower is Better)": b_opt["cost"],
                                "Latency (ms)": b_opt["latency_ms"],
                                "APIs Selected": ", ".join(b_opt["selected_apis"]),
                            },
                            {
                                "Algorithm": "Classical Simulated Annealing",
                                "Solution Bitstring": b_sa["bitstring"],
                                "Cost Value (Lower is Better)": b_sa["cost"],
                                "Latency (ms)": b_sa["latency_ms"],
                                "APIs Selected": ", ".join(b_sa["selected_apis"]),
                            },
                            {
                                "Algorithm": "Classical Greedy",
                                "Solution Bitstring": b_greedy["bitstring"],
                                "Cost Value (Lower is Better)": b_greedy["cost"],
                                "Latency (ms)": b_greedy["latency_ms"],
                                "APIs Selected": ", ".join(b_greedy["selected_apis"]),
                            },
                        ])
                        st.dataframe(df_bench, use_container_width=True)

                        # LaTeX Table Generator for arXiv
                        st.markdown("#### 📝 LaTeX Table for arXiv Paper:")
                        latex_code = f"""\\begin{{table}}[h]
\\centering
\\begin{{tabular}}{{|l|c|c|c|}}
\\hline
\\textbf{{Algorithm}} & \\textbf{{Cost}} & \\textbf{{Latency (ms)}} & \\textbf{{Approximation Ratio}} \\\\
\\hline
QAOA (XY-Mixer, $p=1$) & {b_qaoa['cost']:.4f} & {b_qaoa['latency_ms']:.1f} & {b_qaoa['approximation_ratio']:.3f} \\\\
Classical Simulated Annealing & {b_sa['cost']:.4f} & {b_sa['latency_ms']:.1f} & - \\\\
Classical Greedy & {b_greedy['cost']:.4f} & {b_greedy['latency_ms']:.1f} & - \\\\
Exact Global Optimum & {b_opt['cost']:.4f} & {b_opt['latency_ms']:.1f} & 1.000 \\\\
\\hline
\\end{{tabular}}
\\caption{{Performance comparison on {bench_res['qubits_n']}-qubit Hamiltonian for query: '{query_text.strip()}'}}
\\label{{tab:qaoa_benchmark}}
\\end{{table}}"""
                        st.code(latex_code, language="latex")

else:
    # Welcome & Architectural Overview Dashboard
    st.markdown(
        """
        <div class="quantum-card" style="margin-top: 25px;">
            <h3 style="margin-top:0; color: #38bdf8;">🧠 Welcome to Quantum Knowledge Weaver (QKW)</h3>
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.6;">
                QKW is a pioneering hybrid quantum-classical multi-source cognitive engine that reconciles
                <b>empirical scientific truth (Aql / Logic)</b> with <b>spiritual contemplation (Qalb / Sakoon)</b>.
                Using principles of atomic wave-particle duality, QAOA quantum combinatorial routing, and
                Ghazalian-Sufi psychological models, QKW weaves knowledge across 11 public repositories:
            </p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #93c5fd;">📖 Wikipedia (General Knowledge)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #a7f3d0;">📄 arXiv (Preprint Physics & Math)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #fde047;">🕌 Quran (Divine Revelation)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #fed7aa;">📜 Hadith (Prophetic Traditions)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #f472b6;">🩺 PubMed (Biomedical Sciences)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #c084fc;">🚀 NASA (Astrophysics & Space)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #67e8f9;">📚 OpenAlex (Scholarly Papers)</span>
                <span style="background: #1e293b; border: 1px solid #475569; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #86efac;">🧪 PubChem (Chemical Molecules)</span>
                <span style="background: #1e293b; border: 1px solid #38bdf8; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #38bdf8;">🌐 Google (Knowledge & News Index)</span>
                <span style="background: #1e293b; border: 1px solid #fb7185; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #fb7185;">🔬 Crossref (150M+ Peer-Reviewed DOIs)</span>
                <span style="background: #1e293b; border: 1px solid #facc15; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #facc15;">📚 Open Library (20M+ Digital Books & Philosophy)</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 15px; margin-bottom: 0;">
                👉 <b>To begin:</b> Click one of the 4 prompt buttons above or type any research question and click <b>🔍 Weave Knowledge</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption("Quantum Knowledge Weaver (QKW) • Built with FastAPI, Qiskit, Qdrant, Neo4j, Ollama, & Streamlit")

