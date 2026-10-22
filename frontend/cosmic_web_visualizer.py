"""Interactive 3D & 2D Cosmic Web Visualizer for Ultron Sovereign Core.
Renders high-dimensional cosmic neural networks, filamentary web structures,
galactic clusters, and Hebbian synaptic bridges.
"""

import math
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional


def create_cosmic_web_3d_figure(cosmic_graph: Dict[str, Any], selected_cluster: Optional[str] = None) -> go.Figure:
    """Builds an awe-inspiring 3D Plotly visualization of the Cosmic Web of Neural Networks."""
    fig = go.Figure()

    nodes = cosmic_graph.get("nodes", {})
    filaments = cosmic_graph.get("filaments", [])
    query = cosmic_graph.get("query", "Inquiry")

    # 1. Distant Cosmic Starfield (Ambient Space Background Particles)
    np.random.seed(42)
    n_stars = 140
    star_r = 3.6 + np.random.rand(n_stars) * 1.5
    star_theta = np.random.uniform(0, 2 * np.pi, n_stars)
    star_phi = np.random.uniform(0, np.pi, n_stars)

    star_x = star_r * np.sin(star_phi) * np.cos(star_theta)
    star_y = star_r * np.sin(star_phi) * np.sin(star_theta)
    star_z = star_r * np.cos(star_phi)
    star_sizes = np.random.uniform(1.2, 3.2, n_stars)

    fig.add_trace(
        go.Scatter3d(
            x=star_x,
            y=star_y,
            z=star_z,
            mode="markers",
            marker=dict(
                size=star_sizes,
                color="rgba(226, 232, 240, 0.35)",
                opacity=0.6,
            ),
            hoverinfo="none",
            showlegend=False,
            name="Cosmic Dust & Stars",
        )
    )

    # 2. Draw Cosmic Filaments (Synaptic Strands across Space)
    # Group by color for high rendering performance
    filament_groups: Dict[str, Dict[str, Any]] = {}

    for fil in filaments:
        u = fil.get("source")
        v = fil.get("target")
        if u in nodes and v in nodes:
            n1 = nodes[u]
            n2 = nodes[v]
            col = fil.get("color", "#38bdf8")
            w = fil.get("width", 2.2)
            lbl = fil.get("label", "Filament")

            # Interpolate a smooth filament path with subtle curve
            p0 = np.array([n1["x"], n1["y"], n1["z"]])
            p1 = np.array([n2["x"], n2["y"], n2["z"]])
            mid = (p0 + p1) / 2.0
            # subtle displacement perpendicular to line
            dist = np.linalg.norm(p1 - p0)
            lift = 0.08 * math.sin(dist)

            steps = 10
            xs, ys, zs = [], [], []
            for t in np.linspace(0, 1, steps):
                pt = (1 - t) * p0 + t * p1 + np.array([0, 0, lift * math.sin(t * math.pi)])
                xs.append(pt[0])
                ys.append(pt[1])
                zs.append(pt[2])
            xs.append(None)
            ys.append(None)
            zs.append(None)

            if col not in filament_groups:
                filament_groups[col] = {"xs": [], "ys": [], "zs": [], "width": w, "name": lbl}
            filament_groups[col]["xs"].extend(xs)
            filament_groups[col]["ys"].extend(ys)
            filament_groups[col]["zs"].extend(zs)

    for col, group in filament_groups.items():
        fig.add_trace(
            go.Scatter3d(
                x=group["xs"],
                y=group["ys"],
                z=group["zs"],
                mode="lines",
                line=dict(color=col, width=group["width"]),
                hoverinfo="none",
                showlegend=False,
                name=group["name"],
            )
        )

    # 3. Draw Galactic Cluster Cores & Stellar Nodes
    node_x, node_y, node_z = [], [], []
    node_colors, node_sizes, node_text, node_hover, node_ids = [], [], [], [], []

    for nid, n in nodes.items():
        node_x.append(n["x"])
        node_y.append(n["y"])
        node_z.append(n["z"])
        node_ids.append(nid)

        is_clust = nid.startswith("CLUST_") or nid == "COSMIC_CORE"
        is_highlighted = (selected_cluster and n.get("cluster") == selected_cluster)

        col = "#ffffff" if is_highlighted else n.get("color", "#38bdf8")
        node_colors.append(col)
        node_sizes.append(n.get("size", 16) + (8 if is_highlighted else 0))

        short_label = n.get("label", nid).split("\n")[0]
        node_text.append(short_label if is_clust else "")

        hover_html = (
            f"<b>{short_label}</b><br>"
            f"<b>Galactic Cluster:</b> {n.get('cluster_name', 'Universe')}<br>"
            f"<b>Role:</b> {n.get('role', '')}<br>"
            f"<i>Desc:</i> {n.get('desc', '')[:140]}...<br>"
            f"<b>Stellar Luminosity:</b> {n.get('luminosity', 0.8)*100:.0f}%"
        )
        node_hover.append(hover_html)

    fig.add_trace(
        go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode="markers+text",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                opacity=0.96,
                line=dict(color="#ffffff", width=1.5),
            ),
            text=node_text,
            textposition="top center",
            textfont=dict(color="#f8fafc", size=10, family="Outfit, sans-serif"),
            hoverinfo="text",
            hovertext=node_hover,
            customdata=node_ids,
            name="Galactic Nodes",
        )
    )

    # 4. Highlight Galactic Nucleus Halo
    if "COSMIC_CORE" in nodes:
        core = nodes["COSMIC_CORE"]
        fig.add_trace(
            go.Scatter3d(
                x=[core["x"]],
                y=[core["y"]],
                z=[core["z"]],
                mode="markers",
                marker=dict(
                    size=48,
                    color="rgba(245, 158, 11, 0.22)",
                    line=dict(color="#f59e0b", width=2.5),
                ),
                hoverinfo="none",
                showlegend=False,
            )
        )

    # 5. Cosmic Environment Layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            bgcolor="#030712",
            camera=dict(
                eye=dict(x=1.85, y=1.85, z=1.35),
                up=dict(x=0, y=0, z=1),
            ),
        ),
        paper_bgcolor="#030712",
        plot_bgcolor="#030712",
        margin=dict(l=0, r=0, t=10, b=0),
        height=540,
        legend=dict(
            font=dict(color="#94a3b8"),
            bgcolor="rgba(15, 23, 42, 0.7)",
            bordercolor="rgba(148, 163, 184, 0.2)",
            borderwidth=1,
            x=0.02,
            y=0.95,
        ),
    )

    return fig
