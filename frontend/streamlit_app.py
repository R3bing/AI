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


def render_vis_network(nodes, edges):
    """Renders interactive 2D physics-based Vis.js Knowledge Graph."""
    import json
    import streamlit.components.v1 as components

    if not nodes:
        st.info("No nodes in knowledge graph memory yet. Execute queries to populate the graph.")
        return

    vis_nodes = []
    for n in nodes:
        lbl = n.get("label", "Concept")
        name = n.get("name", n.get("id", ""))
        if lbl == "Query":
            color = {"background": "#9333ea", "border": "#c084fc"}
            shape = "star"
            size = 28
        elif lbl == "Source":
            color = {"background": "#1d4ed8", "border": "#60a5fa"}
            shape = "diamond"
            size = 20
        else:
            color = {"background": "#059669", "border": "#34d399"}
            shape = "dot"
            size = 14
        vis_nodes.append({
            "id": n.get("id"),
            "label": name[:28] + ("..." if len(name) > 28 else ""),
            "title": f"<b>{lbl}</b><br>{name}",
            "color": color,
            "shape": shape,
            "size": size,
            "font": {"color": "#f1f5f9", "size": 12, "face": "sans-serif"},
        })

    vis_edges = []
    for e in edges:
        rel = e.get("relationship", "")
        if rel == "CORROBORATES":
            edge_color = "#10b981"
            width = 3
        elif rel == "CONTRADICTS":
            edge_color = "#ef4444"
            width = 3
        elif rel == "RETRIEVED":
            edge_color = "#a855f7"
            width = 2
        else:
            edge_color = "#64748b"
            width = 1
        vis_edges.append({
            "from": e.get("source"),
            "to": e.get("target"),
            "label": rel,
            "color": {"color": edge_color, "highlight": "#38bdf8"},
            "font": {"color": "#94a3b8", "size": 10},
            "arrows": "to",
            "width": width,
        })

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
      <style>
        body {{ margin: 0; padding: 0; background-color: #0b0f19; }}
        #network {{
          width: 100%;
          height: 480px;
          background: #0f172a;
          border: 1px solid #334155;
          border-radius: 12px;
        }}
      </style>
    </head>
    <body>
      <div id="network"></div>
      <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(vis_nodes)});
        var edges = new vis.DataSet({json.dumps(vis_edges)});
        var container = document.getElementById('network');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
          physics: {{
            barnesHut: {{ gravitationalConstant: -2500, springLength: 95, springConstant: 0.04 }}
          }},
          interaction: {{ hover: true, tooltipDelay: 100, zoomView: true, dragView: true }}
        }};
        var network = new vis.Network(container, data, options);
      </script>
    </body>
    </html>
    """
    components.html(html_content, height=500)


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

# Multi-Provider AI Brain Settings
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Multi-Provider AI Brain")
llm_provider_choice = st.sidebar.selectbox(
    "Synthesis Engine",
    options=["auto", "deepseek", "deepseek_local", "gemini", "groq", "openai", "ollama", "cognitive_local"],
    index=0,
    format_func=lambda x: {
        "auto": "⚡ Auto (DeepSeek → Gemini → Groq → OpenAI → Ollama)",
        "deepseek": "⚡ DeepSeek Cloud (V3 / R1 Reasoner)",
        "deepseek_local": "🦙 DeepSeek-R1 (Local Ollama)",
        "gemini": "✨ Google Gemini (Flash / Pro)",
        "groq": "⚡ Groq (Llama 3.3 70B <400ms)",
        "openai": "🟢 OpenAI (GPT-4o)",
        "ollama": "🦙 Ollama (Local Daemon)",
        "cognitive_local": "🧠 Native Cognitive Engine (Zero-Key)",
    }.get(x, x),
)

with st.sidebar.expander("🔑 Cloud API Keys (Optional)", expanded=False):
    ui_deepseek_key = st.text_input("DeepSeek API Key", type="password", value=os.getenv("DEEPSEEK_API_KEY", ""))
    ui_gemini_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    ui_groq_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    ui_openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))

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
st.markdown("##### 💡 Explore with a Complex / Multi-Clause Inquiry:")
col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
# Session state initialization
if 'query_input' not in st.session_state:
    st.session_state['query_input'] = ''
if 'brain_response' not in st.session_state:
    st.session_state['brain_response'] = None
if 'current_query' not in st.session_state:
    st.session_state['current_query'] = ''

if col_ex1.button('🔬 Quantum Physics & Unity', use_container_width=True):
    st.session_state['query_input'] = 'What does modern physics say about quantum entanglement and cosmic expansion, and how do classical philosophy and theological scripture reflect on universal creation?'

if col_ex2.button('🏥 Medicine, Hygiene & Sunnah', use_container_width=True):
    st.session_state['query_input'] = 'Could you please explain in detail what modern biomedical research says about preventive hygiene and how prophetic traditions approach disease, health, and holistic well-being?'

if col_ex3.button('🌌 NASA Astrophysics & Origins', use_container_width=True):
    st.session_state['query_input'] = 'What are the latest discoveries about the cosmic microwave background radiation and black holes from space telescopes like Euclid and Hubble?'

if col_ex4.button('🧪 Molecular Drugs & Biology', use_container_width=True):
    st.session_state['query_input'] = 'What is the molecular formula, chemical synthesis, and mechanism of action of penicillin in treating bacterial infections?'

# Main Query Form (allows both clicking button AND pressing Enter on keyboard)
with st.form('weave_knowledge_form', clear_on_submit=False):
    query_text = st.text_input(
        'Enter your research or contemplation inquiry (long natural sentences welcome):',
        value=st.session_state.get('query_input', ''),
        placeholder='Ask anything across science, medicine, existential philosophy, cosmology, or theology in natural conversational sentences...',
    )
    col_btn, col_clear, _ = st.columns([2, 1, 4])
    execute_search = col_btn.form_submit_button('🔍 Weave Knowledge', type='primary', use_container_width=True)
    clear_btn = col_clear.form_submit_button('🔄 Reset', use_container_width=True)

if clear_btn:
    st.session_state['brain_response'] = None
    st.session_state['query_input'] = ''
    st.session_state['current_query'] = ''
    st.rerun()

st.session_state['query_input'] = query_text

if execute_search and query_text.strip():
    brain_response = None
    error_msg = None

    with st.status("🧠 Neuro-Quantum Cognitive Brain Processing...", expanded=True) as status_box:
        status_box.write("🧩 **Phase 1: Prefrontal Intake** — Deconstructing inquiry and extracting core semantic entities...")
        status_box.write("⚛️ **Phase 2: Quantum Router** — Calculating QUBO Hamiltonian & QAOA statevector (11 Qubits)...")
        status_box.write(f"🌐 **Phase 3: Multi-Source Dispatch** — Asynchronously querying knowledge repositories...")

        runtime_api_keys = {
            "deepseek": ui_deepseek_key.strip() if ui_deepseek_key else "",
            "gemini": ui_gemini_key.strip() if ui_gemini_key else "",
            "groq": ui_groq_key.strip() if ui_groq_key else "",
            "openai": ui_openai_key.strip() if ui_openai_key else "",
        }

        # 1. Try FastAPI Backend
        if backend_online:
            try:
                payload = {
                    "text": query_text.strip(),
                    "max_sources": max_sources,
                    "force_apis": force_selection if force_selection else None,
                    "use_quantum": use_quantum,
                    "mixer_type": mixer_type,
                    "llm_provider": llm_provider_choice,
                    "deepseek_api_key": ui_deepseek_key.strip() if ui_deepseek_key else None,
                    "api_keys": runtime_api_keys,
                }
                res = requests.post(f"{api_backend_url}/brain/think", json=payload, timeout=45.0)
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
                        api_keys=runtime_api_keys,
                        llm_provider=llm_provider_choice,
                        deepseek_api_key=ui_deepseek_key.strip() if ui_deepseek_key else None,
                    )
                )
                brain_response = res_obj.model_dump()
            except Exception as e:
                error_msg = f"In-process cognitive execution error: {str(e)}"

        status_box.write("🔍 **Phase 4: Semantic Cross-Reference** — Triangulating NLI contradiction & corroboration matrix...")
        status_box.write("⚖️ **Phase 5: Dual-Hemisphere Synthesis** — Merging empirical rigor (Aql) and contemplative insight (Qalb)...")
        status_box.update(label="✅ Cognitive Synthesis & Grounding Complete!", state="complete", expanded=False)

    if error_msg and not brain_response:
        st.error(f"Execution Error: {error_msg}")

    elif brain_response:
        st.session_state['brain_response'] = brain_response
        st.session_state['current_query'] = query_text.strip()

active_response = st.session_state.get('brain_response')
if active_response:
    duality = active_response.get('duality_state', {})
    flow = active_response.get('cognitive_flow', {})
    citations = active_response.get('citations', [])
    cross_refs = active_response.get('cross_references', [])
    q_details = active_response.get('quantum_telemetry', {})
    parsed_info = active_response.get('parsed_query')

    # -------------------------------------------------------------
    # Prefrontal Inquiry Deconstruction HUD
    # -------------------------------------------------------------
    if parsed_info:
        with st.expander('🧩 Prefrontal Inquiry Deconstruction (Human Brain Parser)', expanded=True):
            p_c1, p_c2 = st.columns([1, 1])
            with p_c1:
                st.markdown(f'**Cleaned Research Intent:** `{parsed_info.get("cleaned_intent")}`')
                st.markdown(f'**Epistemic Domains:** {", ".join(f"`{d}`" for d in parsed_info.get("epistemic_domains", []))}')
                st.markdown(f'**Cognitive Mode:** `{parsed_info.get("dominant_mode", "balanced").title()}`')
            with p_c2:
                st.markdown(f'**Extracted Core Concepts:** {", ".join(f"`{e}`" for e in parsed_info.get("core_entities", []))}')
                sub_qs = parsed_info.get('sub_questions', [])
                if sub_qs:
                    st.markdown('**Sub-Questions Addressed:**')
                    for sq in sub_qs[:3]:
                        st.markdown(f'- *{sq}*')

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
    # 8 Master Tabs: Unified with Autonomous NAS Closed-Loop Lab
    # -------------------------------------------------------------
    tab_syn, tab_flow, tab_quantum, tab_tafakkur, tab_citations, tab_graph, tab_bench, tab_nas = st.tabs([
        "⚖️ 1. Harmonious Synthesis",
        "🧠 2. Neuro-Cognitive Flowchart",
        "⚛️ 3. Quantum QAOA Telemetry",
        "🕊️ 4. Tafakkur & Spiritual Dimension",
        "📚 5. Citations & Cross-References",
        "🕸️ 6. Knowledge Graph & Quantum Lab",
        "📊 7. Academic Benchmark & Paper Lab",
        "🧬 8. Autonomous NAS Closed-Loop Lab",
    ])

    # Tab 1: Harmonious Synthesis
    with tab_syn:
        st.markdown("### ⚖️ The Harmonious Synthesis: Intellectual Rigor & Spiritual Sakoon")
        provider_used = brain_response.get("llm_provider_used", "Cognitive Native")
        st.caption(f"🧠 **Synthesis Engine:** `{provider_used}` • **Consulted Repositories:** {', '.join(f'`{api}`' for api in brain_response.get('apis_consulted', []))}")

        # DeepSeek-R1 Chain of Thought Trace
        cot_trace = brain_response.get("reasoning_trace")
        if cot_trace:
            with st.expander("💭 DeepSeek-R1 Deep Cognitive Chain-of-Thought (<think>)", expanded=False):
                st.info("Direct cognitive Chain-of-Thought extracted from DeepSeek-R1 reasoning trace:")
                st.markdown(f"```text\n{cot_trace}\n```")

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

        # Dual-Voice Dialogue & Audio Player (Dr. Aql vs. Shaykh Qalb)
        with st.expander("🎙️ Dual-Voice Dialectical Dialogue: Dr. Aql vs. Shaykh Qalb (Interactive Audio)", expanded=False):
            from backend.synthesis.dual_voice import dual_voice_generator
            turns = dual_voice_generator.generate_dialogue(
                query=st.session_state.get('current_query', ''),
                logical_answer=brain_response.get("logical_factual_answer", ""),
                tafakkur_reflection=brain_response.get("tafakkur_reflection", ""),
                harmonious_synthesis=brain_response.get("harmonious_synthesis", ""),
            )

            import json
            import streamlit.components.v1 as components

            # Render HTML5 Speech Synthesis Controller
            turns_json = json.dumps(turns)
            audio_controller_html = f"""
            <div style="background: #0f172a; padding: 16px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 15px;">
                <button id="playBtn" onclick="playAudio()" style="background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer;">
                    ▶️ Play Dual-Voice Contemplation Audio
                </button>
                <button id="stopBtn" onclick="stopAudio()" style="background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; margin-left: 10px;">
                    ⏹️ Stop Audio
                </button>
                <span id="speakerStatus" style="color: #94a3b8; margin-left: 15px; font-size: 0.9rem;">Ready for playback</span>
            </div>
            <script>
                const scriptTurns = {turns_json};
                let currentIdx = 0;
                let isPlaying = false;

                function stopAudio() {{
                    window.speechSynthesis.cancel();
                    isPlaying = false;
                    document.getElementById('speakerStatus').innerText = "Audio Stopped.";
                }}

                function playAudio() {{
                    window.speechSynthesis.cancel();
                    currentIdx = 0;
                    isPlaying = true;
                    speakNextTurn();
                }}

                function speakNextTurn() {{
                    if (!isPlaying || currentIdx >= scriptTurns.length) {{
                        document.getElementById('speakerStatus').innerText = "Playback Finished.";
                        isPlaying = false;
                        return;
                    }}
                    const item = scriptTurns[currentIdx++];
                    document.getElementById('speakerStatus').innerText = "Speaking: " + item.speaker;
                    const u = new SpeechSynthesisUtterance(item.text);
                    u.pitch = item.voice_pitch || 1.0;
                    u.rate = item.voice_rate || 1.0;
                    u.onend = function() {{
                        if (isPlaying) {{
                            setTimeout(speakNextTurn, 400);
                        }}
                    }};
                    window.speechSynthesis.speak(u);
                }}
            </script>
            """
            components.html(audio_controller_html, height=80)

            for t in turns:
                speaker = t["speaker"]
                if "Aql" in speaker:
                    border_color = "#3b82f6"
                    tag_bg = "#1e3a8a"
                    icon = "🔬"
                elif "Qalb" in speaker:
                    border_color = "#10b981"
                    tag_bg = "#064e3b"
                    icon = "🕊️"
                else:
                    border_color = "#a855f7"
                    tag_bg = "#581c87"
                    icon = "⚛️"

                st.markdown(
                    f"""
                    <div style="background: #1e293b; border-left: 4px solid {border_color}; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                        <span style="background: {tag_bg}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 700;">
                            {icon} {speaker} ({t['role']})
                        </span>
                        <p style="color: #f1f5f9; margin-top: 10px; margin-bottom: 0; line-height: 1.6; font-size: 0.95rem;">
                            "{t['text']}"
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

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
    B -->|Particle Stream α| C1["3. Left Hemisphere (Aql / Logic)<br>QAOA 11-API Quantum Retrieval"]:::leftBrain
    B -->|Wave Stream β| C2["4. Right Hemisphere (Qalb / Spirit)<br>Tafakkur Contemplation & Nafs Resonator"]:::rightBrain
    C1 --> D["5. Corpus Callosum Synaptic Bridge<br>NLI Semantic Cross-Referencing"]:::bridge
    C2 --> D
    D --> E["6. Prefrontal Cortex<br>Harmonious Balanced Synthesis"]:::cortex
```
            """
        )

        # DeepSeek CoT inside Flowchart if present
        if brain_response.get("reasoning_trace"):
            with st.expander("💭 Phase 6 Reasoning Detail: DeepSeek-R1 / CoT Trace", expanded=False):
                st.markdown(f"```text\n{brain_response['reasoning_trace']}\n```")

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
        st.markdown("### ⚛️ QAOA API Selection Optimization & 3D Bloch Sphere")
        if q_details:
            qc1, qc2, qc3 = st.columns(3)
            qc1.metric("Qubits Used", q_details.get("qubits_count", 0))
            qc2.metric("Quantum Energy <H_C>", f"{q_details.get('quantum_energy', 0):.4f}")
            qc3.metric("QAOA Latency", f"{q_details.get('execution_time_ms', 0):.2f} ms")

            st.markdown(f"**Quantum Algorithm:** `{q_details.get('algorithm')}`")
            st.markdown(f"**Quantum Backend:** `{q_details.get('backend_used')}`")
            st.markdown(f"**Candidate APIs ({q_details.get('qubits_count', 11)}-Qubit Register):** {', '.join(q_details.get('qubo_variables', []))}")
            st.markdown(f"**Winning APIs Selected ($x_i=1$):** {', '.join(q_details.get('selected_apis', []))}")

            # 3D Interactive Bloch Sphere
            st.markdown("---")
            st.markdown("#### 🌐 3D Interactive Quantum Bloch Sphere in Hilbert Space")
            st.caption("Visualizing the query's wave-particle superposition state: |Ψ⟩ = α|Aql (North Pole)⟩ + β|Qalb (South Pole)⟩")
            try:
                from backend.quantum.bloch_sphere import create_bloch_sphere_figure
                bloch_fig = create_bloch_sphere_figure(
                    particle_prob=duality.get("particle_probability", 0.5),
                    wave_prob=duality.get("wave_probability", 0.5),
                    entropy_score=duality.get("entropy_score", 0.5),
                    dominant_state=duality.get("dominant_state", "Equilibrium"),
                )
                st.plotly_chart(bloch_fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not render 3D Bloch sphere: {e}")

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
        st.markdown("### 📚 Authoritative Citations (Retrieved from 11 Repositories)")
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

        graph_view_mode = st.radio(
            "Graph Visualization Engine:",
            ["🌌 3D Neural Constellation (Plotly 3D Galaxy)", "🕸️ 2D Physics Network (Vis.js)"],
            horizontal=True,
        )

        if graph_view_mode == "🌌 3D Neural Constellation (Plotly 3D Galaxy)":
            st.markdown("#### 🌌 3D Spherical Neural Galaxy (Rotate, Zoom, and Hover):")
            try:
                from backend.memory.graph_3d import create_3d_knowledge_graph_figure
                fig_3d = create_3d_knowledge_graph_figure(graph_data)
                st.plotly_chart(fig_3d, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not render 3D Galaxy: {e}")
                render_vis_network(nodes, edges)
        else:
            st.markdown("#### 🌐 Dynamic Physics-Based Knowledge Network (Drag & Explore):")
            render_vis_network(nodes, edges)

        st.markdown("---")
        gc1, gc2 = st.columns(2)
        with gc1:
            st.markdown(f"**Total Entities / Nodes in Memory:** `{len(nodes)}`")
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

    # Tab 8: Autonomous NAS Closed-Loop Lab
    with tab_nas:
        st.markdown("### 🧬 Autonomous Neural Architecture Search (NAS) — 5-Step Closed-Loop Engine")
        st.markdown(
            "An autonomous architectural self-evolution cycle connecting **Meta-Design, Instantiation, "
            "Empirical Fitting, Validation, and Policy Gradient Feedback** into a continuous learning loop:"
        )

        st.markdown(
            """
```mermaid
graph LR
    classDef step1 fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#fff;
    classDef step2 fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef step3 fill:#78350f,stroke:#fbbf24,stroke-width:2px,color:#fff;
    classDef step4 fill:#581c87,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef step5 fill:#831843,stroke:#f472b6,stroke-width:2px,color:#fff;

    S1["<b>1. Controller AI</b><br>Architecture Proposal"]:::step1 --> S2["<b>2. Child Model</b><br>Instantiation & Compilation"]:::step2
    S2 --> S3["<b>3. Model Training</b><br>Empirical Fitting"]:::step3
    S3 --> S4["<b>4. Performance Evaluation</b><br>Accuracy & Latency"]:::step4
    S4 --> S5["<b>5. Feedback Loop</b><br>REINFORCE Policy Update"]:::step5
    S5 -->|Advantage: R - b| S1
```
            """
        )

        st.markdown("#### ⚙️ NAS Closed-Loop Configuration")
        nas_col1, nas_col2, nas_col3 = st.columns(3)
        with nas_col1:
            nas_strat = st.selectbox(
                "Controller AI Strategy",
                ["autoregressive_rnn", "transformer_sampler", "evolutionary_genetic"],
                format_func=lambda x: {
                    "autoregressive_rnn": "🧠 Autoregressive RNN (Zoph & Le)",
                    "transformer_sampler": "✨ Transformer Structural Sampler",
                    "evolutionary_genetic": "🧬 Evolutionary Genetic Agent",
                }.get(x, x),
            )
        with nas_col2:
            nas_layers = st.slider("Child Network Layer Range", min_value=2, max_value=8, value=(3, 5))
        with nas_col3:
            nas_epochs = st.slider("Empirical Fitting Epochs per Child", min_value=1, max_value=6, value=3)

        btn_col1, btn_col2, _ = st.columns([2, 2, 3])
        run_cycle_btn = btn_col1.button("🚀 Execute 5-Step Closed-Loop Cycle", type="primary", use_container_width=True)
        run_exp_btn = btn_col2.button("🧬 Run 3-Cycle Autonomous NAS Experiment", use_container_width=True)

        # Session state for NAS results
        if "last_nas_cycle" not in st.session_state:
            st.session_state["last_nas_cycle"] = None
        if "last_nas_exp" not in st.session_state:
            st.session_state["last_nas_exp"] = None

        if run_cycle_btn:
            with st.spinner("Executing 5-Step NAS Cycle (Proposal ➔ Instantiation ➔ Training ➔ Evaluation ➔ Feedback)..."):
                try:
                    from backend.nas.orchestrator import nas_orchestrator
                    from backend.nas.models import ArchitectureProposalRequest, SearchStrategy
                    req = ArchitectureProposalRequest(
                        strategy=SearchStrategy(nas_strat),
                        min_layers=nas_layers[0],
                        max_layers=nas_layers[1],
                        input_dim=64,
                        output_dim=10,
                    )
                    cycle_res = nas_orchestrator.run_single_cycle(request=req, epochs=nas_epochs)
                    st.session_state["last_nas_cycle"] = cycle_res.model_dump()
                    st.success(f"✅ Cycle {cycle_res.cycle_index} completed in {cycle_res.total_cycle_time_ms:.1f} ms!")
                except Exception as e:
                    st.error(f"NAS Cycle error: {e}")

        if run_exp_btn:
            with st.spinner("Running 3-Cycle Autonomous NAS Self-Evolution Experiment..."):
                try:
                    from backend.nas.orchestrator import nas_orchestrator
                    from backend.nas.models import ArchitectureProposalRequest, SearchStrategy
                    req = ArchitectureProposalRequest(
                        strategy=SearchStrategy(nas_strat),
                        min_layers=nas_layers[0],
                        max_layers=nas_layers[1],
                        input_dim=64,
                        output_dim=10,
                    )
                    exp_res = nas_orchestrator.run_experiment(num_cycles=3, request=req, epochs_per_child=nas_epochs)
                    st.session_state["last_nas_exp"] = exp_res.model_dump()
                    st.success("✅ Multi-cycle NAS experiment completed! Pareto frontier updated.")
                except Exception as e:
                    st.error(f"NAS Experiment error: {e}")

        # Render Active Cycle Details
        active_cycle = st.session_state.get("last_nas_cycle")
        if active_cycle:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Cycle Index", f"#{active_cycle.get('cycle_index')}")
            c2.metric("Validation Accuracy", f"{active_cycle['step_4_evaluation']['val_accuracy'] * 100:.1f}%")
            c3.metric("Multi-Objective Fitness", f"{active_cycle['step_4_evaluation']['fitness_score']:.4f}")
            c4.metric("Advantage (R - b)", f"{active_cycle['step_5_feedback']['advantage']:+.4f}")

            st.markdown("---")
            st.markdown("#### 🔍 Step-by-Step Cycle Audit:")

            # Step 1
            with st.expander(f"1️⃣ Step 1: Controller AI Architecture Proposal — {active_cycle['step_1_proposal']['name']}", expanded=True):
                p1 = active_cycle['step_1_proposal']
                st.markdown(f"**Strategy Used:** `{p1['strategy_used']}` • **Sampled Depth:** `{p1['depth']} blocks` • **Theoretical Params:** `{p1['estimated_parameters']:,}`")
                st.markdown(f"**Sampled Hyperparameters:** `{p1['hyperparameters']}`")
                st.markdown("**Sampled Neural Building Blocks:**")
                for b in p1['blocks']:
                    st.markdown(f"- **{b['block_id']}**: `{b['block_type']}` ({b['in_features']} ➔ {b['out_features']}) | act=`{b['activation']}` | norm=`{b['normalization']}` | skips=`{b['skip_connections']}`")

            # Step 2
            with st.expander("2️⃣ Step 2: Child Model Concrete Instantiation & Compilation", expanded=True):
                s2 = active_cycle['step_2_instantiation']
                st.markdown(f"**Compilation Status:** `{s2.get('status')}`")
                st.markdown(f"**Tensor Input Shape:** `{s2.get('input_shape')}` ➔ **Tensor Output Shape:** `{s2.get('output_shape')}`")
                st.markdown(f"**Concrete PyTorch Parameter Count:** `{s2.get('total_trainable_params', 0):,}`")
                st.markdown(f"**Skip Residual Adapters Initialized:** `{s2.get('skip_adapters_count', 0)}`")

            # Step 3
            with st.expander("3️⃣ Step 3: Child Model Dataset Training (Empirical Fitting)", expanded=True):
                s3 = active_cycle['step_3_training']
                st.markdown(f"**Epochs Fitted:** `{s3.get('epochs_trained')}` • **Final Loss:** `{s3.get('final_train_loss'):.4f}` • **Train Accuracy:** `{s3.get('train_accuracy', 0)*100:.1f}%` • **Fitting Time:** `{s3.get('training_time_ms', 0):.1f} ms`")
                if s3.get('loss_history'):
                    df_loss = pd.DataFrame({"Epoch Loss": s3['loss_history']})
                    st.line_chart(df_loss)

            # Step 4
            with st.expander("4️⃣ Step 4: Performance Evaluation & Efficiency Benchmarking", expanded=True):
                s4 = active_cycle['step_4_evaluation']
                ec1, ec2, ec3 = st.columns(3)
                ec1.metric("Validation Accuracy", f"{s4['val_accuracy']*100:.1f}%")
                ec2.metric("Inference Latency", f"{s4['inference_latency_ms']:.2f} ms")
                ec3.metric("MACs (Multiply-Accumulates)", f"{s4['macs_count']:,}")

            # Step 5
            with st.expander("5️⃣ Step 5: Feedback Loop & Controller Policy Gradient Update", expanded=True):
                s5 = active_cycle['step_5_feedback']
                fc1, fc2, fc3 = st.columns(3)
                fc1.metric("Moving Baseline (b)", f"{s5['baseline']:.4f}")
                fc2.metric("Advantage (R - b)", f"{s5['advantage']:+.4f}")
                fc3.metric("REINFORCE Policy Loss", f"{s5['policy_loss']:.4f}")
                st.info(f"Policy weights updated successfully: {'Yes (Weights Perturbed in Advantage Direction)' if s5['policy_updated'] else 'No'}")

        # Render Multi-Cycle Experiment History if available
        active_exp = st.session_state.get("last_nas_exp")
        if active_exp and active_exp.get("pareto_frontier"):
            st.markdown("---")
            st.markdown("#### 🏆 Discovered Architectures & Pareto Frontier:")
            df_pareto = pd.DataFrame(active_exp["pareto_frontier"])
            st.dataframe(df_pareto, use_container_width=True)

            # Convergence Chart
            st.markdown("#### 📈 Reward & Validation Accuracy Convergence Across Cycles:")
            df_curves = pd.DataFrame({
                "Reward": active_exp["reward_history"],
                "Val Accuracy": active_exp["accuracy_history"],
            })
            st.line_chart(df_curves)

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

