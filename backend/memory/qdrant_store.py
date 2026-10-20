"""Vector Memory module for Quantum Knowledge Weaver using Qdrant.
Stores past query vectors, responses, and citations. Enables semantic query caching.
Supports both embedded in-memory mode (:memory:) and remote Qdrant server.
"""

import time
import uuid
from typing import Optional, Dict, Any, List
import numpy as np
import structlog
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from backend.config import settings

logger = structlog.get_logger(__name__)


class QdrantVectorMemory:
    """Vector database manager for semantic retrieval and caching in QKW."""

    def __init__(self, vector_dim: int = 256):
        self.vector_dim = vector_dim
        self.collection_name = settings.qdrant_collection
        self.client: Optional[QdrantClient] = None
        self._init_client()

    def _init_client(self):
        try:
            if settings.qdrant_url:
                self.client = QdrantClient(url=settings.qdrant_url)
                logger.info("qdrant_connected_remote", url=settings.qdrant_url)
            else:
                # In-memory storage: zero setup, blazingly fast
                self.client = QdrantClient(location=":memory:")
                logger.info("qdrant_initialized_in_memory")

            # Check or create collection
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.vector_dim,
                        distance=qmodels.Distance.COSINE,
                    ),
                )
                logger.info("qdrant_collection_created", collection=self.collection_name)
        except Exception as e:
            logger.warning("qdrant_init_fallback_to_memory", error=str(e))
            self.client = QdrantClient(location=":memory:")

    def cache_query(
        self,
        query: str,
        embedding: np.ndarray,
        response_data: Dict[str, Any],
    ) -> bool:
        """Stores a resolved query response and embedding for rapid retrieval."""
        if not self.client:
            return False

        try:
            # Pad or truncate embedding to vector_dim
            vec = np.zeros(self.vector_dim, dtype=float)
            vec[: min(len(embedding), self.vector_dim)] = embedding[: self.vector_dim]

            point_id = str(uuid.uuid4())
            payload = {
                "query": query,
                "timestamp": time.time(),
                "response": response_data,
            }

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    qmodels.PointStruct(
                        id=point_id,
                        vector=vec.tolist(),
                        payload=payload,
                    )
                ],
            )
            return True
        except Exception as e:
            logger.error("qdrant_cache_upsert_failed", error=str(e))
            return False

    def lookup_cache(
        self,
        embedding: np.ndarray,
        threshold: float = 0.93,
    ) -> Optional[Dict[str, Any]]:
        """Finds if a semantically equivalent query was recently answered."""
        if not self.client:
            return None

        try:
            vec = np.zeros(self.vector_dim, dtype=float)
            vec[: min(len(embedding), self.vector_dim)] = embedding[: self.vector_dim]

            # Modern qdrant-client uses query_points, legacy uses search
            if hasattr(self.client, "query_points"):
                search_res = self.client.query_points(
                    collection_name=self.collection_name,
                    query=vec.tolist(),
                    limit=1,
                )
                points = search_res.points
                if points and points[0].score >= threshold:
                    logger.info("qdrant_cache_hit", score=points[0].score)
                    return points[0].payload.get("response")
            elif hasattr(self.client, "search"):
                search_result = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=vec.tolist(),
                    limit=1,
                )
                if search_result and search_result[0].score >= threshold:
                    logger.info("qdrant_cache_hit", score=search_result[0].score)
                    return search_result[0].payload.get("response")

            return None
        except Exception as e:
            logger.warning("qdrant_lookup_failed", error=str(e))
            return None


# Global instance
vector_memory = QdrantVectorMemory()
