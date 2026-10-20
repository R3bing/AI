"""Cross-reference Layer for Quantum Knowledge Weaver.
Calculates semantic similarity between retrieved citations across different APIs,
detects corroborating facts, complementary details, and potential contradictions.
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
import structlog
from backend.orchestrator.models import SourceCitation, CrossRefConnection

logger = structlog.get_logger(__name__)


class CrossReferenceComparator:
    """Compares citations from different sources and extracts cross-reference relations."""

    def __init__(self):
        self._model = None
        self._model_loaded = False

    def _get_embedding(self, text: str) -> np.ndarray:
        """Computes text embedding using sentence-transformers if available, or TF-IDF vectorizer fallback."""
        if not self._model_loaded:
            import importlib
            import importlib.util

            if importlib.util.find_spec("sentence_transformers") is not None:
                try:
                    st_module = importlib.import_module("sentence_transformers")
                    SentenceTransformer = getattr(st_module, "SentenceTransformer")
                    self._model = SentenceTransformer("all-MiniLM-L6-v2")
                    logger.info("sentence_transformers_loaded")
                except Exception as e:
                    logger.info("sentence_transformers_load_failed", error=str(e))
                    self._model = None
            else:
                self._model = None
            self._model_loaded = True

        if self._model is not None:
            return self._model.encode(text, convert_to_numpy=True)

        # Resilient character & word n-gram frequency fallback embedding
        return self._fallback_sparse_embedding(text)

    def _fallback_sparse_embedding(self, text: str, dim: int = 256) -> np.ndarray:
        """Deterministic hashing vectorizer for zero-dependency semantic fallback."""
        import zlib

        words = text.lower().replace("\n", " ").split()
        vec = np.zeros(dim, dtype=float)
        if not words:
            return vec

        for word in words:
            h = zlib.crc32(word.encode("utf-8")) % dim
            vec[h] += 1.0

        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def _cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    def _detect_contradiction_heuristic(self, text_a: str, text_b: str) -> Tuple[bool, str]:
        """Simple heuristic for detecting contrasting claims or negation."""
        negation_pairs = [
            ("increase", "decrease"),
            ("positive", "negative"),
            ("effective", "ineffective"),
            ("true", "false"),
            ("proven", "disproven"),
            ("benefit", "harm"),
            ("cure", "incurable"),
            ("permitted", "prohibited"),
        ]
        text_a_lower = text_a.lower()
        text_b_lower = text_b.lower()

        for term1, term2 in negation_pairs:
            if (term1 in text_a_lower and term2 in text_b_lower) or (term2 in text_a_lower and term1 in text_b_lower):
                return True, f"Opposing sentiments detected around '{term1}' vs '{term2}'"

        return False, ""

    def compare_citations(self, citations: List[SourceCitation]) -> List[CrossRefConnection]:
        """Cross-references citations originating from distinct API sources."""
        connections: List[CrossRefConnection] = []
        if len(citations) < 2:
            return connections

        # Compute embeddings for all snippets
        embeddings = [self._get_embedding(c.title + ". " + c.snippet) for c in citations]

        # Pairwise comparison across different source categories
        for i in range(len(citations)):
            for j in range(i + 1, len(citations)):
                cit_a = citations[i]
                cit_b = citations[j]

                # Focus cross-referencing between DIFFERENT APIs
                if cit_a.source_name == cit_b.source_name:
                    continue

                sim = self._cosine_similarity(embeddings[i], embeddings[j])
                is_contradiction, contra_reason = self._detect_contradiction_heuristic(cit_a.snippet, cit_b.snippet)

                if is_contradiction:
                    rel_type = "contradicts"
                    notes = contra_reason
                elif sim >= 0.70:
                    rel_type = "corroborates"
                    notes = f"Strong semantic alignment ({sim:.2f}) across independent databases."
                elif sim >= 0.35:
                    rel_type = "complements"
                    notes = f"Provides complementary context ({sim:.2f}) from different domain perspectives."
                else:
                    continue

                connections.append(
                    CrossRefConnection(
                        source_a_id=cit_a.source_id,
                        source_a_name=f"{cit_a.source_name}: {cit_a.title}",
                        source_b_id=cit_b.source_id,
                        source_b_name=f"{cit_b.source_name}: {cit_b.title}",
                        similarity_score=round(float(sim), 3),
                        relationship=rel_type,
                        notes=notes,
                    )
                )

        # Sort highest similarity first
        connections.sort(key=lambda c: c.similarity_score, reverse=True)
        return connections


# Global instance
cross_referencer = CrossReferenceComparator()
