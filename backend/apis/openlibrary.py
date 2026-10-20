"""Open Library (Internet Archive) API Client for Quantum Knowledge Weaver.
Queries the global public catalog of 20M+ digitized books, historical philosophy,
scientific treatises, and literature.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class OpenLibraryClient(BaseAPIClient):
    """Fetches digitized books, historical literature, and philosophical treatises from Open Library."""

    def __init__(self):
        super().__init__(
            api_id="openlibrary",
            name="Open Library World Literature",
            domain_tags=["books", "literature", "philosophy", "history", "library", "monographs", "treatises"],
            base_url="https://openlibrary.org/search.json",
            avg_latency_ms=310.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:archive@qkw.local)",
            "Accept": "application/json",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        params = {
            "q": query.strip(),
            "limit": limit,
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            data = resp.json()

            docs = data.get("docs", [])
            for doc in docs[:limit]:
                title = doc.get("title", "Untitled Volume")
                authors = doc.get("author_name", [])
                author_str = ", ".join(authors[:3]) if authors else "Unknown Author"
                year = doc.get("first_publish_year", "")
                key = doc.get("key", "")
                url = f"https://openlibrary.org{key}" if key else None

                first_sentence = doc.get("first_sentence", [])
                first_sent_text = first_sentence[0] if isinstance(first_sentence, list) and first_sentence else ""

                snippet = f"Literary work by {author_str}"
                if year:
                    snippet += f" (first published {year})"
                snippet += f": '{title}'."
                if first_sent_text:
                    snippet += f" Opening: \"{first_sent_text[:120]}...\""

                citations.append(
                    SourceCitation(
                        source_id="openlibrary",
                        source_name="Open Library Books",
                        title=title,
                        url=url,
                        snippet=snippet,
                        relevance_score=0.82,
                        extra_metadata={
                            "authors": author_str,
                            "first_publish_year": year,
                            "key": key,
                        },
                    )
                )

        return citations
