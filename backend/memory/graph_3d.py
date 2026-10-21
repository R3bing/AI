"""Interactive 3D Neural Knowledge Graph Galaxy Visualizer for Quantum Knowledge Weaver.
Renders Neo4j / In-Memory entities and cross-domain relationships as an interactive 3D constellation.
"""

import math
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Any


def create_3d_knowledge_graph_figure(graph_data: Dict[str, Any]) -> go.Figure:
    """Constructs an interactive 3D Plotly figure representing the entity-relation knowledge graph."""
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if not nodes:
        # Default starter constellation if graph is empty
        nodes = [
            {"id": "quantum", "name": "Quantum Mechanics", "label": "Physics"},
            {"id": "entangle", "name": "Entanglement", "label": "Physics"},
            {"id": "tafakkur", "name": "Tafakkur (Contemplation)", "label": "Spiritual"},
            {"id": "unity", "name": "Wahdah (Universal Unity)", "label": "Philosophy"},
            {"id": "brain", "name": "Aql (Human Intellect)", "label": "Cognitive"},
            {"id": "heart", "name": "Qalb (Spiritual Heart)", "label": "Cognitive"},
            {"id": "cosmos", "name": "Cosmology (Afaq)", "label": "Astronomy"},
        ]
        edges = [
            {"source": "quantum", "relationship": "EXHIBITS", "target": "entangle"},
            {"source": "entangle", "relationship": "MIRRORS", "target": "unity"},
            {"source": "tafakkur", "relationship": "INTERNALIZES", "target": "unity"},
            {"source": "brain", "relationship": "INVESTIGATES", "target": "quantum"},
            {"source": "heart", "relationship": "PRACTICES", "target": "tafakkur"},
            {"source": "brain", "relationship": "SYNAPSES_WITH", "target": "heart"},
            {"source": "cosmos", "relationship": "REFLECTS", "target": "unity"},
        ]

    # Map nodes to 3D coordinates using a golden-spiral spherical distribution
    num_nodes = len(nodes)
    node_coords = {}
    indices = np.arange(0, num_nodes, dtype=float) + 0.5
    phi = np.arccos(1.0 - 2.0 * indices / num_nodes)
    theta = np.pi * (1.0 + 5.0 ** 0.5) * indices

    radius = 2.0
    for i, node in enumerate(nodes):
        nid = node.get("id") or str(i)
        x = radius * math.sin(phi[i]) * math.cos(theta[i])
        y = radius * math.sin(phi[i]) * math.sin(theta[i])
        z = radius * math.cos(phi[i])
        node_coords[nid] = (x, y, z)

    # 1. Edge Traces
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in edges:
        s_id = edge.get("source")
        t_id = edge.get("target")
        if s_id in node_coords and t_id in node_coords:
            x0, y0, z0 = node_coords[s_id]
            x1, y1, z1 = node_coords[t_id]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])

    fig = go.Figure()

    if edge_x:
        fig.add_trace(
            go.Scatter3d(
                x=edge_x,
                y=edge_y,
                z=edge_z,
                mode="lines",
                line=dict(color="rgba(148, 163, 184, 0.4)", width=2),
                hoverinfo="none",
                name="Synaptic Connections",
            )
        )

    # 2. Node Traces grouped by Domain Label
    color_map = {
        "Physics": "#38bdf8",
        "Spiritual": "#34d399",
        "Philosophy": "#c084fc",
        "Cognitive": "#f43f5e",
        "Astronomy": "#fbbf24",
        "Medical": "#fb7185",
        "Chemical": "#2dd4bf",
    }

    xs = []
    ys = []
    zs = []
    node_text = []
    node_colors = []

    for node in nodes:
        nid = node.get("id") or ""
        name = node.get("name") or nid
        label = node.get("label") or "Concept"
        x, y, z = node_coords.get(nid, (0, 0, 0))
        xs.append(x)
        ys.append(y)
        zs.append(z)
        node_text.append(f"<b>{name}</b><br>Domain: {label}<br>ID: {nid}")
        node_colors.append(color_map.get(label, "#a855f7"))

    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers+text",
            marker=dict(
                symbol="circle",
                size=12,
                color=node_colors,
                line=dict(color="#ffffff", width=1),
            ),
            text=[n.get("name", "") for n in nodes],
            textposition="top center",
            textfont=dict(color="#f8fafc", size=11),
            hoverinfo="text",
            hovertext=node_text,
            name="Knowledge Entities",
        )
    )

    fig.update_layout(
        title=dict(
            text="🕸️ 3D Neural Knowledge Galaxy: Entities & Synaptic Relational Topology",
            font=dict(size=15, color="#f8fafc"),
        ),
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            bgcolor="#0b0f19",
            camera=dict(
                eye=dict(x=1.6, y=1.6, z=1.3),
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=500,
        showlegend=False,
    )

    return fig
