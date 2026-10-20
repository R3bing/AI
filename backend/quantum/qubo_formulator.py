"""QUBO (Quadratic Unconstrained Binary Optimization) Formulator for API Routing.
Maps query intent, semantic relevance, latency penalties, and budget constraints into a Hamiltonian.
"""

from typing import List, Dict, Tuple
import numpy as np


class QUBOFormulator:
    """Formulates the API selection problem as a QUBO / Ising Hamiltonian.

    Binary decision variable: x_i in {0, 1} indicates whether API_i is selected.
    Objective:
      Minimize: Cost(x) = - w_rel * sum(Relevance_i * x_i)
                          + w_lat * sum(Latency_i * x_i)
                          + penalty * (sum(x_i) - K)^2
    """

    def __init__(
        self,
        relevance_weight: float = 2.5,
        latency_weight: float = 0.8,
        cardinality_penalty: float = 2.0,
    ):
        self.w_rel = relevance_weight
        self.w_lat = latency_weight
        self.penalty = cardinality_penalty

    def compute_relevance_scores(self, query: str, apis_metadata: List[Dict]) -> Dict[str, float]:
        """Calculates semantic keyword and domain match scores for each candidate API."""
        q_lower = query.lower()
        q_tokens = set(q_lower.replace("?", "").replace(",", "").replace(".", "").split())
        scores = {}

        # Domain specific indicator heuristics
        scientific_keywords = {"quantum", "physics", "algorithm", "qubit", "computer", "math", "equation", "tensor"}
        biomedical_keywords = {"disease", "cell", "cancer", "protein", "dna", "gene", "virus", "treatment", "medicine", "clinical"}
        theological_keywords = {"quran", "hadith", "prophet", "islam", "allah", "surah", "verse", "sunnah", "prayer", "faith", "deen"}
        historical_general = {"history", "who", "when", "what", "war", "century", "empire", "biography", "concept", "philosophy"}

        for api in apis_metadata:
            api_id = api["id"]
            tags = set(api.get("domain_tags", []))
            base_score = 0.2  # baseline prior

            # Token overlap with domain tags
            overlap = len(q_tokens.intersection(tags))
            base_score += overlap * 0.4

            # Domain specific triggers
            if api_id == "arxiv" and any(k in q_lower for k in scientific_keywords):
                base_score += 0.8
            elif api_id == "pubmed" and any(k in q_lower for k in biomedical_keywords):
                base_score += 0.8
            elif api_id == "quran" and any(k in q_lower for k in theological_keywords):
                base_score += 0.85
            elif api_id == "hadith" and any(k in q_lower for k in theological_keywords):
                base_score += 0.80
            elif api_id == "wikipedia" and (any(k in q_lower for k in historical_general) or True):
                base_score += 0.45  # Wikipedia is versatile

            # Cap relevance in [0.05, 1.0]
            scores[api_id] = float(np.clip(base_score, 0.05, 1.0))

        return scores

    def build_qubo_matrix(
        self,
        query: str,
        apis_metadata: List[Dict],
        target_k: int = 3,
    ) -> Tuple[np.ndarray, List[str], Dict[str, float]]:
        """Constructs the QUBO matrix Q such that Cost(x) = x^T Q x.

        Returns:
            Q (np.ndarray): Symmetric NxN QUBO coefficient matrix.
            api_ids (List[str]): List of API IDs corresponding to matrix rows/cols.
            relevance_dict (Dict[str, float]): Computed relevance scores.
        """
        api_ids = [api["id"] for api in apis_metadata]
        N = len(api_ids)
        rel_scores = self.compute_relevance_scores(query, apis_metadata)

        # Normalize latencies to [0, 1]
        latencies = [api.get("avg_latency_ms", 300.0) for api in apis_metadata]
        max_lat = max(latencies) if max(latencies) > 0 else 1.0
        norm_latencies = [lat / max_lat for lat in latencies]

        # Initialize NxN matrix
        Q = np.zeros((N, N))

        # Diagonal entries Q_ii:
        # From objective: - w_rel * R_i + w_lat * L_i
        # From penalty: P * (1 - 2*K) * x_i  (since x_i^2 = x_i)
        for i in range(N):
            api_id = api_ids[i]
            r_i = rel_scores[api_id]
            l_i = norm_latencies[i]

            linear_term = - (self.w_rel * r_i) + (self.w_lat * l_i)
            penalty_term = self.penalty * (1.0 - 2.0 * target_k)
            Q[i, i] = linear_term + penalty_term

        # Off-diagonal entries Q_ij (i != j):
        # From penalty: 2 * P * x_i * x_j
        for i in range(N):
            for j in range(i + 1, N):
                Q[i, j] = 2.0 * self.penalty
                Q[j, i] = 2.0 * self.penalty

        return Q, api_ids, rel_scores

    def evaluate_cost(self, bitstring: str, Q: np.ndarray, target_k: int) -> float:
        """Evaluates cost of a binary bitstring x given QUBO matrix Q."""
        x = np.array([int(b) for b in bitstring], dtype=float)
        # x^T Q x + constant offset P * K^2
        return float(x.T @ Q @ x + self.penalty * (target_k ** 2))
