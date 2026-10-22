"""Interactive 3D Quantum Bloch Sphere Visualizer for Quantum Knowledge Weaver.
Maps the query's wave-particle superposition state:
|Psi> = alpha |Aql (Logic / Particle)> + beta |Qalb (Spirit / Wave)>
into 3D Hilbert Space on the unit Bloch Sphere.
"""

import math
import numpy as np
import plotly.graph_objects as go


def create_bloch_sphere_figure(
    particle_prob: float = 0.5,
    wave_prob: float = 0.5,
    entropy_score: float = 0.5,
    dominant_state: str = "Equilibrium",
    spiritual_maqam: Optional[str] = None,
) -> go.Figure:
    """Constructs an interactive 3D Plotly figure of the Quantum Bloch Sphere."""
    # Quantum Angles
    alpha = math.sqrt(max(0.0, min(1.0, particle_prob)))
    beta = math.sqrt(max(0.0, min(1.0, wave_prob)))
    
    # theta in [0, pi]
    theta = 2.0 * math.acos(max(-1.0, min(1.0, alpha)))
    phi = (2.0 * math.pi * entropy_score) % (2.0 * math.pi)

    # Statevector endpoint on sphere
    vx = math.sin(theta) * math.cos(phi)
    vy = math.sin(theta) * math.sin(phi)
    vz = math.cos(theta)

    fig = go.Figure()

    # 1. Wireframe Sphere Meshes
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))

    fig.add_trace(
        go.Surface(
            x=xs,
            y=ys,
            z=zs,
            opacity=0.12,
            colorscale=[[0, "#3b82f6"], [0.5, "#a855f7"], [1, "#10b981"]],
            showscale=False,
            hoverinfo="skip",
        )
    )

    # 2. Equator Ring (z = 0, Harmonious Balance Plane)
    t = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(
        go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines",
            line=dict(color="#c084fc", width=3, dash="dash"),
            name="Equatorial Balance Plane",
            hoverinfo="name",
        )
    )

    # 3. Coordinate Axes
    axis_len = 1.3
    # Z-axis: |Aql> (North) to |Qalb> (South)
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, 0],
            z=[-axis_len, axis_len],
            mode="lines+text",
            line=dict(color="#94a3b8", width=3),
            text=["", ""],
            showlegend=False,
            hoverinfo="skip",
        )
    )
    # X and Y axes
    fig.add_trace(
        go.Scatter3d(
            x=[-axis_len, axis_len],
            y=[0, 0],
            z=[0, 0],
            mode="lines",
            line=dict(color="#475569", width=2),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[-axis_len, axis_len],
            z=[0, 0],
            mode="lines",
            line=dict(color="#475569", width=2),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # 4. Poles & Milestone Markers
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0, 1.1, -1.1],
            y=[0, 0, 0, 0],
            z=[1.15, -1.15, 0, 0],
            mode="text",
            text=[
                "<b>|Aql⟩ (Logic / Particle)</b>",
                "<b>|Qalb⟩ (Spirit / Wave)</b>",
                "+X (Phase 0)",
                "-X (Phase π)",
            ],
            textfont=dict(color=["#60a5fa", "#34d399", "#cbd5e1", "#cbd5e1"], size=[13, 13, 10, 10]),
            showlegend=False,
        )
    )

    # 5. Quantum State Vector Line: Origin -> (vx, vy, vz)
    vector_color = "#38bdf8" if "Aql" in dominant_state else ("#34d399" if "Qalb" in dominant_state else "#e879f9")
    fig.add_trace(
        go.Scatter3d(
            x=[0, vx],
            y=[0, vy],
            z=[0, vz],
            mode="lines",
            line=dict(color=vector_color, width=8),
            name=f"|Ψ⟩ Statevector: {dominant_state}",
        )
    )

    # 6. Quantum State Vector Tip (Marker)
    tip_text = f"|Ψ⟩ ({dominant_state})<br>θ={math.degrees(theta):.1f}°, φ={math.degrees(phi):.1f}°"
    if spiritual_maqam:
        tip_text += f"<br>🕊️ {spiritual_maqam}"

    fig.add_trace(
        go.Scatter3d(
            x=[vx],
            y=[vy],
            z=[vz],
            mode="markers+text",
            marker=dict(size=10, color=vector_color, symbol="diamond"),
            text=[tip_text],
            textposition="top center",
            textfont=dict(color="#ffffff", size=12),
            name="Current Statevector Tip",
        )
    )

    # Camera & Layout styling
    title_text = f"⚛️ 3D Quantum Bloch Sphere Superposition: |Ψ⟩ = {alpha:.3f}|Aql⟩ + {beta:.3f}|Qalb⟩"
    if spiritual_maqam:
        title_text += f" | {spiritual_maqam}"

    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=14, color="#f8fafc"),
        ),
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            bgcolor="#0b0f19",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2),
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=450,
        showlegend=False,
    )

    return fig
