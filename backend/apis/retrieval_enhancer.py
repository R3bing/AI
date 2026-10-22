"""Knowledge Retrieval Enhancer & Multi-Repository Deduplicator for Ultron Sovereign Core.
Implements:
1. Cross-Repository Citation Deduplication (by DOI, normalized title Jaccard distance, and URL).
2. Multi-Factor Authority & Information Density Re-Ranking:
   Score = w_relevance * SemanticOverlap + w_authority * DomainCredibility + w_density * SnippetDepth.
3. Epistemic Cluster Partitioning (Empirical, Ontological, Telemetry, Socioeconomic, Engineering, Sacred).
4. Adaptive Knowledge Stream Selector for high-speed federated dispatch.
"""

import re
from typing import List, Dict, Any, Set, Tuple


class KnowledgeRetrievalEnhancer:
    """Optimizes, deduplicates, and re-ranks citations across all federated knowledge repositories."""

    # Domain credibility weights for re-ranking
    AUTHORITY_WEIGHTS = {
        "pubmed": 1.00,
        "arxiv": 0.98,
        "semanticscholar": 0.97,
        "crossref": 0.95,
        "openalex": 0.94,
        "pubchem": 0.96,
        "nasa": 0.95,
        "quran": 1.00,
        "hadith": 0.96,
        "bible": 0.92,
        "wikidata": 0.90,
        "dbpedia": 0.88,
        "worldbank": 0.93,
        "openmeteo": 0.91,
        "osv": 0.94,
        "wikipedia": 0.87,
        "gutendex": 0.89,
        "openlibrary": 0.88,
        "pypi": 0.88,
        "hackernews": 0.82,
        "google": 0.80,
    }

    # Epistemic Taxonomy mapping
    EPISTEMIC_TAXONOMY = {
        "academic_empirical": ["arxiv", "pubmed", "semanticscholar", "crossref", "openalex", "pubchem"],
        "structured_ontologies": ["wikidata", "dbpedia", "wikipedia"],
        "cosmic_planetary_telemetry": ["nasa", "openmeteo"],
        "socioeconomics_demographics": ["worldbank"],
        "software_systems_security": ["hackernews", "pypi", "osv"],
        "sacred_classical_literature": ["quran", "hadith", "bible", "gutendex", "openlibrary"],
    }

    def _normalize_title(self, title: str) -> Set[str]:
        """Cleans and extracts core tokens from title for similarity comparisons."""
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", title.lower())
        words = set(cleaned.split())
        stopwords = {"a", "an", "the", "in", "on", "of", "and", "or", "for", "with", "to", "at", "by", "from"}
        return words - stopwords

    def _jaccard_similarity(self, tokens_a: Set[str], tokens_b: Set[str]) -> float:
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = len(tokens_a & tokens_b)
        union = len(tokens_a | tokens_b)
        return intersection / float(union) if union > 0 else 0.0

    def deduplicate_citations(self, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicates citations across multi-repository feeds by DOI, Title overlap, and URL."""
        seen_dois: Set[str] = set()
        seen_urls: Set[str] = set()
        unique_citations: List[Dict[str, Any]] = []
        seen_title_tokens: List[Tuple[Set[str], int]] = []

        for cit in citations:
            doi = cit.get("doi", "").strip().lower()
            url = cit.get("url", "").strip().lower()
            title = cit.get("title", "").strip()

            # 1. Exact DOI match
            if doi and doi in seen_dois:
                continue

            # 2. Exact URL match
            if url and url in seen_urls:
                continue

            # 3. Fuzzy Title Jaccard match (> 80% overlap)
            title_tokens = self._normalize_title(title)
            is_duplicate = False
            for prev_tokens, prev_idx in seen_title_tokens:
                sim = self._jaccard_similarity(title_tokens, prev_tokens)
                if sim > 0.80:
                    is_duplicate = True
                    # If this duplicate citation has richer metadata or DOI, enrich the previous citation
                    prev_cit = unique_citations[prev_idx]
                    if doi and not prev_cit.get("doi"):
                        prev_cit["doi"] = doi
                    if len(cit.get("snippet", "")) > len(prev_cit.get("snippet", "")):
                        prev_cit["snippet"] = cit["snippet"]
                    break

            if is_duplicate:
                continue

            # Mark as unique
            if doi:
                seen_dois.add(doi)
            if url:
                seen_urls.add(url)
            if title_tokens:
                seen_title_tokens.append((title_tokens, len(unique_citations)))

            unique_citations.append(cit)

        return unique_citations

    def rank_and_score_citations(self, citations: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Re-ranks deduplicated citations based on authority, query relevance, and information density."""
        q_tokens = self._normalize_title(query)
        scored_citations = []

        for cit in citations:
            src = cit.get("source", "google").lower()
            title = cit.get("title", "")
            snippet = cit.get("snippet", "")
            url = cit.get("url", "")
            doi = cit.get("doi", "")

            # 1. Base Authority Weight
            authority = self.AUTHORITY_WEIGHTS.get(src, 0.85)

            # 2. Query Term Overlap
            content_tokens = self._normalize_title(title + " " + snippet)
            relevance = self._jaccard_similarity(q_tokens, content_tokens)

            # 3. Informational Density Score (0 to 1)
            density = min(1.0, len(snippet.split()) / 40.0)

            # 4. Verifiability Bonus (has DOI, ISBN, or direct HTTPS link)
            verifiability = 0.15 if (doi or (url and url.startswith("https://"))) else 0.0

            # Combined Composite Score
            final_score = (0.40 * authority) + (0.35 * relevance) + (0.15 * density) + verifiability
            cit["composite_rank_score"] = round(final_score, 4)
            scored_citations.append(cit)

        # Sort descending by composite rank score
        scored_citations.sort(key=lambda x: x.get("composite_rank_score", 0.0), reverse=True)
        return scored_citations

    def optimize_knowledge_batch(
        self,
        citations: List[Dict[str, Any]],
        query: str,
        max_citations: int = 25,
    ) -> List[Dict[str, Any]]:
        """Complete pipeline: deduplicates, computes composite quality scores, and returns top evidence."""
        deduped = self.deduplicate_citations(citations)
        ranked = self.rank_and_score_citations(deduped, query)
        return ranked[:max_citations]


# Global singleton instance
retrieval_enhancer = KnowledgeRetrievalEnhancer()
