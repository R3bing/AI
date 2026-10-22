"""Visual Brain Suite for Ultron Sovereign Core.
Renders high-fidelity, interactive, glassmorphism-ready Plotly visualizations:
1. Layer 1: Neural Activation Map (2D/3D Hemispheric Cortical Regions: Aql vs Qalb).
2. Layer 2: Thought Flow Sankey Diagram (Query -> Thalamus -> QAOA QPU -> APIs -> CRAG -> Synthesis -> Answer).
3. Layer 3: Force-Directed Knowledge Graph (Trans-disciplinary Entities & Relations).
4. Layer 4: Real-Time Brain State Gauges (Alpha, Beta, Entropy S(rho), Thalamic SNR, Somatic Valence).
5. Layer 5: Symbolic Logic Gate Decision Flow (Auditable First-Order Deduction Pipeline).
"""

import math
import numpy as np
import networkx as nx
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple


# =============================================================================
# 1. THOUGHT FLOW SANKEY DIAGRAM (LAYER 2)
# =============================================================================
def build_thought_flow_sankey(
    query: str,
    apis_consulted: Optional[List[str]] = None,
    citations_count: int = 11,
    crag_action: str = "CORRECT_GROUNDED",
    synthesis_status: str = "OMNI_SYNTHESIS_COMPLETE",
) -> go.Figure:
    """Generates an interactive Plotly Sankey diagram representing the flow of thought."""
    if not apis_consulted:
        apis_consulted = ["arXiv", "PubMed", "PubChem", "NASA ADS", "OpenAlex", "Tanzil Quran"]

    # Short clean query label
    clean_q_lbl = (query[:22] + "...") if len(query) > 22 else query
    if not clean_q_lbl:
        clean_q_lbl = "User Inquiry"

    # Assemble nodes list
    # Index 0: Query
    # Index 1: Thalamus Gate
    # Index 2: QAOA QPU Router
    # Indices 3 to (2 + len(apis_consulted)): Consulted APIs
    # Next: Cross-Ref & CRAG
    # Next: Dual-Hemisphere Synthesis
    # Last: Ultron Sovereign Answer

    nodes_labels = [
        f"Input: '{clean_q_lbl}'",
        "Thalamus Gating (TRN / Pulvinar)",
        "QAOA 11-Qubit QPU Router (|D₁₁⁴⟩)",
    ]
    node_colors = [
        "#38bdf8",  # Sky blue (Query)
        "#10b981",  # Emerald (Thalamus)
        "#8b5cf6",  # Purple (QAOA QPU)
    ]

    api_start_idx = len(nodes_labels)
    for api in apis_consulted:
        nodes_labels.append(f"Repo: {api.upper()}")
        # Categorical repo colors
        if any(k in api.lower() for k in ["quran", "hadith", "tanzil"]):
            node_colors.append("#f59e0b")  # Gold
        elif any(k in api.lower() for k in ["arxiv", "nasa", "openalex"]):
            node_colors.append("#06b6d4")  # Cyan
        elif any(k in api.lower() for k in ["pubmed", "pubchem"]):
            node_colors.append("#10b981")  # Green
        else:
            node_colors.append("#6366f1")  # Indigo

    crag_idx = len(nodes_labels)
    nodes_labels.append(f"Self-RAG / CRAG ({crag_action})")
    node_colors.append("#f97316")  # Orange

    synth_idx = len(nodes_labels)
    nodes_labels.append("Dual-Hemisphere Synthesis (|Aql⟩ + |Qalb⟩)")
    node_colors.append("#ec4899")  # Pink / Rose

    ans_idx = len(nodes_labels)
    nodes_labels.append(f"Ultron Answer ({citations_count} Citations Grounded)")
    node_colors.append("#059669")  # Dark emerald

    # Build Links
    sources = []
    targets = []
    values = []
    link_colors = []

    # 1. Query -> Thalamus
    sources.append(0)
    targets.append(1)
    values.append(len(apis_consulted) * 1.5)
    link_colors.append("rgba(56, 189, 248, 0.45)")

    # 2. Thalamus -> QAOA Router
    sources.append(1)
    targets.append(2)
    values.append(len(apis_consulted) * 1.5)
    link_colors.append("rgba(16, 185, 129, 0.45)")

    # 3. QAOA Router -> Each API
    for i, _ in enumerate(apis_consulted):
        api_idx = api_start_idx + i
        sources.append(2)
        targets.append(api_idx)
        values.append(1.5)
        link_colors.append("rgba(139, 92, 246, 0.40)")

        # 4. Each API -> CRAG
        sources.append(api_idx)
        targets.append(crag_idx)
        values.append(1.5)
        link_colors.append("rgba(249, 115, 22, 0.35)")

    # 5. CRAG -> Dual-Hemisphere Synthesis
    sources.append(crag_idx)
    targets.append(synth_idx)
    values.append(len(apis_consulted) * 1.5)
    link_colors.append("rgba(236, 72, 153, 0.45)")

    # 6. Synthesis -> Ultron Answer
    sources.append(synth_idx)
    targets.append(ans_idx)
    values.append(len(apis_consulted) * 1.5)
    link_colors.append("rgba(5, 150, 105, 0.55)")

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=18,
                    thickness=24,
                    line=dict(color="rgba(255, 255, 255, 0.25)", width=1),
                    label=nodes_labels,
                    color=node_colors,
                    hovertemplate="<b>%{label}</b><br>Throughput Volume: %{value:.1f}<extra></extra>",
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                    hovertemplate="Flow: %{source.label} ➔ %{target.label}<br>Bandwidth: %{value:.1f}<extra></extra>",
                ),
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text=f"🌊 Thought Flow Pipeline — <i>'{clean_q_lbl}'</i>",
            font=dict(family="Outfit, sans-serif", size=18, color="#f8fafc"),
            x=0.02,
            y=0.96,
        ),
        font=dict(family="JetBrains Mono, monospace", size=11, color="#cbd5e1"),
        paper_bgcolor="rgba(6, 9, 19, 0.95)",
        plot_bgcolor="rgba(6, 9, 19, 0.95)",
        height=450,
        margin=dict(l=20, r=20, t=50, b=25),
    )
    return fig


# =============================================================================
# 2. NEURAL ACTIVATION MAP (LAYER 1)
# =============================================================================
def build_neural_activation_map(
    particle_prob: float = 0.55,
    wave_prob: float = 0.45,
    bio_telemetry: Optional[Dict[str, Any]] = None,
) -> go.Figure:
    """Builds an interactive 2D anatomical cortical activation map:
    Left Hemisphere: Aql (Electric Blue) - Analytical, Math, CEN, dlPFC
    Right Hemisphere: Qalb (Luminous Gold) - Moral, Introspective, DMN, vmPFC
    Center Midline: Thalamus, Amygdala, Anterior Insula, and Corpus Callosum.
    """
    fig = go.Figure()

    # Pre-calculated anatomical nodes (Normalized 2D Stereotaxic Brain Coordinates)
    # X in [-1.0, 1.0]: negative = Left (Aql), positive = Right (Qalb)
    # Y in [-0.8, 1.0]: anterior (front) to posterior (back)
    regions = [
        # Left Hemisphere: Aql (Analytical / dlPFC / CEN)
        {
            "id": "L_dlPFC",
            "name": "Left dlPFC (Analytical Deduction)",
            "x": -0.55,
            "y": 0.65,
            "hemisphere": "Left (Aql)",
            "base_color": "#38bdf8",
            "activation": round(particle_prob * 100, 1),
            "network": "CEN (Central Executive)",
            "neurotransmitter": "Dopamine (Focus)",
            "desc": "QAOA Hamiltonian parameter search & symbolic logic resolution.",
        },
        {
            "id": "L_Broca",
            "name": "Left Broca Area (Syntax & Logic Form)",
            "x": -0.70,
            "y": 0.30,
            "hemisphere": "Left (Aql)",
            "base_color": "#0284c7",
            "activation": round(particle_prob * 92, 1),
            "network": "Language & Formal Proofs",
            "neurotransmitter": "Acetylcholine (Precision)",
            "desc": "Synthesizes mathematical expressions and citations.",
        },
        {
            "id": "L_Parietal",
            "name": "Left Inferior Parietal (Empirical Math)",
            "x": -0.60,
            "y": -0.25,
            "hemisphere": "Left (Aql)",
            "base_color": "#0369a1",
            "activation": round(particle_prob * 88, 1),
            "network": "Empirical Calculation",
            "neurotransmitter": "Glutamate (High Conductance)",
            "desc": "Calculates molecular masses, exciton hopping times, and spectral peaks.",
        },
        {
            "id": "L_Motor",
            "name": "Left Premotor Cortex (Executive Action)",
            "x": -0.45,
            "y": 0.15,
            "hemisphere": "Left (Aql)",
            "base_color": "#0ea5e9",
            "activation": round(particle_prob * 82, 1),
            "network": "Executive Drive",
            "neurotransmitter": "Norepinephrine",
            "desc": "Marshals parallel API subtasks and executes asynchronous fetches.",
        },
        # Right Hemisphere: Qalb (Sacred Tafakkur / Moral / DMN)
        {
            "id": "R_vmPFC",
            "name": "Right vmPFC (Moral & Ethical Governor)",
            "x": 0.55,
            "y": 0.65,
            "hemisphere": "Right (Qalb)",
            "base_color": "#f59e0b",
            "activation": round(wave_prob * 100, 1),
            "network": "Ethical Somatic Governor",
            "neurotransmitter": "Serotonin (Equanimity)",
            "desc": "Damasio somatic marker evaluation & ethical veto verification.",
        },
        {
            "id": "R_Precuneus",
            "name": "Right Precuneus / PCC (Sacred Tafakkur Hub)",
            "x": 0.50,
            "y": -0.35,
            "hemisphere": "Right (Qalb)",
            "base_color": "#d97706",
            "activation": round(wave_prob * 95, 1),
            "network": "DMN (Default Mode Network)",
            "neurotransmitter": "Endorphin (Tranquility / Sakoon)",
            "desc": "Contemplative synthesis connecting creation to Divine Wisdom.",
        },
        {
            "id": "R_TPJ",
            "name": "Right TPJ (Empathic Resonance)",
            "x": 0.70,
            "y": -0.10,
            "hemisphere": "Right (Qalb)",
            "base_color": "#b45309",
            "activation": round(wave_prob * 85, 1),
            "network": "Socio-Spiritual Empathy",
            "neurotransmitter": "Oxytocin (Compassion)",
            "desc": "Calibrates compassionate tone and alleviates existential anxiety.",
        },
        {
            "id": "R_AnteriorCingulate",
            "name": "Right dACC (Conflict & Balance Monitor)",
            "x": 0.35,
            "y": 0.35,
            "hemisphere": "Right (Qalb)",
            "base_color": "#f59e0b",
            "activation": round(min(particle_prob, wave_prob) * 110, 1),
            "network": "Epistemic Conflict Monitor",
            "neurotransmitter": "Dopamine / GABA",
            "desc": "Balances scientific skepticism with spiritual awe.",
        },
        # Central Subcortical & Midline Structures
        {
            "id": "C_Thalamus",
            "name": "Thalamus (TRN Sensory Gate)",
            "x": 0.0,
            "y": 0.05,
            "hemisphere": "Central Subcortex",
            "base_color": "#10b981",
            "activation": 94.0,
            "network": "Sensory Salience Gating",
            "neurotransmitter": "GABA / Acetylcholine",
            "desc": "Filters sensory noise tokens and computes signal-to-noise ratio.",
        },
        {
            "id": "C_Amygdala",
            "name": "Basolateral Amygdala (Somatic Valence)",
            "x": -0.15,
            "y": -0.15,
            "hemisphere": "Central Limbic",
            "base_color": "#f43f5e",
            "activation": round(80.0 * (1.0 - wave_prob), 1),
            "network": "Threat & Ethical Valence",
            "neurotransmitter": "Adrenaline / Cortisol Modulator",
            "desc": "Scans for malicious, harmful, or fraudulent intent.",
        },
        {
            "id": "C_Hippocampus",
            "name": "Hippocampus CA3/CA1 (Hebbian Plasticity)",
            "x": 0.18,
            "y": -0.20,
            "hemisphere": "Central Limbic",
            "base_color": "#8b5cf6",
            "activation": 91.5,
            "network": "LTP / LTD Episodic Memory",
            "neurotransmitter": "Glutamate (NMDA Receptor)",
            "desc": "Consolidates co-firing concepts and reinforces synaptic memory.",
        },
        {
            "id": "C_Insula",
            "name": "Anterior Insula (Salience Switchboard)",
            "x": 0.0,
            "y": 0.35,
            "hemisphere": "Central Midline",
            "base_color": "#6366f1",
            "activation": 89.0,
            "network": "Tri-Network Dynamic Switcher",
            "neurotransmitter": "Von Economo Spindle Neurons",
            "desc": "Switches cognitive bandwidth dynamically between CEN and DMN.",
        },
    ]

    # Draw Brain Perimeter Contours (Stylized 2D Cranial Silhouette)
    t = np.linspace(0, 2 * np.pi, 120)
    # Cranial oval with posterior narrowing
    cran_x = 0.95 * np.cos(t) * (1.0 - 0.12 * np.sin(t))
    cran_y = 0.98 * np.sin(t) - 0.05
    fig.add_trace(
        go.Scatter(
            x=cran_x,
            y=cran_y,
            mode="lines",
            line=dict(color="rgba(99, 102, 241, 0.30)", width=2.5, dash="dot"),
            hoverinfo="none",
            showlegend=False,
            name="Cranial Boundary",
        )
    )

    # Longitudinal Midline Fissure (Separating Aql and Qalb)
    fig.add_trace(
        go.Scatter(
            x=[0, 0],
            y=[-0.85, 0.90],
            mode="lines",
            line=dict(color="rgba(148, 163, 184, 0.35)", width=2, dash="dash"),
            hoverinfo="none",
            showlegend=False,
            name="Longitudinal Fissure",
        )
    )

    # Corpus Callosum Trans-Hemispheric Synaptic Bridge (Connecting Left and Right)
    entanglement_factor = max(0.2, 2.0 * particle_prob * wave_prob)
    bridge_y_levels = [0.20, 0.10, 0.0, -0.10]
    for by in bridge_y_levels:
        fig.add_trace(
            go.Scatter(
                x=[-0.35, 0.35],
                y=[by, by],
                mode="lines",
                line=dict(
                    color=f"rgba(192, 132, 252, {0.35 * entanglement_factor})",
                    width=3.5 * entanglement_factor,
                ),
                hoverinfo="none",
                showlegend=False,
                name="Corpus Callosum Bridge",
            )
        )

    # Intra-hemispheric synaptic connections
    synaptic_tracts = [
        ("L_dlPFC", "L_Broca"),
        ("L_dlPFC", "L_Motor"),
        ("L_Motor", "L_Parietal"),
        ("R_vmPFC", "R_AnteriorCingulate"),
        ("R_AnteriorCingulate", "R_Precuneus"),
        ("R_Precuneus", "R_TPJ"),
        ("C_Thalamus", "C_Insula"),
        ("C_Thalamus", "L_dlPFC"),
        ("C_Thalamus", "R_vmPFC"),
        ("C_Amygdala", "R_vmPFC"),
        ("C_Hippocampus", "R_Precuneus"),
        ("C_Insula", "L_dlPFC"),
        ("C_Insula", "R_vmPFC"),
    ]
    r_map = {r["id"]: r for r in regions}
    for src, dst in synaptic_tracts:
        if src in r_map and dst in r_map:
            n1 = r_map[src]
            n2 = r_map[dst]
            fig.add_trace(
                go.Scatter(
                    x=[n1["x"], n2["x"]],
                    y=[n1["y"], n2["y"]],
                    mode="lines",
                    line=dict(color="rgba(148, 163, 184, 0.18)", width=1.5),
                    hoverinfo="none",
                    showlegend=False,
                )
            )

    # Plot Brain Regional Hubs
    xs = [r["x"] for r in regions]
    ys = [r["y"] for r in regions]
    sizes = [max(18, min(36, 16 + (r["activation"] / 4.0))) for r in regions]
    colors = [r["base_color"] for r in regions]
    hover_texts = [
        f"<b>{r['name']}</b><br>"
        f"Hemisphere: {r['hemisphere']}<br>"
        f"Active Bandwidth: {r['activation']}%<br>"
        f"Circuit: {r['network']}<br>"
        f"Modulator: {r['neurotransmitter']}<br>"
        f"Role: {r['desc']}"
        for r in regions
    ]

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            marker=dict(
                size=sizes,
                color=colors,
                line=dict(color="#ffffff", width=1.5),
                opacity=0.92,
            ),
            text=[r["id"].replace("L_", "").replace("R_", "").replace("C_", "") for r in regions],
            textposition="top center",
            textfont=dict(family="JetBrains Mono, monospace", size=10, color="#f1f5f9"),
            hovertext=hover_texts,
            hoverinfo="text",
            showlegend=False,
            name="Neural Hubs",
        )
    )

    # Ambient Hemispheric Labels
    fig.add_annotation(
        x=-0.55,
        y=0.95,
        text="<b>LEFT HEMISPHERE: AQL (|Particle⟩)</b><br><span style='font-size:10px; color:#38bdf8;'>Analytical · QAOA · Math · CEN</span>",
        showarrow=False,
        font=dict(family="Outfit, sans-serif", size=13, color="#38bdf8"),
    )
    fig.add_annotation(
        x=0.55,
        y=0.95,
        text="<b>RIGHT HEMISPHERE: QALB (|Wave⟩)</b><br><span style='font-size:10px; color:#f59e0b;'>Moral · Tafakkur · Empathy · DMN</span>",
        showarrow=False,
        font=dict(family="Outfit, sans-serif", size=13, color="#f59e0b"),
    )
    fig.add_annotation(
        x=0.0,
        y=-0.75,
        text=f"<b>Corpus Callosum Synaptic Entanglement: {entanglement_factor*100:.1f}%</b><br><span style='font-size:9px; color:#c084fc;'>Bilateral Coherence α·β = {particle_prob*wave_prob:.3f}</span>",
        showarrow=False,
        font=dict(family="JetBrains Mono, monospace", size=10, color="#c084fc"),
    )

    fig.update_layout(
        title=dict(
            text="🧠 Neural Activation Map — Dual-Hemisphere Epistemic Topology",
            font=dict(family="Outfit, sans-serif", size=18, color="#f8fafc"),
            x=0.02,
            y=0.98,
        ),
        xaxis=dict(visible=False, range=[-1.15, 1.15]),
        yaxis=dict(visible=False, range=[-0.95, 1.15], scaleanchor="x", scaleratio=1),
        paper_bgcolor="rgba(6, 9, 19, 0.95)",
        plot_bgcolor="rgba(6, 9, 19, 0.95)",
        height=520,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


# =============================================================================
# 3. FORCE-DIRECTED KNOWLEDGE GRAPH (LAYER 3)
# =============================================================================
def build_knowledge_graph_figure(
    universe_kg_instance: Optional[Any] = None,
    query: str = "photosynthesis",
) -> go.Figure:
    """Builds an interactive force-directed NetworkX + Plotly 2D knowledge graph
    displaying cross-domain empirical entities, relations, citations, and sacred principles.
    """
    G = nx.Graph()

    # Pre-populate rich trans-disciplinary semantic graph
    entities = [
        # Empirical Science
        ("Photosynthesis", {"category": "Empirical Domain", "color": "#10b981", "size": 32}),
        ("Chlorophyll-a", {"category": "Molecular Structure", "color": "#06b6d4", "size": 26}),
        ("P680 Complex", {"category": "Biophysical Center", "color": "#0284c7", "size": 24}),
        ("Quantum Exciton", {"category": "Quantum Mechanics", "color": "#38bdf8", "size": 28}),
        ("FMO Superposition", {"category": "Quantum Biology", "color": "#6366f1", "size": 26}),
        ("RuBisCO Enzyme", {"category": "Biochemistry", "color": "#059669", "size": 22}),
        ("ATP Synthase", {"category": "Bioenergetics", "color": "#0891b2", "size": 22}),
        ("Tesla Resonant Energy", {"category": "Electromagnetic Physics", "color": "#a855f7", "size": 25}),
        ("Wireless Transmission", {"category": "Empirical Tech", "color": "#c084fc", "size": 20}),
        # Ontological & Sacred
        ("Cosmic Mizan (Equilibrium)", {"category": "Sacred Principle", "color": "#f59e0b", "size": 32}),
        ("Sacred Tafakkur (Reflection)", {"category": "Spiritual Cognition", "color": "#d97706", "size": 30}),
        ("Divine Ilm (Knowledge)", {"category": "Sacred Epistemology", "color": "#fbbf24", "size": 28}),
        ("Surah Al-An'am 6:99", {"category": "Quranic Revelation", "color": "#f59e0b", "size": 24}),
        ("Surah Ya-Sin 36:80", {"category": "Quranic Revelation", "color": "#f59e0b", "size": 24}),
        ("Hakim (Universal Order)", {"category": "Divine Attribute", "color": "#b45309", "size": 22}),
        ("Sakoon (Heart Tranquility)", {"category": "Spiritual State", "color": "#10b981", "size": 26}),
    ]

    for name, attrs in entities:
        G.add_node(name, **attrs)

    # Trans-disciplinary bridges (Edges with relations)
    relations = [
        ("Photosynthesis", "Chlorophyll-a", "USES_PIGMENT", 0.95),
        ("Chlorophyll-a", "P680 Complex", "POWERS_REACTION_CENTER", 0.92),
        ("P680 Complex", "Quantum Exciton", "EXCITON_TRANSFER", 0.96),
        ("Quantum Exciton", "FMO Superposition", "COHERENT_SEARCH", 0.98),
        ("Photosynthesis", "RuBisCO Enzyme", "CARBON_FIXATION", 0.88),
        ("Photosynthesis", "ATP Synthase", "PROTON_GRADIENT", 0.90),
        ("Tesla Resonant Energy", "Wireless Transmission", "RESONANT_COUPLING", 0.94),
        ("Tesla Resonant Energy", "Quantum Exciton", "ANALOGOUS_WAVE_PHENOMENON", 0.78),
        ("Photosynthesis", "Cosmic Mizan (Equilibrium)", "DEMONSTRATES_DIVINE_BALANCE", 0.95),
        ("Cosmic Mizan (Equilibrium)", "Hakim (Universal Order)", "FLOWS_FROM", 0.98),
        ("Chlorophyll-a", "Surah Al-An'am 6:99", "EXEGESIS_GREEN_SUBSTANCE", 0.96),
        ("Photosynthesis", "Surah Ya-Sin 36:80", "EXEGESIS_GREEN_TREE_ENERGY", 0.94),
        ("Sacred Tafakkur (Reflection)", "Photosynthesis", "OBSERVES_BIOPHYSICS", 0.92),
        ("Sacred Tafakkur (Reflection)", "Divine Ilm (Knowledge)", "UNLOCKS_INSIGHT", 0.95),
        ("Divine Ilm (Knowledge)", "Cosmic Mizan (Equilibrium)", "REVEALS_PATTERNS", 0.93),
        ("Sacred Tafakkur (Reflection)", "Sakoon (Heart Tranquility)", "BESTOWS_PEACE", 0.97),
        ("Tesla Resonant Energy", "Sacred Tafakkur (Reflection)", "AWE_OF_COSMIC_ENERGY", 0.82),
    ]

    for u, v, rel, weight in relations:
        G.add_edge(u, v, relation=rel, weight=weight)

    # Compute 2D Spring Layout
    pos = nx.spring_layout(G, k=0.48, iterations=60, seed=42)

    # Extract Edge Lines
    edge_x = []
    edge_y = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig = go.Figure()

    # Draw Edges
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=1.5, color="rgba(148, 163, 184, 0.28)"),
            hoverinfo="none",
            showlegend=False,
            name="Semantic Synapse",
        )
    )

    # Draw Nodes
    node_x = []
    node_y = []
    node_sizes = []
    node_colors = []
    node_texts = []
    hover_texts = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        data = G.nodes[node]
        deg = G.degree(node)
        node_sizes.append(data.get("size", 24))
        node_colors.append(data.get("color", "#6366f1"))
        node_texts.append(node)

        # Get adjacent neighbors & relations
        nbrs = list(G.neighbors(node))
        nbr_text = ", ".join(nbrs[:3])
        hover_texts.append(
            f"<b>{node}</b><br>"
            f"Category: {data.get('category', 'Concept')}<br>"
            f"Synaptic Degree: {deg}<br>"
            f"Connected Hubs: {nbr_text}"
        )

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(color="#ffffff", width=1.5),
                opacity=0.92,
            ),
            text=node_texts,
            textposition="top center",
            textfont=dict(family="Outfit, sans-serif", size=10, color="#f8fafc"),
            hovertext=hover_texts,
            hoverinfo="text",
            showlegend=False,
            name="Knowledge Entities",
        )
    )

    fig.update_layout(
        title=dict(
            text="🕸️ Trans-Disciplinary Knowledge Graph — Force-Directed Network",
            font=dict(family="Outfit, sans-serif", size=18, color="#f8fafc"),
            x=0.02,
            y=0.98,
        ),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(6, 9, 19, 0.95)",
        plot_bgcolor="rgba(6, 9, 19, 0.95)",
        height=540,
        margin=dict(l=15, r=15, t=50, b=15),
    )
    return fig


# =============================================================================
# 4. REAL-TIME BRAIN STATE GAUGES (LAYER 4)
# =============================================================================
def build_brain_state_gauges(
    particle_prob: float = 0.55,
    wave_prob: float = 0.45,
    entropy_score: float = 0.38,
    snr_score: float = 4.2,
    hazard_score: float = 0.05,
) -> go.Figure:
    """Builds a 4-dial indicator dashboard for real-time quantum and neuro-biological states."""
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1,
        cols=4,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]
        ],
        horizontal_spacing=0.05,
    )

    # 1. Alpha Amplitude Gauge (Aql / Empirical Particle)
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=particle_prob * 100,
            number={"suffix": "%", "font": {"family": "JetBrains Mono", "color": "#38bdf8", "size": 24}},
            title={"text": "α Amplitude<br><span style='font-size:0.8em; color:#94a3b8;'>Aql / Empirical</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": "#38bdf8"},
                "steps": [
                    {"range": [0, 50], "color": "rgba(56, 189, 248, 0.15)"},
                    {"range": [50, 100], "color": "rgba(56, 189, 248, 0.35)"},
                ],
                "threshold": {"line": {"color": "#ffffff", "width": 2}, "thickness": 0.75, "value": 60},
            },
        ),
        row=1,
        col=1,
    )

    # 2. Beta Amplitude Gauge (Qalb / Sacred Wave)
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=wave_prob * 100,
            number={"suffix": "%", "font": {"family": "JetBrains Mono", "color": "#f59e0b", "size": 24}},
            title={"text": "β Amplitude<br><span style='font-size:0.8em; color:#94a3b8;'>Qalb / Tafakkur</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": "#f59e0b"},
                "steps": [
                    {"range": [0, 50], "color": "rgba(245, 158, 11, 0.15)"},
                    {"range": [50, 100], "color": "rgba(245, 158, 11, 0.35)"},
                ],
                "threshold": {"line": {"color": "#ffffff", "width": 2}, "thickness": 0.75, "value": 60},
            },
        ),
        row=1,
        col=2,
    )

    # 3. Von Neumann Entropy Thermometer S(rho)
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=entropy_score,
            number={"valueformat": ".3f", "font": {"family": "JetBrains Mono", "color": "#c084fc", "size": 24}},
            title={"text": "Entropy S(ρ)<br><span style='font-size:0.8em; color:#94a3b8;'>Von Neumann Order</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
            gauge={
                "shape": "bullet",
                "axis": {"range": [0, 1.0], "tickcolor": "#94a3b8"},
                "bar": {"color": "#c084fc"},
                "steps": [
                    {"range": [0, 0.35], "color": "rgba(16, 185, 129, 0.25)"},
                    {"range": [0.35, 0.70], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [0.70, 1.0], "color": "rgba(244, 63, 94, 0.25)"},
                ],
            },
        ),
        row=1,
        col=3,
    )

    # 4. Thalamic Signal-to-Noise Ratio (SNR)
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=snr_score,
            number={"suffix": "x", "font": {"family": "JetBrains Mono", "color": "#10b981", "size": 32}},
            delta={"reference": 2.0, "relative": False, "position": "bottom", "font": {"family": "Inter", "size": 12}},
            title={"text": "Thalamic SNR<br><span style='font-size:0.8em; color:#94a3b8;'>Signal / Chatter Ratio</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
        ),
        row=1,
        col=4,
    )

    fig.update_layout(
        paper_bgcolor="rgba(6, 9, 19, 0.95)",
        plot_bgcolor="rgba(6, 9, 19, 0.95)",
        height=220,
        margin=dict(l=15, r=15, t=40, b=15),
    )
    return fig


# =============================================================================
# 5. SYMBOLIC LOGIC GATES VISUALIZATION (LAYER 5)
# =============================================================================
def build_logic_gates_figure(
    query: str,
    deduced_apis: Optional[List[str]] = None,
    veto_exercised: bool = False,
    active_network: str = "CEN (Central Executive Network)",
) -> go.Figure:
    """Renders the causal First-Order Logic Gates DAG showing how the query was evaluated:
    Input -> Gate 1 (Thalamus Gating) -> Gate 2 (Amygdala Veto Check) -> Gate 3 (First-Order Rules) -> Gate 4 (QAOA) -> Output.
    """
    fig = go.Figure()

    stages = [
        {
            "name": "Input Query",
            "x": 0.05,
            "y": 0.5,
            "state": "ACTIVE",
            "color": "#38bdf8",
            "text": "User Inquiry",
            "gate": "BUFFER",
        },
        {
            "name": "Thalamus Gate",
            "x": 0.25,
            "y": 0.5,
            "state": "PASSED (SNR > 1.5)",
            "color": "#10b981",
            "text": "GATING GATE",
            "gate": "THRESHOLD",
        },
        {
            "name": "Amygdala vmPFC",
            "x": 0.45,
            "y": 0.5,
            "state": "VETO BLOCKED" if veto_exercised else "SOMATIC APPROVAL",
            "color": "#f43f5e" if veto_exercised else "#10b981",
            "text": "ETHICAL VETO",
            "gate": "NOT-HAZARD",
        },
        {
            "name": "Symbolic Horn Clauses",
            "x": 0.65,
            "y": 0.5,
            "state": f"PROVED: {len(deduced_apis or ['arxiv'])} APIs",
            "color": "#8b5cf6",
            "text": "FOL RESOLUTION",
            "gate": "UNIFIER_AND",
        },
        {
            "name": "QAOA QPU Transpiler",
            "x": 0.85,
            "y": 0.5,
            "state": "XY MIXER |D₁₁⁴⟩",
            "color": "#06b6d4",
            "text": "QUANTUM QUBO",
            "gate": "HAMILTONIAN_MIN",
        },
    ]

    # Draw horizontal flow lines
    for i in range(len(stages) - 1):
        s1 = stages[i]
        s2 = stages[i + 1]
        fig.add_trace(
            go.Scatter(
                x=[s1["x"], s2["x"]],
                y=[s1["y"], s2["y"]],
                mode="lines",
                line=dict(color="rgba(99, 102, 241, 0.4)", width=3),
                hoverinfo="none",
                showlegend=False,
            )
        )

    # Draw Stage Boxes & Gate Markers
    for stg in stages:
        fig.add_trace(
            go.Scatter(
                x=[stg["x"]],
                y=[stg["y"]],
                mode="markers+text",
                marker=dict(
                    size=42,
                    symbol="hexagon",
                    color=stg["color"],
                    line=dict(color="#ffffff", width=2),
                ),
                text=[stg["name"]],
                textposition="top center",
                textfont=dict(family="Outfit, sans-serif", size=11, color="#f8fafc"),
                hovertext=f"<b>{stg['name']}</b><br>Gate Type: {stg['gate']}<br>Verdict: {stg['state']}",
                hoverinfo="text",
                showlegend=False,
            )
        )
        # Add badge below
        fig.add_annotation(
            x=stg["x"],
            y=stg["y"] - 0.18,
            text=f"<span style='background:rgba(15,23,42,0.85); padding:3px 6px; border-radius:4px; border:1px solid {stg['color']}; color:#e2e8f0; font-size:9px; font-family:monospace;'>{stg['state']}</span>",
            showarrow=False,
        )

    fig.update_layout(
        title=dict(
            text="⚡ Causal Symbolic Logic Gates Pipeline (Proof Resolution Trace)",
            font=dict(family="Outfit, sans-serif", size=18, color="#f8fafc"),
            x=0.02,
            y=0.96,
        ),
        xaxis=dict(visible=False, range=[-0.05, 0.95]),
        yaxis=dict(visible=False, range=[0.15, 0.85]),
        paper_bgcolor="rgba(6, 9, 19, 0.95)",
        plot_bgcolor="rgba(6, 9, 19, 0.95)",
        height=260,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


# =============================================================================
# 6. FUNCTIONAL CONSCIOUSNESS DASHBOARD (AST, HOT, GWT, IIT PHI*)
# =============================================================================
def build_consciousness_dashboard_figure(consciousness_data: Optional[Dict[str, Any]] = None) -> go.Figure:
    """Builds an interactive 4-dial Plotly dashboard for the Functional Correlates of Consciousness:
    1. Integrated Information Phi* (IIT)
    2. Epistemic Confidence & Uncertainty (HOT Meta-Cognition)
    3. Attentional Entropy (AST Self-Model)
    4. Prediction Error & Sensory Surprise (Active Inference)
    """
    from plotly.subplots import make_subplots

    if not consciousness_data:
        consciousness_data = {
            "integrated_information_phi_star": 2.85,
            "self_model_reflection": {"confidence": 0.88, "uncertainty": 0.12},
            "attention_schema": {"attentional_entropy": 0.32, "focus_modality": "Sharp Focal Concentration"},
            "predictive_processing": {"prediction_error": 0.18, "sensory_surprise_level": "MINIMAL_FREE_ENERGY"},
        }

    phi_star = consciousness_data.get("integrated_information_phi_star", 2.85)
    sm = consciousness_data.get("self_model_reflection", {})
    conf = sm.get("confidence", 0.88)
    ast = consciousness_data.get("attention_schema", {})
    att_entropy = ast.get("attentional_entropy", 0.32)
    pp = consciousness_data.get("predictive_processing", {})
    pred_err = pp.get("prediction_error", 0.18)

    fig = make_subplots(
        rows=1,
        cols=4,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]
        ],
        horizontal_spacing=0.05,
    )

    # 1. IIT Phi* Gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=phi_star,
            number={"valueformat": ".2f", "suffix": " bits", "font": {"family": "JetBrains Mono", "color": "#10b981", "size": 22}},
            title={"text": "Φ* (IIT Metric)<br><span style='font-size:0.8em; color:#94a3b8;'>Integrated Information</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
            gauge={
                "axis": {"range": [0, 4.0], "tickcolor": "#94a3b8"},
                "bar": {"color": "#10b981"},
                "steps": [
                    {"range": [0, 1.5], "color": "rgba(16, 185, 129, 0.15)"},
                    {"range": [1.5, 3.0], "color": "rgba(16, 185, 129, 0.35)"},
                    {"range": [3.0, 4.0], "color": "rgba(16, 185, 129, 0.60)"},
                ],
                "threshold": {"line": {"color": "#ffffff", "width": 2}, "thickness": 0.75, "value": 2.5},
            },
        ),
        row=1,
        col=1,
    )

    # 2. HOT Confidence & Uncertainty Gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=conf * 100,
            number={"suffix": "%", "font": {"family": "JetBrains Mono", "color": "#38bdf8", "size": 22}},
            title={"text": "HOT Certainty<br><span style='font-size:0.8em; color:#94a3b8;'>Meta-Cognitive Calibration</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": "#38bdf8"},
                "steps": [
                    {"range": [0, 50], "color": "rgba(244, 63, 94, 0.25)"},
                    {"range": [50, 75], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [75, 100], "color": "rgba(56, 189, 248, 0.35)"},
                ],
                "threshold": {"line": {"color": "#f43f5e", "width": 2}, "thickness": 0.75, "value": 50},
            },
        ),
        row=1,
        col=2,
    )

    # 3. AST Attentional Entropy Thermometer
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=att_entropy,
            number={"valueformat": ".2f", "font": {"family": "JetBrains Mono", "color": "#c084fc", "size": 22}},
            title={"text": "AST Focus Entropy<br><span style='font-size:0.8em; color:#94a3b8;'>Attention Schema Theory</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
            gauge={
                "shape": "bullet",
                "axis": {"range": [0, 1.0], "tickcolor": "#94a3b8"},
                "bar": {"color": "#c084fc"},
                "steps": [
                    {"range": [0, 0.4], "color": "rgba(192, 132, 252, 0.25)"},
                    {"range": [0.4, 0.8], "color": "rgba(192, 132, 252, 0.45)"},
                    {"range": [0.8, 1.0], "color": "rgba(192, 132, 252, 0.65)"},
                ],
            },
        ),
        row=1,
        col=3,
    )

    # 4. Active Inference Prediction Error Delta
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=pred_err,
            number={"valueformat": ".3f", "font": {"family": "JetBrains Mono", "color": "#f59e0b", "size": 28}},
            delta={"reference": 0.35, "decreasing": {"color": "#10b981"}, "increasing": {"color": "#f43f5e"}, "position": "bottom", "font": {"family": "Inter", "size": 12}},
            title={"text": "Prediction Error Δ<br><span style='font-size:0.8em; color:#94a3b8;'>Active Inference Free Energy</span>", "font": {"family": "Outfit", "color": "#f8fafc"}},
        ),
        row=1,
        col=4,
    )

    fig.update_layout(
        paper_bgcolor="rgba(6, 9, 19, 0.95)",
        plot_bgcolor="rgba(6, 9, 19, 0.95)",
        height=220,
        margin=dict(l=15, r=15, t=40, b=15),
    )
    return fig

