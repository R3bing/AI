"""Dynamic Prompt Neural Pathway Engine for Ultron Sovereign Core.
Maps any user inquiry/prompt into an active 3D spherical constellation on the
cybernetic globe, interconnecting empirical databases, cognitive brain blocks,
Multi-AI Council agents, and sacred ontological nodes via curved geodesic strings.
"""

import math
import hashlib
from typing import Dict, List, Any, Optional


def _spherical_to_cartesian(theta_deg: float, phi_deg: float, radius: float = 2.2):
    """Converts spherical coordinates (theta in [-180, 180], phi in [0, 180]) to Cartesian (x, y, z)."""
    theta_rad = math.radians(theta_deg)
    phi_rad = math.radians(phi_deg)
    x = radius * math.sin(phi_rad) * math.cos(theta_rad)
    y = radius * math.sin(phi_rad) * math.sin(theta_rad)
    z = radius * math.cos(phi_rad)
    return x, y, z


class DynamicPromptPathwayEngine:
    """Constructs dynamic 3D spherical node networks and geodesic synaptic strings for any prompt."""

    def build_pathway(
        self,
        query: str,
        citations: List[Dict[str, Any]],
        council_turns: List[Dict[str, Any]],
        matched_apis: Optional[List[Dict[str, Any]]] = None,
        duality_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generates a complete 3D spherical graph specification for the prompt."""
        clean_q = query.strip()
        matched_apis = matched_apis or []
        duality_state = duality_state or {}

        nodes: Dict[str, Dict[str, Any]] = {}
        pathways: List[Dict[str, Any]] = []

        # -------------------------------------------------------------
        # 1. CORE DIRECTIVE SEED NODE (Front Equator)
        # -------------------------------------------------------------
        core_id = "PROMPT_CORE"
        nodes[core_id] = {
            "id": core_id,
            "name": f"⚡ DIRECTIVE: {clean_q[:35]}",
            "short_name": "Active Directive",
            "role": "Prompt Origin & Operational Intent",
            "icon": "⚡",
            "category": "User Directive",
            "color": "#f59e0b",
            "size": 24,
            "sphere_coords": {"theta_deg": 0.0, "phi_deg": 90.0, "radius": 2.28},
            "url": "#",
            "snippet": f"User prompt: '{clean_q}'. Coordinates all dimensional resources into unified synthesis.",
            "link_tab": "📑 1. Epistemic Synthesis",
            "details": {
                "inquiry": clean_q,
                "total_citations": len(citations),
                "council_participants": len(council_turns),
            },
        }

        # -------------------------------------------------------------
        # 2. CORE COGNITIVE ARCHITECTURAL BLOCKS (Anchor Points)
        # -------------------------------------------------------------
        anchors = [
            ("B1_THALAMUS", "Sensory Thalamus", "Tokenization & Intent Intake", "🧩", "#a855f7", 0.0, 70.0, "Input"),
            ("B4_QAOA", "QAOA 11-Qubit Router", "Dicke Subspace API Routing", "⚛️", "#06b6d4", 0.0, 40.0, "Quantum Routing"),
            ("B2_AQL", "Aql Cerebral Hemisphere", "Empirical Science & Logic (Left Brain)", "🧠", "#38bdf8", -50.0, 45.0, "Empirical Hemisphere"),
            ("B3_QALB", "Qalb Sacred Matrix", "Ontological Tafakkur & Sakoon (Right Brain)", "🕊️", "#10b981", 50.0, 45.0, "Sacred Hemisphere"),
            ("B7_OMNI_FUSION", "Omni-Resource Fusion", "Unified Composite Synthesis", "🏛️", "#ef4444", 0.0, 120.0, "Synthesis Core"),
        ]

        for b_id, s_name, role, icon, col, th, ph, cat in anchors:
            nodes[b_id] = {
                "id": b_id,
                "name": f"Block: {s_name}",
                "short_name": s_name,
                "role": role,
                "icon": icon,
                "category": cat,
                "color": col,
                "size": 17,
                "sphere_coords": {"theta_deg": th, "phi_deg": ph, "radius": 2.20},
                "url": "#",
                "snippet": f"Core cognitive block responsible for {role.lower()}.",
                "link_tab": "📑 1. Epistemic Synthesis" if b_id == "B7_OMNI_FUSION" else "⚛️ 7. Quantum & Vitals",
                "details": {"block_id": b_id, "category": cat},
            }

        # Direct backbone strings
        pathways.append({"source": "PROMPT_CORE", "target": "B1_THALAMUS", "color": "#f59e0b", "width": 3.8, "name": "Sensory Intake"})
        pathways.append({"source": "B1_THALAMUS", "target": "B4_QAOA", "color": "#a855f7", "width": 3.2, "name": "Quantum Routing Dispatch"})

        # -------------------------------------------------------------
        # 3. EMPIRICAL REPOSITORY CITATION NODES (Northern Hemisphere)
        # -------------------------------------------------------------
        n_cits = min(len(citations), 8)
        empirical_node_ids = []
        for i in range(n_cits):
            c = citations[i]
            src = c.get("source_name") or c.get("source") or "Repository"
            title = c.get("title", "Research Record")
            url = c.get("url", "#")
            snippet = c.get("snippet", "")
            score = c.get("relevance_score", 0.9)

            c_id = f"CIT_{i}_{src[:4].upper()}"

            # Distribute along Northern Hemisphere
            th_angle = -110.0 + (220.0 * (i / max(1, n_cits - 1)))
            ph_angle = 30.0 + 15.0 * math.sin(i * 1.5)

            col = "#38bdf8"
            icon = "📚"
            link_tab = "🔬 2. Literature Matrix"

            if "NASA" in src:
                col = "#06b6d4"
                icon = "🪐"
            elif "PubMed" in src:
                col = "#10b981"
                icon = "🧬"
            elif "arXiv" in src:
                col = "#8b5cf6"
                icon = "⚛️"
            elif "PubChem" in src:
                col = "#f59e0b"
                icon = "🧪"
            elif "Quran" in src or "Hadith" in src:
                col = "#34d399"
                icon = "📖"
                link_tab = "🕊️ 5. Sacred Tafakkur"
            elif "Wikipedia" in src:
                col = "#94a3b8"
                icon = "🌐"

            nodes[c_id] = {
                "id": c_id,
                "name": f"[{src}] {title[:32]}",
                "short_name": f"{icon} {src[:10]}",
                "role": f"Verified Evidence: {title[:40]}",
                "icon": icon,
                "category": f"Empirical: {src}",
                "color": col,
                "size": 14,
                "sphere_coords": {"theta_deg": th_angle, "phi_deg": ph_angle, "radius": 2.22},
                "url": url,
                "snippet": snippet[:220],
                "link_tab": link_tab,
                "details": {
                    "source": src,
                    "title": title,
                    "url": url,
                    "relevance_match": f"{score*100:.0f}%",
                    "snippet": snippet,
                },
            }
            empirical_node_ids.append((c_id, src))

            # String from Quantum Router to this Empirical Database
            pathways.append({"source": "B4_QAOA", "target": c_id, "color": col, "width": 2.2, "name": f"QAOA -> {src}"})

            # String from Empirical Database to Aql (Left Brain) or Qalb (Right Brain)
            if "Quran" in src or "Hadith" in src:
                pathways.append({"source": c_id, "target": "B3_QALB", "color": "#10b981", "width": 2.4, "name": f"{src} -> Qalb"})
            else:
                pathways.append({"source": c_id, "target": "B2_AQL", "color": "#38bdf8", "width": 2.4, "name": f"{src} -> Aql"})

        # -------------------------------------------------------------
        # 4. MULTI-AI COUNCIL PARTICIPANT NODES (Equatorial Flanks)
        # -------------------------------------------------------------
        council_node_ids = []
        for j, turn in enumerate(council_turns[:5]):
            speaker = turn.get("speaker", f"AI Agent {j+1}")
            role = turn.get("role", "Dialectical Auditor")
            avatar = turn.get("avatar", "🤖")
            col = turn.get("color", "#f43f5e")
            content = turn.get("content", "")
            cot = turn.get("reasoning_trace", "")

            cn_id = f"COUNCIL_{j}"
            # Flank along Equator
            th_c = -75.0 + (38.0 * j)
            ph_c = 85.0 + 8.0 * math.sin(j)

            nodes[cn_id] = {
                "id": cn_id,
                "name": f"{avatar} {speaker}",
                "short_name": speaker.split()[0],
                "role": role,
                "icon": avatar,
                "category": "Multi-AI Council",
                "color": col,
                "size": 16,
                "sphere_coords": {"theta_deg": th_c, "phi_deg": ph_c, "radius": 2.24},
                "url": "#",
                "snippet": content[:220],
                "link_tab": "🏛️ 4. Multi-AI Council",
                "details": {
                    "speaker": speaker,
                    "role": role,
                    "reasoning_trace": cot,
                    "entropy": turn.get("entropy", 0.5),
                },
            }
            council_node_ids.append(cn_id)

            # Strings from Aql and Qalb to Council
            pathways.append({"source": "B2_AQL", "target": cn_id, "color": "#38bdf8", "width": 2.0, "name": "Aql -> Council"})
            pathways.append({"source": "B3_QALB", "target": cn_id, "color": "#10b981", "width": 2.0, "name": "Qalb -> Council"})
            # String from Council to Omni-Fusion Core
            pathways.append({"source": cn_id, "target": "B7_OMNI_FUSION", "color": col, "width": 2.5, "name": f"{speaker} -> Omni-Fusion"})

        # -------------------------------------------------------------
        # 5. PUBLIC APIS NODES (Southern Hemisphere)
        # -------------------------------------------------------------
        for k, api_item in enumerate(matched_apis[:4]):
            name = api_item.get("name", "Public API")
            url = api_item.get("url", "#")
            desc = api_item.get("description", "")
            cat = api_item.get("category", "General")

            api_id = f"API_{k}"
            th_api = -60.0 + (40.0 * k)
            ph_api = 135.0

            nodes[api_id] = {
                "id": api_id,
                "name": f"🌐 {name}",
                "short_name": name[:12],
                "role": f"Public API ({cat}): {desc[:40]}",
                "icon": "🌐",
                "category": f"Public API ({cat})",
                "color": "#f59e0b",
                "size": 13,
                "sphere_coords": {"theta_deg": th_api, "phi_deg": ph_api, "radius": 2.21},
                "url": url,
                "snippet": desc[:200],
                "link_tab": "🌐 6. Public APIs",
                "details": api_item,
            }
            # String from B7_OMNI_FUSION to Public APIs
            pathways.append({"source": "B7_OMNI_FUSION", "target": api_id, "color": "#f59e0b", "width": 2.0, "name": f"Fusion -> {name}"})

        # Close the loop: Omni-Fusion back to Core Directive
        pathways.append({"source": "B7_OMNI_FUSION", "target": "PROMPT_CORE", "color": "#10b981", "width": 3.8, "name": "Synthesis Emitted"})

        return {
            "query": clean_q,
            "nodes": nodes,
            "pathways": pathways,
            "total_nodes": len(nodes),
            "total_pathways": len(pathways),
            "timestamp": hashlib.md5(clean_q.encode()).hexdigest()[:8],
        }


# Global Singleton Instance
dynamic_prompt_pathway_engine = DynamicPromptPathwayEngine()
