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
        """Calculates semantic keyword and domain match scores for each candidate API using cognitive query decomposition."""
        from backend.neural_brain.query_parser import query_parser
        parsed = query_parser.parse(query)

        q_lower = query.lower()
        # Combine original tokens, core entities, and parsed intent
        q_tokens = set(q_lower.replace("?", "").replace(",", "").replace(".", "").split())
        for ent in parsed.core_entities:
            q_tokens.update(ent.lower().split())

        scores = {}

        # Domain specific indicator heuristics
        scientific_keywords = {"quantum", "physics", "algorithm", "qubit", "computer", "math", "equation", "tensor"}
        biomedical_keywords = {"disease", "cell", "cancer", "protein", "dna", "gene", "virus", "treatment", "medicine", "clinical", "brain", "neuron"}
        theological_keywords = {"quran", "hadith", "prophet", "islam", "allah", "surah", "verse", "sunnah", "prayer", "faith", "deen", "soul", "heart", "ruh", "qalb"}
        space_keywords = {"space", "astronomy", "planet", "galaxy", "cosmology", "telescope", "orbit", "universe", "star", "mars"}
        chemical_keywords = {"chemical", "compound", "molecule", "formula", "drug", "acid", "synthesis", "bonding", "reaction"}
        academic_keywords = {"citation", "paper", "journal", "author", "scholar", "study", "literature", "review"}
        historical_general = {"history", "who", "when", "what", "war", "century", "empire", "biography", "concept", "philosophy"}
        google_keywords = {"google", "news", "current", "latest", "recent", "trending", "update", "today", "discovery", "breakthrough", "world"}
        book_keywords = {"book", "author", "philosophy", "monograph", "literature", "treatise", "classic", "dialogue", "history", "ancient"}
        crossref_keywords = {"doi", "peer-reviewed", "journal", "published", "crossref", "springer", "elsevier", "ieee", "nature"}

        for api in apis_metadata:
            api_id = api["id"]
            tags = set(api.get("domain_tags", []))
            base_score = 0.2  # baseline prior

            # Token overlap with domain tags
            overlap = len(q_tokens.intersection(tags))
            base_score += overlap * 0.35

            # Cognitive Domain Affinities from parsed query
            if api_id == "arxiv" and ("physics" in parsed.epistemic_domains or any(k in q_lower for k in scientific_keywords)):
                base_score += 0.85
            elif api_id == "pubmed" and ("biomedical" in parsed.epistemic_domains or any(k in q_lower for k in biomedical_keywords)):
                base_score += 0.85
            elif api_id == "quran" and ("theological" in parsed.epistemic_domains or any(k in q_lower for k in theological_keywords)):
                base_score += 0.90
            elif api_id == "hadith" and ("theological" in parsed.epistemic_domains or any(k in q_lower for k in theological_keywords)):
                base_score += 0.85
            elif api_id == "nasa" and ("astrophysics" in parsed.epistemic_domains or any(k in q_lower for k in space_keywords)):
                base_score += 0.85
            elif api_id == "pubchem" and ("chemistry" in parsed.epistemic_domains or any(k in q_lower for k in chemical_keywords)):
                base_score += 0.85
            elif api_id == "openalex" and (any(k in q_lower for k in academic_keywords) or any(k in q_lower for k in scientific_keywords) or "academic" in parsed.epistemic_domains):
                base_score += 0.75
            elif api_id == "google" and (any(k in q_lower for k in google_keywords) or True):
                base_score += 0.55  # Google is high-utility global live feed
            elif api_id == "crossref" and (any(k in q_lower for k in crossref_keywords) or any(k in q_lower for k in academic_keywords)):
                base_score += 0.75
            elif api_id == "openlibrary" and ("humanities" in parsed.epistemic_domains or any(k in q_lower for k in book_keywords)):
                base_score += 0.70
            elif api_id == "wikipedia" and (any(k in q_lower for k in historical_general) or True):
                base_score += 0.45  # Wikipedia is versatile

            # Cap relevance in [0.05, 1.0]
            scores[api_id] = float(np.clip(base_score, 0.05, 1.0))

        return scores

    # Known cross-domain synergy pairs (negative energy reward for joint selection)
    CROSS_API_SYNERGIES = {
        ("arxiv", "nasa"): -1.2,
        ("arxiv", "openalex"): -1.0,
        ("quran", "hadith"): -1.5,
        ("pubmed", "pubchem"): -1.3,
        ("pubmed", "hadith"): -0.7,
        ("wikipedia", "openalex"): -0.6,
        ("nasa", "wikipedia"): -0.5,
        ("google", "wikipedia"): -0.8,
        ("google", "openalex"): -0.8,
        ("crossref", "openalex"): -1.2,
        ("crossref", "arxiv"): -1.0,
        ("openlibrary", "wikipedia"): -0.7,
        ("openlibrary", "quran"): -0.6,
    }

    def _get_pairwise_synergy(self, api_a: str, api_b: str) -> float:
        """Retrieves pairwise cross-API coupling reward/penalty."""
        pair = (api_a, api_b)
        rev_pair = (api_b, api_a)
        return self.CROSS_API_SYNERGIES.get(pair, self.CROSS_API_SYNERGIES.get(rev_pair, 0.0))

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
        # Linear: - w_rel * R_i + w_lat * L_i
        # Penalty: P * (1 - 2*K) * x_i  (since x_i^2 = x_i)
        for i in range(N):
            api_id = api_ids[i]
            r_i = rel_scores[api_id]
            l_i = norm_latencies[i]

            linear_term = - (self.w_rel * r_i) + (self.w_lat * l_i)
            penalty_term = self.penalty * (1.0 - 2.0 * target_k)
            Q[i, i] = linear_term + penalty_term

        # Off-diagonal entries Q_ij (i != j):
        # Cardinality Penalty: 2 * P * x_i * x_j
        # Quantum Covariance Synergy: + J_ij * x_i * x_j
        for i in range(N):
            for j in range(i + 1, N):
                synergy_coupling = self._get_pairwise_synergy(api_ids[i], api_ids[j])
                coupling_term = 2.0 * self.penalty + synergy_coupling
                Q[i, j] = coupling_term
                Q[j, i] = coupling_term

        return Q, api_ids, rel_scores

    def evaluate_cost(self, bitstring: str, Q: np.ndarray, target_k: int) -> float:
        """Evaluates cost of a binary bitstring x given QUBO matrix Q."""
        x = np.array([int(b) for b in bitstring], dtype=float)
        # x^T Q x + constant offset P * K^2
        return float(x.T @ Q @ x + self.penalty * (target_k ** 2))
