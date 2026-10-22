"""Interactive Concept & Quantum Linkage Graph Visualizer for Ultron Core.
Builds dynamic, publication-grade Plotly network graphs illustrating the
epistemic, empirical, and ontological linkages between query entities,
scientific databases, and AI Council participants.
"""

from typing import Dict, List, Any
import plotly.graph_objects as go
import numpy as np


def create_concept_linkage_figure(query: str, citations: List[Dict[str, Any]], council_turns: List[Dict[str, Any]]) -> go.Figure:
    """Constructs an interactive 2D circular/force network graph mapping all linkages for the query."""
    q_low = query.lower()
    is_photo = any(k in q_low for k in ["photosynthesis", "chlorophyll", "plant", "calvin", "thylakoid", "rubisco", "bioenergetic", "leaf"])

    if is_photo:
        nodes = [
            # Central Core
            {"id": "core", "label": "🌿 Photosynthesis\nCore Engine", "group": "core", "size": 36, "color": "#10b981", "x": 0.0, "y": 0.0, "desc": "Overall Reaction: 6CO2 + 6H2O + hν → C6H12O6 + 6O2 (ΔG°' = +2870 kJ/mol)"},
            # Scientific Mechanisms
            {"id": "light_rxn", "label": "⚡ Thylakoid Membrane\n(Light Reactions)", "group": "bio", "size": 26, "color": "#06b6d4", "x": -0.65, "y": 0.45, "desc": "PSII (P680) water photolysis (2H2O → O2 + 4H+ + 4e-) & proton motive force"},
            {"id": "dark_rxn", "label": "🧪 Stroma Calvin Cycle\n(RuBisCO Fixation)", "group": "bio", "size": 26, "color": "#14b8a6", "x": 0.65, "y": 0.45, "desc": "RuBisCO fixes CO2 with RuBP into 3-PGA, reduced to G3P & hexose sugars"},
            {"id": "quantum_coherence", "label": "⚛️ Quantum Exciton\nCoherence (FMO)", "group": "quantum", "size": 28, "color": "#8b5cf6", "x": -0.75, "y": -0.35, "desc": "Wave-like spatial superposition in FMO antenna complex yields ~99% energy transfer efficiency"},
            {"id": "energy_carriers", "label": "🔋 ATP & NADPH\nBioenergetics", "group": "bio", "size": 24, "color": "#f59e0b", "x": 0.0, "y": 0.75, "desc": "Rotary ATP Synthase & Ferredoxin-NADP+ Reductase drive cellular metabolism"},
            {"id": "space_botany", "label": "🪐 NASA Space Botany\n& Orbit SIF", "group": "space", "size": 24, "color": "#38bdf8", "x": 0.75, "y": -0.35, "desc": "NASA OCO-2 chlorophyll fluorescence & ISS APEX-09 microgravity plant growth"},
            {"id": "sacred_khadir", "label": "🕊️ Sacred 'Al-Khadir'\n& Solar Fire Storage", "group": "sacred", "size": 26, "color": "#10b981", "x": 0.0, "y": -0.75, "desc": "Surah Al-An'am (6:99) & Ya-Sin (36:80): Green chlorophyll capturing incoming celestial fire"},
            # Databases
            {"id": "db_nasa", "label": "🪐 NASA Data", "group": "db", "size": 18, "color": "#0284c7", "x": 0.95, "y": -0.05, "desc": "Satellite remote sensing & SIF mapping"},
            {"id": "db_pubmed", "label": "🧬 PubMed Bio", "group": "db", "size": 18, "color": "#059669", "x": -0.4, "y": 0.85, "desc": "Biophotoelectrochemistry & cellular mechanisms"},
            {"id": "db_arxiv", "label": "⚛️ arXiv Quantum", "group": "db", "size": 18, "color": "#7c3aed", "x": -0.95, "y": -0.05, "desc": "Theoretical exciton coherence & bandgap models"},
            {"id": "db_pubchem", "label": "🧪 PubChem NIH", "group": "db", "size": 18, "color": "#d97706", "x": 0.4, "y": 0.85, "desc": "Chlorophyll-A (CID 6433226) chemical structure"},
            {"id": "db_quran", "label": "📖 Quran Corpus", "group": "db", "size": 18, "color": "#047857", "x": -0.4, "y": -0.85, "desc": "Ontological verses on green shoots and vegetation"},
            {"id": "db_wiki", "label": "🌐 Wikipedia", "group": "db", "size": 18, "color": "#64748b", "x": 0.4, "y": -0.85, "desc": "Global empirical synthesis of light reactions"},
        ]

        edges = [
            ("core", "light_rxn"), ("core", "dark_rxn"), ("core", "quantum_coherence"),
            ("core", "energy_carriers"), ("core", "space_botany"), ("core", "sacred_khadir"),
            ("light_rxn", "energy_carriers"), ("energy_carriers", "dark_rxn"),
            ("light_rxn", "quantum_coherence"), ("quantum_coherence", "db_arxiv"),
            ("light_rxn", "db_pubmed"), ("dark_rxn", "db_pubchem"),
            ("space_botany", "db_nasa"), ("sacred_khadir", "db_quran"),
            ("core", "db_wiki"), ("dark_rxn", "db_wiki"),
            ("quantum_coherence", "sacred_khadir"), ("space_botany", "core"),
        ]
    else:
        # Generalized Universal Linkage Map
        nodes = [
            {"id": "core", "label": f"⚡ {query[:25]}\nCore Inquiry", "group": "core", "size": 34, "color": "#6366f1", "x": 0.0, "y": 0.0, "desc": f"Epistemic core for: {query}"},
            {"id": "aql", "label": "🔬 Empirical Science\n(Left Hemisphere / Aql)", "group": "aql", "size": 26, "color": "#06b6d4", "x": -0.65, "y": 0.4, "desc": "Observable data, peer-reviewed citations, mathematical formulation"},
            {"id": "qalb", "label": "🕊️ Sacred Conscience\n(Right Hemisphere / Qalb)", "group": "qalb", "size": 26, "color": "#10b981", "x": 0.65, "y": 0.4, "desc": "Ontological purpose, spiritual tranquility (Sakoon), scripture resonance"},
            {"id": "quantum_qaoa", "label": "⚛️ Quantum QAOA\nRouter & Duality", "group": "quantum", "size": 24, "color": "#8b5cf6", "x": 0.0, "y": -0.65, "desc": "11-Qubit Dicke state router allocating query budget"},
            {"id": "council", "label": "🏛️ Multi-AI Council\nMajlis Arena", "group": "council", "size": 24, "color": "#f43f5e", "x": -0.7, "y": -0.35, "desc": "Gemini, DeepSeek CoT, Groq LPU, Dr. Farooq, Hazrat Irfan"},
            {"id": "apis", "label": "🌐 2,238 Public APIs\nData Mesh", "group": "api", "size": 22, "color": "#f59e0b", "x": 0.7, "y": -0.35, "desc": "Live external open APIs connected to the domain"},
        ]
        edges = [
            ("core", "aql"), ("core", "qalb"), ("core", "quantum_qaoa"),
            ("core", "council"), ("core", "apis"), ("aql", "qalb"),
            ("quantum_qaoa", "aql"), ("council", "quantum_qaoa"), ("apis", "aql"),
        ]

    # Map node lookup
    node_map = {n["id"]: n for n in nodes}

    # Build Edge Traces
    edge_x = []
    edge_y = []
    for u, v in edges:
        if u in node_map and v in node_map:
            edge_x.extend([node_map[u]["x"], node_map[v]["x"], None])
            edge_y.extend([node_map[u]["y"], node_map[v]["y"], None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1.8, color="rgba(148, 163, 184, 0.35)"),
        hoverinfo="none",
        mode="lines",
    )

    # Build Node Traces
    node_x = [n["x"] for n in nodes]
    node_y = [n["y"] for n in nodes]
    node_text = [n["label"] for n in nodes]
    node_hover = [f"<b>{n['label'].replace(chr(10), ' ')}</b><br/>{n['desc']}" for n in nodes]
    node_color = [n["color"] for n in nodes]
    node_size = [n["size"] for n in nodes]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hovertext=node_hover,
        hoverinfo="text",
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line=dict(width=2.5, color="rgba(255, 255, 255, 0.85)"),
            opacity=0.95,
        ),
        textfont=dict(
            family="Outfit, sans-serif",
            size=11,
            color="#e2e8f0",
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text=f"🌐 Multi-Dimensional Epistemic & Empirical Linkage Topology: <i>{query}</i>",
                font=dict(family="Outfit, sans-serif", size=14, color="#cbd5e1"),
                x=0.02,
                y=0.96,
            ),
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=20, r=20, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="rgba(10, 16, 30, 0.6)",
            paper_bgcolor="rgba(6, 10, 20, 0.0)",
            height=460,
        ),
    )
    return fig
