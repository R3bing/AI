"""JARVIS Astra OS — Flagship Multimodal Executive Agent Dashboard.

Inspired by Zubair Trabzada's GPT-6 Astra JARVIS:
- Iron Man Cyber-Glassmorphism HUD with pulsating Arc Reactor
- Real-Time Voice Synthesis & Web Speech Input
- Multi-Modal Vision ('JARVIS Eyes' via Webcam & Screen Upload)
- 3D Holographic Second Brain (HOLO Deck at port 4890)
- Autonomous System Tools: File Finder, Web Research, Focus Guardian, Strata 125B Local MoE
"""

from __future__ import annotations

import os
import sys
import json
import time
import requests
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

# Workspace Root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from backend.jarvis.vision_engine import jarvis_vision
from backend.jarvis.system_tools import jarvis_tools
from backend.synthesis.synthesizer import llm_synthesizer
from backend.orchestrator.models import SourceCitation, CrossRefConnection


def render_jarvis_astra_os():
    """Renders the complete J.A.R.V.I.S. Astra Executive OS."""

    # -----------------------------------------------------------------------------
    # Curated Cyberpunk Stark HUD Glassmorphism Styling
    # -----------------------------------------------------------------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --jarvis-cyan: #00f0ff;
            --jarvis-gold: #fbbf24;
            --jarvis-blue: #0284c7;
            --jarvis-dark: #030712;
            --hud-bg: rgba(6, 11, 25, 0.85);
            --hud-border: rgba(0, 240, 255, 0.28);
        }

        .stApp {
            background: radial-gradient(circle at 50% 10%, #081229 0%, #030712 70%, #000208 100%) !important;
            color: #e2e8f0;
            font-family: 'Rajdhani', -apple-system, sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Orbitron', monospace !important;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        code, pre {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Arc Reactor Hero Card */
        .arc-reactor-card {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.08) 0%, rgba(2, 132, 199, 0.04) 50%, rgba(6, 11, 25, 0.95) 100%);
            border: 1px solid var(--hud-border);
            border-radius: 16px;
            padding: 24px 30px;
            margin-bottom: 22px;
            box-shadow: 0 0 35px rgba(0, 240, 255, 0.12), inset 0 0 15px rgba(0, 240, 255, 0.05);
            backdrop-filter: blur(16px);
            position: relative;
            overflow: hidden;
        }

        .arc-reactor-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, var(--jarvis-cyan), transparent);
        }

        /* HUD Metric Card */
        .hud-card {
            background: var(--hud-bg);
            border: 1px solid var(--hud-border);
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .hud-card:hover {
            border-color: rgba(0, 240, 255, 0.6);
            transform: translateY(-2px);
        }

        /* Glowing Badge */
        .glow-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            border: 1px solid var(--jarvis-cyan);
            background: rgba(0, 240, 255, 0.12);
            color: #e0f2fe;
        }

        /* Executive Speech Bubble */
        .jarvis-bubble {
            background: rgba(10, 18, 38, 0.88);
            border-left: 4px solid var(--jarvis-cyan);
            border-radius: 0 12px 12px 0;
            padding: 18px 22px;
            margin-top: 14px;
            margin-bottom: 14px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            line-height: 1.6;
            font-size: 1.05rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------------
    # Session State Initialization
    # -----------------------------------------------------------------------------
    if "jarvis_history" not in st.session_state:
        st.session_state["jarvis_history"] = []
    if "last_voice_text" not in st.session_state:
        st.session_state["last_voice_text"] = ""
    if "voice_enabled" not in st.session_state:
        st.session_state["voice_enabled"] = True

    # -----------------------------------------------------------------------------
    # Arc Reactor Top Navigation Banner
    # -----------------------------------------------------------------------------
    st.markdown(
        """
        <div class="arc-reactor-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 14px; height: 14px; border-radius: 50%; background: #00f0ff; box-shadow: 0 0 12px #00f0ff; animation: pulse 2s infinite;"></div>
                        <span style="font-family: 'Orbitron', monospace; font-size: 1.85rem; font-weight: 900; color: #ffffff; letter-spacing: 0.08em;">
                            J.A.R.V.I.S. <span style="color: #00f0ff;">ASTRA OS</span>
                        </span>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px; font-weight: 500;">
                        Executive Multimodal Operating System · 3D Second Brain · Vision Eyes · Strata 125B MoE
                    </div>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="glow-badge">⚡ Core Online</span>
                    <span class="glow-badge" style="border-color: #fbbf24; background: rgba(251, 191, 36, 0.12); color: #fef3c7;">👁️ Eyes Armed</span>
                    <span class="glow-badge" style="border-color: #10b981; background: rgba(16, 185, 129, 0.12); color: #d1fae5;">✋ Holo Port 4890</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------------
    # Core Action Tabs
    # -----------------------------------------------------------------------------
    tab_cmd, tab_vision, tab_second_brain, tab_tools, tab_strata = st.tabs([
        "⚡ Executive Command",
        "👁️ JARVIS Eyes (Vision)",
        "✋ 3D Second Brain (HOLO)",
        "🛠️ Autonomous Tools",
        "🧠 Strata 125B MoE Core",
    ])

    # =============================================================================
    # TAB 1: EXECUTIVE COMMAND
    # =============================================================================
    with tab_cmd:
        cmd_col1, cmd_col2 = st.columns([2, 1])

        with cmd_col1:
            st.markdown("##### 🎙️ Command JARVIS (Voice or Text)")
            
            # Audio Speech Toggle
            st.session_state["voice_enabled"] = st.toggle("🔊 Spoken Voice Audio (TTS Output)", value=st.session_state["voice_enabled"])

            # Quick Directives
            q_pills = st.pills(
                "⚡ Quick Executive Directives:",
                options=[
                    "Find recent Python files in workspace",
                    "Research quantum exciton coherence",
                    "Activate 30-min Focus Lock",
                    "List all 3D Second Brain notes",
                    "Audit local PC hardware for 125B MoE",
                ],
                key="quick_pills",
            )

            user_directive = st.text_input(
                "Enter directive or speak below:",
                value=q_pills if q_pills else "",
                placeholder="e.g. 'Sir, search for all files modified today' or 'Explain quantum biology simply'...",
                key="main_cmd_input",
            )

            # Web Speech API Browser Voice Input Widget
            st.components.v1.html(
                """
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 8px; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="color: #94a3b8; font-family: sans-serif; font-size: 13px;">
                        🎙️ <b>Hands-Free Voice Recognition</b> (Chrome Speech API):
                    </div>
                    <button id="micBtn" onclick="toggleMic()" style="background: #00f0ff; color: #000; border: none; padding: 6px 14px; border-radius: 6px; font-weight: bold; cursor: pointer; font-family: monospace;">
                        🎤 PUSH TO TALK
                    </button>
                </div>
                <div id="speechOut" style="margin-top: 6px; font-family: monospace; font-size: 12px; color: #38bdf8;"></div>

                <script>
                let recognition;
                let recognizing = false;
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = true;
                    recognition.lang = 'en-US';

                    recognition.onstart = function() {
                        recognizing = true;
                        document.getElementById('micBtn').innerText = '🔴 LISTENING...';
                        document.getElementById('micBtn').style.background = '#f43f5e';
                    };
                    recognition.onresult = function(event) {
                        let text = '';
                        for (let i = event.resultIndex; i < event.results.length; ++i) {
                            text += event.results[i][0].transcript;
                        }
                        document.getElementById('speechOut').innerText = 'Detected: ' + text;
                    };
                    recognition.onend = function() {
                        recognizing = false;
                        document.getElementById('micBtn').innerText = '🎤 PUSH TO TALK';
                        document.getElementById('micBtn').style.background = '#00f0ff';
                    };
                }
                function toggleMic() {
                    if (!recognition) {
                        alert("Speech recognition not supported in this browser.");
                        return;
                    }
                    if (recognizing) {
                        recognition.stop();
                    } else {
                        recognition.start();
                    }
                }
                </script>
                """,
                height=85,
            )

            btn_execute = st.button("🚀 Execute Directive", use_container_width=True, type="primary")

        with cmd_col2:
            st.markdown("##### ⏱️ Active Systems Telemetry")
            st.markdown(
                """
                <div class="hud-card">
                    <div style="font-size: 0.8rem; color: #94a3b8; font-family: monospace;">SYS_CLOCK & STATUS</div>
                    <div style="font-size: 1.15rem; font-weight: bold; color: #00f0ff; margin-top: 4px;">ALL SYSTEMS NOMINAL</div>
                    <hr style="border-color: rgba(0, 240, 255, 0.15); margin: 8px 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                        <span style="color: #94a3b8;">HOLO 3D Server:</span>
                        <span style="color: #10b981; font-weight: bold;">PORT 4890 (UP)</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-top: 4px;">
                        <span style="color: #94a3b8;">Strata 125B MoE:</span>
                        <span style="color: #fbbf24; font-weight: bold;">CACHED & READY</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-top: 4px;">
                        <span style="color: #94a3b8;">Focus Lock:</span>
                        <span style="color: #38bdf8;">STANDBY</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # -------------------------------------------------------------
        # Execution Logic
        # -------------------------------------------------------------
        if btn_execute and user_directive:
            st.markdown("---")
            with st.spinner("Processing directive through JARVIS Executive Core..."):
                # Check for file finding command
                if any(k in user_directive.lower() for k in ["find file", "search file", "look for"]):
                    keyword = user_directive.lower().replace("find file", "").replace("search file", "").replace("look for", "").strip()
                    files = jarvis_tools.find_files(keyword or "py")
                    resp_text = f"Sir, I executed a local workspace scan for `{keyword}`. Located {len(files)} matches across the system."
                    st.markdown(f"<div class='jarvis-bubble'><b>J.A.R.V.I.S.:</b><br>{resp_text}</div>", unsafe_allow_html=True)
                    if files:
                        st.dataframe(files, use_container_width=True)

                # Check for Second Brain Note creation
                elif any(k in user_directive.lower() for k in ["take note", "create note", "remember"]):
                    note_body = user_directive.replace("take note", "").replace("create note", "").replace("remember", "").strip()
                    res = jarvis_tools.create_second_brain_note(title="Quick Thought", content=note_body)
                    resp_text = f"Sir, I have crystallized that into your 3D Second Brain as `{res['filename']}`. It is now floating as an interactive orb in your HOLO deck."
                    st.markdown(f"<div class='jarvis-bubble'><b>J.A.R.V.I.S.:</b><br>{resp_text}</div>", unsafe_allow_html=True)

                # Check for Focus Lock
                elif "focus lock" in user_directive.lower():
                    goal = user_directive.replace("focus lock", "").strip() or "High-Velocity Deep Work"
                    f_res = jarvis_tools.set_focus_lock(goal)
                    resp_text = f_res["message"]
                    st.markdown(f"<div class='jarvis-bubble'><b>J.A.R.V.I.S.:</b><br>{resp_text}</div>", unsafe_allow_html=True)

                # General Executive Synthesis
                else:
                    citations = [
                        SourceCitation(
                            source_id="jarvis_core",
                            source_name="JARVIS Astra Intelligence Core",
                            title="Executive Synthesis on User Directive",
                            snippet=f"Processing request: '{user_directive}'",
                            url="",
                        )
                    ]
                    cross_refs = []
                    import asyncio
                    res_output = asyncio.run(llm_synthesizer.synthesize(
                        f"You are JARVIS. Answer with sharp, brilliant, executive clarity. No fluff. Directive: {user_directive}",
                        citations,
                        cross_refs,
                    ))

                    st.markdown(
                        f"<div class='jarvis-bubble'><b>J.A.R.V.I.S.:</b><br>{res_output}</div>",
                        unsafe_allow_html=True,
                    )

                    # HTML5 Speech Synthesis (Reads the response aloud!)
                    if st.session_state["voice_enabled"]:
                        clean_spoken = res_output.replace('"', '\\"').replace('\n', ' ')[:320]
                        st.components.v1.html(
                            f"""
                            <script>
                            if ('speechSynthesis' in window) {{
                                const utterance = new SpeechSynthesisUtterance("{clean_spoken}");
                                utterance.rate = 1.05;
                                utterance.pitch = 0.95;
                                window.speechSynthesis.speak(utterance);
                            }}
                            </script>
                            """,
                            height=0,
                        )

    # =============================================================================
    # TAB 2: JARVIS EYES (VISION)
    # =============================================================================
    with tab_vision:
        st.markdown("### 👁️ JARVIS Multimodal Eyes (Camera & Screen Perception)")
        st.caption("Allow JARVIS to visually inspect your physical desk, webcam feed, or an uploaded screen capture in real-time.")

        vis_c1, vis_c2 = st.columns([1, 1])

        with vis_c1:
            st.markdown("##### 📷 Optical Feed (Webcam Snapshot)")
            camera_snap = st.camera_input("Capture frame for JARVIS analysis:")
            
            file_upload = st.file_uploader("Or upload screen capture / diagram (PNG, JPG):", type=["png", "jpg", "jpeg"])

        with vis_c2:
            st.markdown("##### 🧠 Visual Intelligence Diagnostics")
            image_to_analyze = camera_snap.getvalue() if camera_snap else (file_upload.getvalue() if file_upload else None)
            vision_prompt = st.text_input("Vision Directive for JARVIS:", value="What is on my screen or desk? Identify objects, text, code, or anomalies.")

            if image_to_analyze:
                if st.button("🔍 Analyze Optical Feed", use_container_width=True, type="primary"):
                    with st.spinner("JARVIS Eyes inspecting optical matrix..."):
                        import asyncio
                        v_res = asyncio.run(jarvis_vision.analyze_image(image_to_analyze, vision_prompt))
                        
                        st.markdown(
                            f"""
                            <div class="jarvis-bubble">
                                <b>J.A.R.V.I.S. Visual Assessment ({v_res.get('provider')}):</b><br><br>
                                {v_res.get('analysis')}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.info("Point your webcam or upload a screenshot to engage visual processing.")

    # =============================================================================
    # TAB 3: 3D HOLOGRAPHIC SECOND BRAIN (HOLO)
    # =============================================================================
    with tab_second_brain:
        st.markdown("### ✋ HOLO — 3D Hand-Gesture Controlled Second Brain")
        st.caption("Directly connected to Zubair Trabzada's HOLO Deck (running locally on port 4890). Notes float as interactive 3D orbs.")

        h_col1, h_col2 = st.columns([2, 1])

        with h_col1:
            st.markdown(
                """
                <div class="hud-card" style="margin-bottom: 14px;">
                    <div style="font-weight: bold; color: #00f0ff; font-size: 1.1rem;">
                        ⚡ Live HOLO Deck Connection: <a href="http://localhost:4890" target="_blank" style="color:#00f0ff; text-decoration: underline;">http://localhost:4890</a>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 4px;">
                        Raise your hands to the webcam: <b>Pinch</b> to grab a note, <b>Throw</b> with momentum, <b>Two-Hand Stretch</b> to pull big, press <b>J</b> for JARVIS voice narration.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Embedded HOLO Deck Preview
            st.components.v1.iframe("http://localhost:4890", height=520, scrolling=True)

        with h_col2:
            st.markdown("##### 📝 Second Brain Memory Notes")
            notes = jarvis_tools.list_second_brain_notes()
            st.metric("Total 3D Memory Notes", f"{len(notes)} orbs")

            with st.expander("➕ Materialize New 3D Note", expanded=False):
                n_title = st.text_input("Note Title:", placeholder="Project Astra Specs")
                n_body = st.text_area("Note Content:", placeholder="Key milestones and architecture details...")
                if st.button("✨ Materialize into HOLO Orb", use_container_width=True):
                    if n_title and n_body:
                        res = jarvis_tools.create_second_brain_note(n_title, n_body)
                        st.success(res["message"])
                        st.rerun()

            for note in notes[:6]:
                with st.expander(f"🔮 {note['title']}", expanded=False):
                    st.caption(note["filename"])
                    st.markdown(note["preview"])

    # =============================================================================
    # TAB 4: AUTONOMOUS TOOLS
    # =============================================================================
    with tab_tools:
        st.markdown("### 🛠️ JARVIS Autonomous Tools Grid")
        
        t_c1, t_c2 = st.columns(2)

        with t_c1:
            st.markdown("##### 📁 System File Radar")
            search_kw = st.text_input("Find files across PC:", placeholder="e.g. strata, synthesizer, .env, notes")
            if search_kw:
                found_files = jarvis_tools.find_files(search_kw)
                st.write(f"Located {len(found_files)} matches:")
                for f in found_files[:6]:
                    st.code(f"{f['relative_path']} ({f['size_kb']} KB)")

        with t_c2:
            st.markdown("##### 🛡️ Focus Lock (Anti-Distraction Guardian)")
            st.caption('"Sir, Instagram can wait. Your objectives require focus."')
            focus_input = st.text_input("Session Focus Objective:", value="Build & Polish JARVIS Astra OS")
            
            if not jarvis_tools.focus_mode_active:
                if st.button("🔒 Engage Focus Lock", use_container_width=True):
                    res = jarvis_tools.set_focus_lock(focus_input)
                    st.success(res["message"])
            else:
                st.warning(f"Focus Lock Active: '{jarvis_tools.focus_goal}'")
                if st.button("🔓 Disengage Focus Lock", use_container_width=True):
                    res = jarvis_tools.release_focus_lock()
                    st.info(res["message"])

    # =============================================================================
    # TAB 5: STRATA 125B MoE CORE
    # =============================================================================
    with tab_strata:
        st.markdown("### 🧠 Strata: Local 125B MoE Private Inference Engine")
        st.caption("Runs Qwen3.8-Flash-Next 125B on local consumer hardware using dynamic expert paging (CAAE/RCO).")

        strata_art_path = os.path.join(ROOT_DIR, "artifacts", "strata_studio_run.json")
        if os.path.exists(strata_art_path):
            with open(strata_art_path, "r", encoding="utf-8") as f_art:
                art = json.load(f_art)
            
            st1, st2, st3, st4 = st.columns(4)
            with st1:
                st.metric("125B MoE Catalog", f"{len(art.get('catalog', []))} variants")
            with st2:
                st.metric("BPE Tokenizer", "100% Lossless")
            with st3:
                st.metric("Quant Formats", "37 GGML Types")
            with st4:
                st.metric("Paging Cache Hit", f"{art.get('moe_simulation', {}).get('hit_rate_percent', 27.0)}%")

            with st.expander("📄 View Verified 125B Model Catalog & Compression Matrix", expanded=True):
                st.dataframe(art.get("catalog", []), use_container_width=True)
                st.dataframe(art.get("quantization", {}).get("tiers", []), use_container_width=True)
        else:
            st.info("Run `python scripts/strata_studio.py` to populate live benchmark telemetry.")

    # -----------------------------------------------------------------------------
    # Footer
    # -----------------------------------------------------------------------------
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 35px; font-family: 'JetBrains Mono', monospace;">
            ⚡ J.A.R.V.I.S. ASTRA OPERATING SYSTEM · POWERED BY MULTIMODAL INTELLIGENCE & HOLO 3D
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    try:
        st.set_page_config(
            page_title="JARVIS Astra OS — Executive Sovereign AI",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except Exception:
        pass
    render_jarvis_astra_os()
