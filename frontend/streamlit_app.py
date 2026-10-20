"""Streamlit Interactive Frontend for Quantum Knowledge Weaver (QKW).
Provides intuitive query exploration, quantum QAOA telemetry, citations, cross-referencing,
and knowledge graph visualization.
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
    page_title="Quantum Knowledge Weaver (QKW)",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern aesthetic
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
    .quantum-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
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
st.sidebar.title("Quantum Weaver")
st.sidebar.caption("Hybrid Quantum-Classical API Brain")

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
    st.sidebar.success(f"● Connected (v{health_info.get('version', '0.1.0')})")
    llm_badge = "🟢 Ready" if health_info.get("llm_connected") else "🟡 Offline / Fallback"
    st.sidebar.markdown(f"**Local LLM (Ollama):** {llm_badge}")
    st.sidebar.markdown(f"**Quantum Engine:** `{health_info.get('quantum_engine', 'QAOA')}`")
else:
    st.sidebar.warning("○ Backend Server Offline (Using In-Process Direct Engine)")

st.sidebar.markdown("---")
st.sidebar.subheader("Cognitive Mode")
brain_mode = st.sidebar.radio(
    "Architecture Selection",
    options=["🧠 Neural Brain (Heart & Brain Duality)", "⚛️ Standard QAOA Orchestrator"],
    index=0,
    help="Neural Brain balances Logic (Particle/Aql) and Spiritual Contemplation (Wave/Qalb) via background cognitive flowchart.",
)

st.sidebar.markdown("---")
st.sidebar.subheader("Quantum Router (QAOA)")
use_quantum = st.sidebar.checkbox("Enable QAOA API Routing", value=True)
max_sources = st.sidebar.slider("Target API Budget (K)", min_value=1, max_value=8, value=3)
mixer_type = st.sidebar.selectbox(
    "QAOA Mixer Hamiltonian",
    options=["xy_mixer", "standard"],
    index=0,
    format_func=lambda x: "XY-Mixer (Excitation-Preserving Dicke State)" if x == "xy_mixer" else "Standard Transverse Mixer (X)",
    help="XY-Mixer mathematically guarantees exactly K APIs are chosen without penalty tuning.",
)

# Selective API overrides across all 8 integrated repositories
available_apis = ["wikipedia", "arxiv", "quran", "hadith", "pubmed", "nasa", "openalex", "pubchem"]
force_selection = st.sidebar.multiselect(
    "Force Specific APIs (Optional)",
    options=available_apis,
    default=[],
    help="Leave empty for autonomous QAOA optimization",
)

# Header
st.title("⚛️ Quantum Knowledge Weaver (QKW)")
st.markdown(
    "Synthesizing authoritative answers across **Wikipedia**, **arXiv**, **Quran**, **Hadith**, **PubMed**, "
    "**NASA**, **OpenAlex**, and **PubChem** using **QAOA quantum routing**, **semantic cross-referencing**, and **anti-hallucinatory LLM synthesis**."
)

# Sample Queries
st.markdown("##### 💡 Try an Example Prompt:")
col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
sample_query = None

if col_ex1.button("🔬 Quantum Physics & Interconnectedness", use_container_width=True):
    sample_query = "What does modern physics say about quantum entanglement and interconnectedness, and how does classical thought or theology reflect on universal unity?"

if col_ex2.button("🏥 Medicine, Hygiene & Traditions", use_container_width=True):
    sample_query = "How do modern medical research and prophetic traditions approach medicine, hygiene, and disease treatment?"

if col_ex3.button("🌌 NASA Astrophysics & Deep Space", use_container_width=True):
    sample_query = "What are the latest observations and discoveries about black holes, galaxies, and cosmology from space telescopes?"

if col_ex4.button("🧪 Molecular Drugs & Chemical Compounds", use_container_width=True):
    sample_query = "What is the molecular formula, synthesis, and mechanism of action of penicillin in treating bacterial infections?"

# Main Query Input
query_text = st.text_input(
    "Enter your research inquiry:",
    value=sample_query if sample_query else "",
    placeholder="Ask anything across science, medicine, encyclopedic knowledge, or theology...",
)

col_btn, col_clear = st.columns([1, 6])
execute_search = col_btn.button("🔍 Weave Knowledge", type="primary", use_container_width=True)

if execute_search and query_text.strip():
    is_neural_mode = "Neural Brain" in brain_mode

    with st.spinner("Processing through Neural-Quantum Dual-Hemisphere Cognitive Architecture..." if is_neural_mode else "Executing QAOA Quantum Routing & Multi-Source Retrieval..."):
        response_data = None
        brain_response = None
        error_msg = None

        if is_neural_mode:
            # 1. Neural Brain Mode (Heart & Brain Duality)
            if backend_online:
                try:
                    res = requests.post(f"{api_backend_url}/brain/think", json={"text": query_text.strip()}, timeout=40.0)
                    if res.status_code == 200:
                        brain_response = res.json()
                    else:
                        error_msg = f"HTTP {res.status_code}: {res.text}"
                except Exception as e:
                    error_msg = str(e)

            if not brain_response:
                try:
                    import asyncio
                    from backend.neural_brain.engine import neural_brain
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    res_obj = loop.run_until_complete(neural_brain.think_and_reply(query_text.strip()))
                    brain_response = res_obj.model_dump()
                except Exception as e:
                    error_msg = f"In-process Neural Brain error: {str(e)}"

        else:
            # 2. Standard QAOA Orchestrator Mode
            payload = {
                "text": query_text.strip(),
                "use_quantum": use_quantum,
                "max_sources": max_sources,
                "force_apis": force_selection if force_selection else None,
            }

            if backend_online:
                try:
                    res = requests.post(f"{api_backend_url}/query", json=payload, timeout=30.0)
                    if res.status_code == 200:
                        response_data = res.json()
                    else:
                        error_msg = f"HTTP {res.status_code}: {res.text}"
                except Exception as e:
                    error_msg = str(e)

            if not response_data:
                try:
                    import asyncio
                    from backend.orchestrator.engine import orchestrator
                    from backend.orchestrator.models import QueryRequest

                    req = QueryRequest(
                        text=query_text.strip(),
                        use_quantum=use_quantum,
                        max_sources=max_sources,
                        force_apis=force_selection if force_selection else None,
                    )
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    res_obj = loop.run_until_complete(orchestrator.execute_query(req))
                    response_data = res_obj.model_dump()
                except Exception as e:
                    error_msg = f"In-process execution error: {str(e)}"

        # -------------------------------------------------------------
        # Render Results
        # -------------------------------------------------------------
        if error_msg and not brain_response and not response_data:
            st.error(f"Execution Error: {error_msg}")

        elif brain_response:
            # RENDER NEURAL BRAIN DUALITY MODE
            duality = brain_response.get("duality_state", {})
            flow = brain_response.get("cognitive_flow", {})

            # Duality Superposition Header Card
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
                            border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                    <h3 style="margin-top:0; color: #a855f7;">⚛️ Wave-Particle Atomic Duality State: |Ψ⟩ = α|Aql⟩ + β|Qalb⟩</h3>
                    <p style="color: #cbd5e1; margin-bottom: 8px;">
                        Mimicking the fundamental duality of matter & energy: balancing <b>Aql (Particle/Logic/Fact)</b>
                        with <b>Qalb (Wave/Spirit/Tafakkur)</b>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Duality Metrics
            dm1, dm2, dm3, dm4 = st.columns(4)
            dm1.metric("Dominant Resonance", duality.get("dominant_state", "Equilibrium"))
            dm2.metric("Particle |Aql|² (Logic)", f"{duality.get('particle_probability', 0) * 100:.1f}%")
            dm3.metric("Wave |Qalb|² (Spirit)", f"{duality.get('wave_probability', 0) * 100:.1f}%")
            dm4.metric("Cognitive Latency", f"{flow.get('total_synaptic_latency_ms', 0):.1f} ms")

            # Dual progress ratio bar
            particle_pct = duality.get("particle_probability", 0.5)
            st.markdown(f"**Aql (Particle / Logic) vs. Qalb (Wave / Contemplation) Balance:**")
            st.progress(float(particle_pct), text=f"Left: Aql/Brain {particle_pct*100:.1f}% ⟵ Harmonious Equilibrium ⟶ Right: Qalb/Heart {(1-particle_pct)*100:.1f}%")

            # Brain Tabs
            tab_syn, tab_flow, tab_tafakkur, tab_emp, tab_bench = st.tabs([
                "⚖️ Harmonious Synthesis",
                "🧠 Background Cognitive Flowchart",
                "🕊️ Tafakkur & Spiritual Dimension",
                "📚 Empirical Citations & Qubits",
                "📊 Academic Benchmark & Paper Lab",
            ])

            with tab_syn:
                st.markdown(brain_response.get("harmonious_synthesis", ""))

            with tab_flow:
                st.markdown("### 🧠 Background Neuro-Cognitive Reasoning Flowchart")
                st.markdown(
                    "Trace of the brain's internal reasoning from sensory intake (Thalamus) through "
                    "parallel dual-hemispheric processing and corpus callosum synaptic bridge:"
                )

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

            with tab_tafakkur:
                st.markdown("### 🕊️ Tafakkur: Contemplative Spiritual Psychology")
                st.markdown(brain_response.get("tafakkur_reflection", ""))
                st.info("The Tafakkur engine synthesizes Islamic psychology, Ghazalian wisdom, and Sufi nafs models to provide emotional grounding and self-reflection.")

            with tab_emp:
                st.markdown("### 📚 Authoritative Multi-Source Citations (8 APIs)")
                citations = brain_response.get("citations", [])
                for i, cit in enumerate(citations, 1):
                    with st.expander(f"[{i}] {cit.get('source_name')} — {cit.get('title')}", expanded=True):
                        st.markdown(f"**Snippet:** *\"{cit.get('snippet')}\"*")
                        if cit.get("url"):
                            st.markdown(f"🔗 **URL:** [{cit.get('url')}]({cit.get('url')})")

            with tab_bench:
                st.markdown("### 📊 Quantum Advantage & Academic Benchmark Suite")
                if st.button("🚀 Run Comparative Benchmark for this Query", key="bench_neural_btn"):
                    with st.spinner("Executing QAOA vs Classical Solvers..."):
                        from backend.evaluation.benchmark import benchmark_engine
                        bench_res = benchmark_engine.run_benchmark(query=query_text.strip(), target_k=max_sources)
                        st.json(bench_res)

        elif response_data:
            # RENDER STANDARD QAOA ORCHESTRATOR MODE
            # Display Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Latency", f"{response_data.get('total_latency_ms', 0):.1f} ms")
            m2.metric("Citations Retrieved", len(response_data.get("citations", [])))
            m3.metric("Cross-References", len(response_data.get("cross_references", [])))
            m4.metric("Memory Cache", "Hit (Fast)" if response_data.get("cached") else "Miss (Fresh)")

            # Tabbed View
            tab_ans, tab_quantum, tab_cross, tab_graph, tab_bench = st.tabs([
                "📄 Synthesized Answer & Citations",
                "⚛️ Quantum QAOA Telemetry",
                "🔗 Cross-Reference Matrix",
                "🧠 Knowledge Graph & Demos",
                "📊 Academic Benchmark & Paper Lab",
            ])

            # Tab 1: Answer & Citations
            with tab_ans:
                st.markdown("### Synthesized Knowledge")
                st.markdown(response_data.get("synthesized_answer", ""))

                st.markdown("---")
                st.markdown("### 📚 Authoritative Citations")
                citations = response_data.get("citations", [])
                if not citations:
                    st.info("No direct citations were returned for this query.")
                else:
                    for i, cit in enumerate(citations, 1):
                        with st.expander(f"[{i}] {cit.get('source_name')} — {cit.get('title')}", expanded=True):
                            st.markdown(f"**Snippet:** *\"{cit.get('snippet')}\"*")
                            if cit.get("url"):
                                st.markdown(f"🔗 **URL:** [{cit.get('url')}]({cit.get('url')})")
                            st.caption(f"Relevance Score: {cit.get('relevance_score', 0):.2f}")

            # Tab 2: Quantum Routing Telemetry
            with tab_quantum:
                st.markdown("### ⚛️ QAOA API Selection Optimization")
                q_details = response_data.get("quantum_routing")
                if q_details:
                    qc1, qc2, qc3 = st.columns(3)
                    qc1.metric("Qubits Used", q_details.get("qubits_count", 0))
                    qc2.metric("Quantum Energy <H_C>", f"{q_details.get('quantum_energy', 0):.4f}")
                    qc3.metric("QAOA Latency", f"{q_details.get('execution_time_ms', 0):.2f} ms")

                    st.markdown(f"**Quantum Backend:** `{q_details.get('backend_used')}`")
                    st.markdown(f"**Candidate APIs (Qubit Register):** {', '.join(q_details.get('qubo_variables', []))}")
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
                    st.info("Quantum routing was bypassed or ran in manual override mode.")

            # Tab 3: Cross Reference Matrix
            with tab_cross:
                st.markdown("### 🔗 Semantic Cross-Referencing & Contradiction Detection")
                cross_refs = response_data.get("cross_references", [])
                if not cross_refs:
                    st.info("No cross-domain connections detected between the retrieved sources.")
                else:
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

            # Tab 4: Knowledge Graph & Demos
            with tab_graph:
                st.markdown("### 🧠 Knowledge Graph Entities & Relations")
                from backend.memory.neo4j_store import graph_memory
                graph_data = graph_memory.get_graph_data()

                nodes = graph_data.get("nodes", [])
                edges = graph_data.get("edges", [])

                gc1, gc2 = st.columns(2)
                with gc1:
                    st.markdown(f"**Total Entities / Nodes:** {len(nodes)}")
                    if nodes:
                        st.dataframe(pd.DataFrame(nodes)[["id", "label", "name"]], height=200, use_container_width=True)
                with gc2:
                    st.markdown(f"**Total Graph Relationships:** {len(edges)}")
                    if edges:
                        st.dataframe(pd.DataFrame(edges)[["source", "relationship", "target"]], height=200, use_container_width=True)

                st.markdown("---")
                st.markdown("### 🔬 Interactive Quantum Algorithms Lab")

                demo_choice = st.radio("Choose Quantum Module Demo:", ["Grover Search on Graph", "VQE Molecular Simulation"], horizontal=True)

                if demo_choice == "Grover Search on Graph":
                    st.markdown("#### Grover's Quadratic Speedup $O(\\sqrt{N})$ Search")
                    search_query = st.text_input("Entity or term to search in graph:", value="quantum")
                    if st.button("Run Grover Quantum Search"):
                        from backend.quantum.grover_search import grover_search
                        res = grover_search.search(
                            items=nodes if nodes else [{"id": "n1", "name": "quantum"}, {"id": "n2", "name": "physics"}],
                            predicate_fn=lambda item: search_query.lower() in item.get("name", "").lower(),
                        )
                        st.json(res)

                elif demo_choice == "VQE Molecular Simulation":
                    st.markdown("#### Variational Quantum Eigensolver (VQE) for $H_2$")
                    bond_dist = st.slider("Interatomic Bond Distance (Ångström)", min_value=0.3, max_value=2.5, value=0.74, step=0.05)
                    if st.button("Calculate Ground State Energy via VQE"):
                        from backend.quantum.vqe_simulator import vqe_simulator
                        res = vqe_simulator.simulate_ground_state(bond_distance=bond_dist)
                        st.success(f"VQE Ground State Energy: {res['vqe_ground_state_energy_hartree']} Hartree (Error: {res['absolute_error_hartree']} Ha)")
                        st.json(res)

            # Tab 5: Academic Benchmark & Paper Metrics
            with tab_bench:
                st.markdown("### 📊 Quantum Advantage & Academic Benchmark Suite")
                st.markdown(
                    "Rigorous performance evaluation comparing **QAOA (XY-Mixer with Dicke states)** against "
                    "classical baselines (**Greedy**, **Simulated Annealing**, and **Exact Brute Force**)."
                )

                if st.button("🚀 Run Comparative Benchmark for this Query"):
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

st.markdown("---")
st.caption("Quantum Knowledge Weaver (QKW) • Built with FastAPI, Qiskit, Qdrant, Neo4j, Ollama, & Streamlit")
