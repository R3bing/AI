"""Crossref DOI & Academic Papers API Client for Quantum Knowledge Weaver.
Queries the global citation registry of 150M+ peer-reviewed journal papers and DOIs.
Keyless, open-access public API.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class CrossrefClient(BaseAPIClient):
    """Fetches peer-reviewed journal articles and multi-publisher DOI citations from Crossref."""

    def __init__(self):
        super().__init__(
            api_id="crossref",
            name="Crossref Academic Papers & DOIs",
            domain_tags=["crossref", "academic", "papers", "journals", "doi", "peer_reviewed", "science", "scholarship"],
            base_url="https://api.crossref.org/works",
            avg_latency_ms=290.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:scholar@qkw.local)",
            "Accept": "application/json",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        params = {
            "query": query.strip(),
            "rows": limit,
            "sort": "relevance",
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("message", {}).get("items", [])
            for item in items[:limit]:
                # Title
                raw_title_list = item.get("title", [])
                title = raw_title_list[0].strip() if raw_title_list else "Untitled Crossref Work"

                # DOI & URL
                doi = item.get("DOI", "")
                url = f"https://doi.org/{doi}" if doi else item.get("URL")

                # Publisher & Authors
                publisher = item.get("publisher", "Academic Publisher")
                authors = []
                for a in item.get("author", [])[:3]:
                    family = a.get("family", "")
                    given = a.get("given", "")
                    if family:
                        authors.append(f"{given} {family}".strip())
                author_str = ", ".join(authors) if authors else "Scholarly Research Team"

                # Date
                date_parts = item.get("published", {}).get("date-parts", [[]])[0]
                pub_year = str(date_parts[0]) if date_parts else ""

                # Construct scholarly snippet
                snippet = f"Peer-reviewed paper published by {publisher}"
                if pub_year:
                    snippet += f" ({pub_year})"
                snippet += f" by {author_str}: '{title}'."

                citations.append(
                    SourceCitation(
                        source_id="crossref",
                        source_name="Crossref Academic DOI",
                        title=title,
                        url=url,
                        snippet=snippet,
                        relevance_score=0.85,
                        extra_metadata={
                            "doi": doi,
                            "publisher": publisher,
                            "authors": author_str,
                            "year": pub_year,
                        },
                    )
                )

        return citations
