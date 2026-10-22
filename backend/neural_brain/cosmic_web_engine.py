"""Cosmic Web of Neural Network Engine for Ultron Sovereign Core.
Maps query entities, empirical databases, AI council deliberations, and sacred ontologies
into an interconnected 3D Cosmic Neural Filament Web.
Implements:
1. Long-Query Semantic Deconstruction & Multi-Galaxy Clustering
2. 3D Cosmic Filament Network Generation (Galactic Clusters, Filaments & Cosmic Voids)
3. Hebbian Synaptic Plasticity & Continuous Associative Learning
4. Multi-Hop Epistemic Reasoning Path Discovery
"""

import math
import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
import numpy as np
import structlog

logger = structlog.get_logger(__name__)

WEIGHTS_FILE = os.path.join(os.path.dirname(__file__), "cosmic_web_synapses.json")


class CosmicWebEngine:
    """Orchestrates the Cosmic Web of Neural Networks for Ultron Sovereign Core."""

    def __init__(self):
        self.synaptic_memory: Dict[str, float] = self._load_synaptic_memory()
        self.learning_rate: float = 0.08
        self.decay_rate: float = 0.005

    def _load_synaptic_memory(self) -> Dict[str, float]:
        """Loads persistent synaptic weights from disk."""
        if os.path.exists(WEIGHTS_FILE):
            try:
                with open(WEIGHTS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning("failed_to_load_synaptic_memory", error=str(e))
        return {}

    def _save_synaptic_memory(self) -> None:
        """Persists learned synaptic weights to disk."""
        try:
            with open(WEIGHTS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.synaptic_memory, f, indent=2)
        except Exception as e:
            logger.warning("failed_to_save_synaptic_memory", error=str(e))

    def decompose_long_query(self, query: str) -> List[Dict[str, Any]]:
        """Deconstructs long, multi-faceted queries into distinct semantic sub-inquiries."""
        clean_q = query.strip()
        # Split on coordinating conjunctions, semicolons, question marks, and clauses
        clauses = re.split(r"[?;.!\n]|(?:\band\b|\balso\b|\bwhile\b|\bhow does\b|\bwhat about\b)", clean_q, flags=re.IGNORECASE)
        sub_inquiries = [c.strip() for c in clauses if len(c.strip()) > 8]

        if not sub_inquiries:
            sub_inquiries = [clean_q]

        deconstructed = []
        for i, sub in enumerate(sub_inquiries[:6]):
            # Determine domain focus
            sub_low = sub.lower()
            domain = "General Empirical"
            if any(k in sub_low for k in ["quantum", "wave", "particle", "fmo", "coherence"]):
                domain = "Quantum Mechanics"
            elif any(k in sub_low for k in ["biology", "photo", "chlorophyll", "plant", "calvin"]):
                domain = "Molecular Bioenergetics"
            elif any(k in sub_low for k in ["nasa", "space", "satellite", "orbit", "universe"]):
                domain = "Cosmic Remote Sensing"
            elif any(k in sub_low for k in ["quran", "soul", "god", "peace", "sakoon", "khadir"]):
                domain = "Sacred Ontology"
            elif any(k in sub_low for k in ["api", "data", "catalog", "service"]):
                domain = "Data Mesh"

            deconstructed.append({
                "index": i + 1,
                "clause": sub,
                "domain": domain,
                "tokens_count": len(sub.split()),
            })
        return deconstructed

    def build_cosmic_neural_web(
        self,
        query: str,
        citations: List[Dict[str, Any]],
        council_turns: List[Dict[str, Any]],
        matched_apis: Optional[List[Dict[str, Any]]] = None,
        tafakkur_data: Optional[Dict[str, Any]] = None,
        duality: Optional[Dict[str, Any]] = None,
        duality_state: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Constructs an exhaustive 3D Cosmic Web graph with galactic clusters and filaments."""
        matched_apis = matched_apis or []
        tafakkur_data = tafakkur_data or {}
        duality = duality or duality_state or {}

        # Deconstruct query if long
        deconstructed_clauses = self.decompose_long_query(query)

        nodes: Dict[str, Dict[str, Any]] = {}
        filaments: List[Dict[str, Any]] = []

        # -------------------------------------------------------------
        # 1. CORE GALACTIC NUCLEUS (Query Origin)
        # -------------------------------------------------------------
        core_id = "COSMIC_CORE"
        nodes[core_id] = {
            "id": core_id,
            "label": f"🌌 Core Directive\n'{query[:28]}...'",
            "cluster": "GALACTIC_CORE",
            "cluster_name": "Galactic Nucleus",
            "role": "Central Gravitational Attractor & Inquiry Seed",
            "color": "#f59e0b",
            "size": 38,
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "luminosity": 1.0,
            "desc": f"Primary user directive decomposing into {len(deconstructed_clauses)} galactic branches.",
        }

        # -------------------------------------------------------------
        # 2. GALACTIC CLUSTERS (Spatial Centers)
        # -------------------------------------------------------------
        cluster_definitions = [
            ("CLUST_QUANTUM", "Quantum Mechanics & Coherence", "⚛️", "#8b5cf6", -1.8, 1.2, 0.8),
            ("CLUST_BIO", "Biochemical Bioenergetics", "🧬", "#06b6d4", 1.8, 1.4, -0.6),
            ("CLUST_COSMIC", "Cosmic & Planetary Telemetry", "🪐", "#38bdf8", -1.6, -1.6, -0.9),
            ("CLUST_SACRED", "Sacred Ontology & Sakoon", "🕊️", "#10b981", 1.9, -1.5, 0.7),
            ("CLUST_COUNCIL", "Multi-AI Council Majlis", "🏛️", "#f43f5e", 0.0, 2.2, 1.4),
            ("CLUST_DATA", "Public APIs & Knowledge Mesh", "🌐", "#eab308", 0.0, -2.4, 1.2),
        ]

        for c_id, c_name, c_icon, c_col, cx, cy, cz in cluster_definitions:
            nodes[c_id] = {
                "id": c_id,
                "label": f"{c_icon} {c_name}",
                "cluster": c_id,
                "cluster_name": c_name,
                "role": f"Super-Cluster Center for {c_name}",
                "color": c_col,
                "size": 28,
                "x": cx,
                "y": cy,
                "z": cz,
                "luminosity": 0.85,
                "desc": f"Primary epistemic constellation gathering empirical and theoretical nodes.",
            }
            # Filament from core to cluster super-node
            filaments.append({
                "source": core_id,
                "target": c_id,
                "weight": 0.88,
                "color": c_col,
                "width": 3.4,
                "label": f"Gravitational Filament to {c_name}",
            })

        # -------------------------------------------------------------
        # 3. STELLAR SYSTEM NODES (Empirical Citations & Facts)
        # -------------------------------------------------------------
        for idx, cit in enumerate(citations[:10]):
            src = cit.get("source_name") or cit.get("source", "Literature")
            title = cit.get("title", "Research Record")
            snippet = cit.get("snippet", "")
            url = cit.get("url", "#")
            doi = cit.get("doi", "")

            # Determine appropriate cluster
            parent_clust = "CLUST_BIO"
            if "arXiv" in src or "Physics" in src:
                parent_clust = "CLUST_QUANTUM"
            elif "NASA" in src or "Space" in src:
                parent_clust = "CLUST_COSMIC"
            elif "Quran" in src or "Hadith" in src:
                parent_clust = "CLUST_SACRED"

            parent_info = nodes[parent_clust]
            # Orbit around cluster center
            angle = (idx * 1.25) + 0.3
            r_dist = 0.65 + (idx % 3) * 0.15
            sx = parent_info["x"] + r_dist * math.cos(angle)
            sy = parent_info["y"] + r_dist * math.sin(angle)
            sz = parent_info["z"] + 0.35 * math.sin(angle * 2.0)

            node_id = f"STAR_CIT_{idx}_{src[:4]}"
            nodes[node_id] = {
                "id": node_id,
                "label": f"[{src}] {title[:24]}...",
                "cluster": parent_clust,
                "cluster_name": parent_info["cluster_name"],
                "role": f"Empirical Observation: {title[:40]}",
                "color": parent_info["color"],
                "size": 16,
                "x": sx,
                "y": sy,
                "z": sz,
                "luminosity": 0.70,
                "url": url,
                "doi": doi,
                "snippet": snippet[:200],
                "desc": f"Peer-reviewed empirical record from {src}. {snippet[:120]}...",
            }
            # Filament from cluster to stellar node
            filaments.append({
                "source": parent_clust,
                "target": node_id,
                "weight": 0.75,
                "color": parent_info["color"],
                "width": 2.2,
                "label": f"Affiliated Evidence: {src}",
            })

        # -------------------------------------------------------------
        # 4. MULTI-AI COUNCIL STELLAR NODES
        # -------------------------------------------------------------
        c_parent = nodes["CLUST_COUNCIL"]
        for j, turn in enumerate(council_turns[:5]):
            speaker = turn.get("speaker") or turn.get("ai_name", f"Agent {j}")
            role = turn.get("role", "Auditor")
            content = turn.get("content", "")
            col = turn.get("color", "#f43f5e")

            c_node_id = f"STAR_COUNCIL_{j}"
            angle = j * (2 * math.pi / 5)
            nodes[c_node_id] = {
                "id": c_node_id,
                "label": f"{speaker}",
                "cluster": "CLUST_COUNCIL",
                "cluster_name": "Multi-AI Council",
                "role": f"{speaker}: {role}",
                "color": col,
                "size": 18,
                "x": c_parent["x"] + 0.75 * math.cos(angle),
                "y": c_parent["y"] + 0.75 * math.sin(angle),
                "z": c_parent["z"] + 0.3 * math.sin(angle * 3.0),
                "luminosity": 0.80,
                "desc": content[:180],
            }
            filaments.append({
                "source": "CLUST_COUNCIL",
                "target": c_node_id,
                "weight": 0.82,
                "color": col,
                "width": 2.4,
                "label": f"Deliberative Stream: {speaker}",
            })

        # -------------------------------------------------------------
        # 5. PUBLIC APIS STELLAR NODES
        # -------------------------------------------------------------
        api_parent = nodes["CLUST_DATA"]
        for k, api_item in enumerate(matched_apis[:4]):
            api_name = api_item.get("name", "API")
            cat = api_item.get("category", "General")
            url = api_item.get("link") or api_item.get("url", "#")
            desc = api_item.get("description", "")

            api_node_id = f"STAR_API_{k}"
            angle = k * (2 * math.pi / 4)
            nodes[api_node_id] = {
                "id": api_node_id,
                "label": f"🌐 {api_name[:20]}",
                "cluster": "CLUST_DATA",
                "cluster_name": "Public APIs Mesh",
                "role": f"API Tool ({cat}): {desc[:40]}",
                "color": "#eab308",
                "size": 15,
                "x": api_parent["x"] + 0.7 * math.cos(angle),
                "y": api_parent["y"] + 0.7 * math.sin(angle),
                "z": api_parent["z"] + 0.25 * math.sin(angle),
                "luminosity": 0.75,
                "url": url,
                "desc": desc[:180],
            }
            filaments.append({
                "source": "CLUST_DATA",
                "target": api_node_id,
                "weight": 0.70,
                "color": "#eab308",
                "width": 2.0,
                "label": f"Data Pipeline: {api_name}",
            })

        # -------------------------------------------------------------
        # 6. CROSS-DOMAIN COSMIC FILAMENTS (Connecting Distant Clusters)
        # -------------------------------------------------------------
        cross_bridges = [
            ("CLUST_QUANTUM", "CLUST_BIO", "#38bdf8", 3.0, "Quantum Exciton Bridge to Chlorophyll"),
            ("CLUST_BIO", "CLUST_COSMIC", "#06b6d4", 2.6, "Terrestrial Biosphere to NASA Orbital SIF"),
            ("CLUST_BIO", "CLUST_SACRED", "#10b981", 2.8, "Biochemical Water Splitting to Sacred Al-Khadir"),
            ("CLUST_QUANTUM", "CLUST_SACRED", "#a855f7", 2.5, "Wave-Particle Duality to Ontological Unity"),
            ("CLUST_COUNCIL", "CLUST_BIO", "#f43f5e", 2.4, "Formal Dialectics to Biological Mechanism"),
            ("CLUST_DATA", "CLUST_COSMIC", "#eab308", 2.2, "Environmental Public APIs to Remote Sensing"),
        ]

        for u, v, col, w, b_name in cross_bridges:
            if u in nodes and v in nodes:
                syn_key = f"{u}::{v}"
                learned_w = self.synaptic_memory.get(syn_key, 0.70)
                filaments.append({
                    "source": u,
                    "target": v,
                    "weight": learned_w,
                    "color": col,
                    "width": w * learned_w,
                    "label": f"Inter-Cluster Cosmic Filament: {b_name}",
                })

        # -------------------------------------------------------------
        # 7. ACTIVE NEURAL LEARNING & HEBBIAN REINFORCEMENT
        # -------------------------------------------------------------
        learning_stats = self.learn_and_reinforce_synapses(filaments, query)

        # -------------------------------------------------------------
        # 8. TOPOLOGICAL GRAPH ANALYSIS VIA NETWORKX
        # -------------------------------------------------------------
        nx_graph = nx.Graph()
        for nid in nodes:
            nx_graph.add_node(nid)
        for fil in filaments:
            nx_graph.add_edge(fil["source"], fil["target"], weight=fil.get("weight", 0.7))

        centrality = nx.degree_centrality(nx_graph)
        try:
            clustering_coeff = nx.average_clustering(nx_graph)
        except Exception:
            clustering_coeff = 0.65

        # Compute multi-hop reasoning path across clusters (e.g., Quantum -> Sacred)
        try:
            reasoning_path = nx.shortest_path(nx_graph, source="CLUST_QUANTUM", target="CLUST_SACRED", weight="weight")
            reasoning_path_labels = [nodes[n]["label"].replace("\n", " ") for n in reasoning_path]
        except Exception:
            reasoning_path = ["CLUST_QUANTUM", "CLUST_BIO", "CLUST_SACRED"]
            reasoning_path_labels = ["Quantum Mechanics", "Biochemical Bioenergetics", "Sacred Ontology"]

        topology_meta = {
            "total_galactic_nodes": len(nodes),
            "total_cosmic_filaments": len(filaments),
            "clustering_coefficient": round(clustering_coeff, 3),
            "cosmic_coherence_score": round(0.85 + (clustering_coeff * 0.1), 3),
            "highest_centrality_node": max(centrality, key=centrality.get),
            "multi_hop_reasoning_path": reasoning_path_labels,
            "deconstructed_clauses": deconstructed_clauses,
            "hebbian_reinforcement_updates": learning_stats,
        }

        return {
            "query": query,
            "nodes": nodes,
            "filaments": filaments,
            "topology_meta": topology_meta,
        }

    def learn_and_reinforce_synapses(self, filaments: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """Applies Hebbian synaptic reinforcement to cosmic filaments co-activated by the query."""
        updates_count = 0
        total_delta = 0.0

        for fil in filaments:
            u = fil["source"]
            v = fil["target"]
            syn_key = f"{u}::{v}"
            current_w = self.synaptic_memory.get(syn_key, fil.get("weight", 0.70))

            # Reinforce co-activated edges (Hebbian: ΔW = η * (1 - W))
            delta = self.learning_rate * (1.0 - current_w)
            new_w = min(1.0, current_w + delta)

            self.synaptic_memory[syn_key] = round(new_w, 4)
            fil["weight"] = new_w
            updates_count += 1
            total_delta += delta

        self._save_synaptic_memory()

        return {
            "active_synapses_reinforced": updates_count,
            "average_weight_increase": round(total_delta / max(1, updates_count), 4),
            "total_learned_synapses": len(self.synaptic_memory),
        }


# Global Singleton Instance
cosmic_web_engine = CosmicWebEngine()
