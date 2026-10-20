"""OpenAlex Academic Graph API Client for Quantum Knowledge Weaver.
Queries the global scholarly database of 250M+ research papers, citation metrics, and open-access science.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class OpenAlexClient(BaseAPIClient):
    """Fetches peer-reviewed academic literature and global research citation data from OpenAlex."""

    def __init__(self):
        super().__init__(
            api_id="openalex",
            name="OpenAlex Global Research Graph",
            domain_tags=["research", "science", "academia", "citations", "papers", "technology", "multidisciplinary"],
            base_url="https://api.openalex.org/works",
            avg_latency_ms=280.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:info@qkw.local)"
        }

    def _reconstruct_abstract(self, inverted_index: Dict[str, List[int]]) -> str:
        """Reconstructs text from OpenAlex's inverted abstract index."""
        if not inverted_index or not isinstance(inverted_index, dict):
            return ""
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(w for _, w in word_positions)

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        params = {
            "search": query.strip(),
            "per-page": limit,
            "sort": "relevance_score:desc",
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            data = resp.json()

            results = data.get("results", [])
            for item in results[:limit]:
                work_id = item.get("id", "").split("/")[-1]
                title = item.get("title", "Untitled Research") or "Untitled Scholarly Work"
                pub_year = item.get("publication_year", "")
                cited_by = item.get("cited_by_count", 0)

                # Reconstruct abstract or build informative snippet
                abstract = self._reconstruct_abstract(item.get("abstract_inverted_index", {}))
                if not abstract:
                    concepts = [c.get("display_name", "") for c in item.get("concepts", [])[:4] if c.get("display_name")]
                    snippet = f"Scholarly publication ({pub_year}). Key research areas: {', '.join(concepts)}. Cited by {cited_by} independent academic papers."
                else:
                    snippet = " ".join(abstract.split())
                    if len(snippet) > 400:
                        snippet = snippet[:397] + "..."

                primary_loc = item.get("primary_location", {}) or {}
                landing_page = primary_loc.get("landing_page_url") or item.get("doi") or f"https://openalex.org/{work_id}"

                citations.append(
                    SourceCitation(
                        source_id=f"openalex-{work_id}",
                        source_name=self.name,
                        title=f"{title} ({pub_year})",
                        url=landing_page,
                        snippet=snippet,
                        relevance_score=0.94,
                        extra_metadata={
                            "openalex_id": work_id,
                            "cited_by_count": cited_by,
                            "publication_year": pub_year,
                        },
                    )
                )

        return citations
