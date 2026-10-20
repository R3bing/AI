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
st.sidebar.subheader("Quantum Router (QAOA)")
use_quantum = st.sidebar.checkbox("Enable QAOA API Routing", value=True)
max_sources = st.sidebar.slider("Target API Budget (K)", min_value=1, max_value=5, value=3)

# Selective API overrides
available_apis = ["wikipedia", "arxiv", "quran", "hadith", "pubmed"]
force_selection = st.sidebar.multiselect(
    "Force Specific APIs (Optional)",
    options=available_apis,
    default=[],
    help="Leave empty for autonomous QAOA optimization",
)

# Header
st.title("⚛️ Quantum Knowledge Weaver (QKW)")
st.markdown(
    "Synthesizing authoritative answers across **Wikipedia**, **arXiv**, **Quran**, **Hadith**, and **PubMed** "
    "using **QAOA quantum routing**, **semantic cross-referencing**, and **anti-hallucinatory LLM synthesis**."
)

# Sample Queries
st.markdown("##### 💡 Try an Example Prompt:")
col_ex1, col_ex2, col_ex3 = st.columns(3)
sample_query = None

if col_ex1.button("🔬 Quantum Computing & Interconnectedness", use_container_width=True):
    sample_query = "What does modern physics say about quantum entanglement and interconnectedness, and how does classical thought or theology reflect on universal unity?"

if col_ex2.button("🏥 Disease Treatment & Healthcare Traditions", use_container_width=True):
    sample_query = "How do modern medical research and prophetic traditions approach medicine, hygiene, and disease treatment?"

if col_ex3.button("⚡ Algorithmic Optimization & AI QAOA", use_container_width=True):
    sample_query = "What are the latest algorithmic advances in quantum approximate optimization algorithms (QAOA) for combinatorial graph routing?"

# Main Query Input
query_text = st.text_input(
    "Enter your research inquiry:",
    value=sample_query if sample_query else "",
    placeholder="Ask anything across science, medicine, encyclopedic knowledge, or theology...",
)

col_btn, col_clear = st.columns([1, 6])
execute_search = col_btn.button("🔍 Weave Knowledge", type="primary", use_container_width=True)

if execute_search and query_text.strip():
    with st.spinner("Executing QAOA Quantum Routing & Multi-Source Retrieval..."):
        response_data = None
        error_msg = None

        payload = {
            "text": query_text.strip(),
            "use_quantum": use_quantum,
            "max_sources": max_sources,
            "force_apis": force_selection if force_selection else None,
        }

        # Try HTTP backend first
        if backend_online:
            try:
                res = requests.post(f"{api_backend_url}/query", json=payload, timeout=30.0)
                if res.status_code == 200:
                    response_data = res.json()
                else:
                    error_msg = f"HTTP {res.status_code}: {res.text}"
            except Exception as e:
                error_msg = str(e)

        # In-process direct fallback if backend not running
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

        if error_msg and not response_data:
            st.error(f"Execution Error: {error_msg}")
        elif response_data:
            # Display Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Latency", f"{response_data.get('total_latency_ms', 0):.1f} ms")
            m2.metric("Citations Retrieved", len(response_data.get("citations", [])))
            m3.metric("Cross-References", len(response_data.get("cross_references", [])))
            m4.metric("Memory Cache", "Hit (Fast)" if response_data.get("cached") else "Miss (Fresh)")

            # Tabbed View
            tab_ans, tab_quantum, tab_cross, tab_graph = st.tabs([
                "📄 Synthesized Answer & Citations",
                "⚛️ Quantum QAOA Telemetry",
                "🔗 Cross-Reference Matrix",
                "🧠 Knowledge Graph & Demos",
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

st.markdown("---")
st.caption("Quantum Knowledge Weaver (QKW) • Built with FastAPI, Qiskit, Qdrant, Neo4j, Ollama, & Streamlit")
