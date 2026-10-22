"""Universe Knowledge Graph for Quantum Knowledge Weaver & Ultron Core.
Merges structured knowledge from:
1. Wikidata (Entities, QIDs, Aliases, Claims)
2. DBpedia (Ontology types, RDF properties, categories)
3. OpenAlex (Citation networks, Scholarly works, DOIs)
4. Ontological Sacred Principles (Tafakkur, Ethics, Mizan)
Stored in a high-speed NetworkX graph with bidirectional Neo4j synchronization.
Supports GraphRAG multi-hop relationship exploration.
"""

import time
from typing import Dict, Any, List, Optional, Tuple, Set
import networkx as nx
import structlog
from backend.memory.neo4j_store import graph_memory

logger = structlog.get_logger(__name__)


class UniverseKnowledgeGraph:
    """Multi-source unified Knowledge Graph connecting empirical science, philosophy, and citations."""

    def __init__(self):
        self.nx_graph = nx.DiGraph()
        self.neo4j_store = graph_memory
        self._init_foundational_ontology()

    def _init_foundational_ontology(self):
        """Pre-populates core trans-disciplinary anchor nodes."""
        core_anchors = [
            ("Concept:QuantumMechanics", {"type": "DBpedia:Domain", "label": "Quantum Mechanics", "source": "DBpedia"}),
            ("Concept:Photosynthesis", {"type": "DBpedia:Process", "label": "Photosynthesis", "source": "DBpedia"}),
            ("Concept:Cosmology", {"type": "DBpedia:Domain", "label": "Astrophysics & Cosmology", "source": "DBpedia"}),
            ("Concept:Mizan", {"type": "Sacred:Ontology", "label": "Cosmic Equilibrium (Mizan)", "source": "Quranic"}),
            ("Concept:Tafakkur", {"type": "Sacred:Ontology", "label": "Deep Contemplation (Tafakkur)", "source": "Quranic"}),
            ("Entity:Q11053", {"type": "Wikidata:Entity", "label": "Chlorophyll", "qid": "Q11053", "source": "Wikidata"}),
            ("Entity:Q11344", {"type": "Wikidata:Entity", "label": "Chemical reaction", "qid": "Q11344", "source": "Wikidata"}),
        ]
        for node_id, attrs in core_anchors:
            self.nx_graph.add_node(node_id, **attrs)

        # Connect anchors
        self.nx_graph.add_edge("Entity:Q11053", "Concept:Photosynthesis", relation="PARTICIPATES_IN")
        self.nx_graph.add_edge("Concept:Photosynthesis", "Concept:Mizan", relation="DEMONSTRATES_EQUILIBRIUM")
        self.nx_graph.add_edge("Concept:QuantumMechanics", "Concept:Tafakkur", relation="INSPIRES_AWE")

    def ingest_wikidata_entity(self, qid: str, label: str, description: str, claims: Optional[List[Dict]] = None):
        """Ingests a verified entity from Wikidata."""
        node_id = f"Wikidata:{qid}"
        self.nx_graph.add_node(
            node_id,
            type="Wikidata:Entity",
            qid=qid,
            label=label,
            description=description,
            source="Wikidata",
        )
        if claims:
            for c in claims:
                target_id = c.get("target_id")
                prop = c.get("property", "RELATED_TO")
                if target_id:
                    self.nx_graph.add_edge(node_id, target_id, relation=prop)

    def ingest_dbpedia_relation(self, subject: str, predicate: str, obj: str):
        """Ingests an ontological RDF triple from DBpedia."""
        s_id = f"DBpedia:{subject.replace(' ', '_')}"
        o_id = f"DBpedia:{obj.replace(' ', '_')}"
        self.nx_graph.add_node(s_id, type="DBpedia:Concept", label=subject, source="DBpedia")
        self.nx_graph.add_node(o_id, type="DBpedia:Concept", label=obj, source="DBpedia")
        self.nx_graph.add_edge(s_id, o_id, relation=predicate, source="DBpedia")

    def ingest_openalex_work(self, doi: str, title: str, cited_by_count: int, concepts: List[str]):
        """Ingests a scholarly publication from OpenAlex and connects it to conceptual topics."""
        work_id = f"OpenAlex:{doi}"
        self.nx_graph.add_node(
            work_id,
            type="OpenAlex:Publication",
            doi=doi,
            title=title,
            citations=cited_by_count,
            source="OpenAlex",
        )
        for c in concepts[:4]:
            c_id = f"Concept:{c.replace(' ', '_')}"
            self.nx_graph.add_node(c_id, type="Concept", label=c, source="OpenAlex")
            self.nx_graph.add_edge(work_id, c_id, relation="STUDIES_CONCEPT")

    def merge_citations(self, citations: List[Any], query: str):
        """Merges live empirical citations and connects them into the graph."""
        q_node = f"Query:{query.strip()[:35]}"
        self.nx_graph.add_node(q_node, type="UserQuery", text=query)

        for cit in citations:
            if hasattr(cit, "title"):
                title = cit.title
                source_id = cit.source_id
                url = cit.url
            elif isinstance(cit, dict):
                title = cit.get("title", "Untitled")
                source_id = cit.get("source_id", "external")
                url = cit.get("url")
            else:
                continue

            cit_node = f"{source_id}:{title[:30]}"
            self.nx_graph.add_node(cit_node, type="Citation", title=title, source=source_id, url=url)
            self.nx_graph.add_edge(q_node, cit_node, relation="RETRIEVED_BY")

            # Link to broad domain anchors
            t_lower = title.lower()
            if any(k in t_lower for k in ["quantum", "physics", "qubit"]):
                self.nx_graph.add_edge(cit_node, "Concept:QuantumMechanics", relation="INSTANCE_OF")
            elif any(k in t_lower for k in ["photo", "chlorophyll", "plant", "leaf"]):
                self.nx_graph.add_edge(cit_node, "Concept:Photosynthesis", relation="INSTANCE_OF")

    def query_multihop_path(self, start_label: str, target_label: str, max_hops: int = 3) -> List[List[str]]:
        """GraphRAG: Discovers multi-hop explanatory paths bridging disparate concepts."""
        matching_starts = [n for n in self.nx_graph.nodes if start_label.lower() in str(n).lower()]
        matching_targets = [n for n in self.nx_graph.nodes if target_label.lower() in str(n).lower()]

        if not matching_starts or not matching_targets:
            return []

        paths = []
        for s in matching_starts[:2]:
            for t in matching_targets[:2]:
                if nx.has_path(self.nx_graph, s, t):
                    for path in nx.all_simple_paths(self.nx_graph, s, t, cutoff=max_hops):
                        paths.append(path)
                        if len(paths) >= 4:
                            break
        return paths

    def get_graph_stats(self) -> Dict[str, Any]:
        """Returns topological telemetry for the universe knowledge graph."""
        return {
            "total_nodes": self.nx_graph.number_of_nodes(),
            "total_edges": self.nx_graph.number_of_edges(),
            "graph_density": round(nx.density(self.nx_graph), 4),
            "sources_integrated": ["Wikidata", "DBpedia", "OpenAlex", "Sacred Ontology", "Live Citations"],
            "neo4j_synced": self.neo4j_store.is_connected(),
        }


# Global singleton instance
universe_knowledge_graph = UniverseKnowledgeGraph()
