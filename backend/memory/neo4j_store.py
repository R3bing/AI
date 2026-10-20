"""Knowledge Graph Memory module for Quantum Knowledge Weaver.
Stores entities, concepts, and relationships in Neo4j, with an in-memory graph fallback.
"""

from typing import List, Dict, Any, Optional, Set
import structlog
from neo4j import GraphDatabase
from backend.config import settings
from backend.orchestrator.models import SourceCitation, CrossRefConnection

logger = structlog.get_logger(__name__)


class KnowledgeGraphMemory:
    """Manages entity-relation knowledge graph in Neo4j with resilient local fallback."""

    def __init__(self):
        self.driver = None
        self._connected = False
        # In-memory graph fallback: { "nodes": [...], "edges": [...] }
        self._local_nodes: Dict[str, Dict[str, Any]] = {}
        self._local_edges: List[Dict[str, Any]] = []
        self._init_connection()

    def _init_connection(self):
        try:
            if settings.neo4j_uri:
                self.driver = GraphDatabase.driver(
                    settings.neo4j_uri,
                    auth=(settings.neo4j_user, settings.neo4j_password),
                    connection_timeout=2.0,
                )
                # Verify connectivity
                with self.driver.session() as session:
                    session.run("RETURN 1 AS test")
                self._connected = True
                logger.info("neo4j_connected_successfully", uri=settings.neo4j_uri)
        except Exception as e:
            logger.info("neo4j_server_offline_using_in_memory_graph", error=str(e))
            self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def _extract_simple_entities(self, text: str) -> List[str]:
        """Simple rule-based entity / capitalized terms extractor."""
        import re
        words = re.findall(r"\b[A-Z][a-zA-Z0-9_\-]{2,}\b", text)
        stopwords = {"The", "And", "For", "With", "This", "That", "From", "What", "When", "Where", "How"}
        entities = list(set(w for w in words if w not in stopwords))
        return entities[:8]

    def store_knowledge_triples(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
    ):
        """Stores Query -> Citations -> Entities in the graph."""
        query_node_id = f"Query:{query[:30]}"
        self._local_nodes[query_node_id] = {"id": query_node_id, "label": "Query", "name": query}

        # Add citation nodes and link from Query
        for cit in citations:
            cit_node_id = f"Source:{cit.source_id}"
            self._local_nodes[cit_node_id] = {
                "id": cit_node_id,
                "label": "Source",
                "name": cit.title,
                "source_name": cit.source_name,
                "url": cit.url,
            }
            self._local_edges.append({
                "source": query_node_id,
                "target": cit_node_id,
                "relationship": "RETRIEVED",
            })

            # Extract concepts
            entities = self._extract_simple_entities(cit.snippet)
            for ent in entities:
                ent_node_id = f"Concept:{ent}"
                if ent_node_id not in self._local_nodes:
                    self._local_nodes[ent_node_id] = {"id": ent_node_id, "label": "Concept", "name": ent}
                self._local_edges.append({
                    "source": cit_node_id,
                    "target": ent_node_id,
                    "relationship": "MENTIONS",
                })

        # Add cross reference edges
        for cr in cross_references:
            id_a = f"Source:{cr.source_a_id}"
            id_b = f"Source:{cr.source_b_id}"
            if id_a in self._local_nodes and id_b in self._local_nodes:
                self._local_edges.append({
                    "source": id_a,
                    "target": id_b,
                    "relationship": cr.relationship.upper(),
                    "score": cr.similarity_score,
                })

        # If connected to remote Neo4j, execute Cypher queries
        if self._connected and self.driver:
            try:
                with self.driver.session() as session:
                    session.run("MERGE (q:Query {name: $query})", query=query)
                    for cit in citations:
                        session.run(
                            """
                            MERGE (s:Source {id: $cit_id})
                            ON CREATE SET s.title = $title, s.api = $api
                            MERGE (q:Query {name: $query})
                            MERGE (q)-[:RETRIEVED]->(s)
                            """,
                            cit_id=cit.source_id,
                            title=cit.title,
                            api=cit.source_name,
                            query=query,
                        )
            except Exception as e:
                logger.warning("neo4j_cypher_sync_error", error=str(e))

    def get_graph_data(self) -> Dict[str, Any]:
        """Returns node and edge dictionary for visualization."""
        return {
            "nodes": list(self._local_nodes.values()),
            "edges": self._local_edges,
            "connected_to_neo4j": self._connected,
        }


# Global instance
graph_memory = KnowledgeGraphMemory()
