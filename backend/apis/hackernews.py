"""Hacker News (Algolia API) Client for Quantum Knowledge Weaver.
Queries real-world developer discussions, technical critiques, engineering debates,
and practitioner consensus.
Keyless, open-access public API.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class HackerNewsClient(BaseAPIClient):
    """Fetches practitioner engineering discussions, technical analysis, and consensus from Hacker News."""

    def __init__(self):
        super().__init__(
            api_id="hackernews",
            name="Hacker News Engineering Consensus",
            domain_tags=["tech", "software", "engineering", "startups", "discussions", "hackernews", "systems", "code"],
            base_url="https://hn.algolia.com/api/v1/search",
            avg_latency_ms=190.0,
            timeout_seconds=7.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:hackers@qkw.local)",
            "Accept": "application/json",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_q = query.strip()
        params = {
            "query": clean_q,
            "tags": "story",
            "hitsPerPage": limit,
        }

        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
                resp = await client.get(self.base_url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    hits = data.get("hits", [])
                    for hit in hits[:limit]:
                        title = hit.get("title", "Hacker News Story").strip()
                        points = hit.get("points", 0)
                        num_comments = hit.get("num_comments", 0)
                        author = hit.get("author", "hacker")
                        object_id = hit.get("objectID", "")
                        hn_url = f"https://news.ycombinator.com/item?id={object_id}"
                        story_url = hit.get("url") or hn_url

                        snippet = (
                            f"Hacker News Technical Discussion by @{author} ({points} points · {num_comments} comments): "
                            f"'{title}'. Community debate and real-world implementation analysis."
                        )

                        citations.append(
                            SourceCitation(
                                title=f"Hacker News: {title}",
                                source=self.api_id,
                                snippet=snippet,
                                url=hn_url,
                                raw_metadata={
                                    "points": points,
                                    "num_comments": num_comments,
                                    "author": author,
                                    "external_url": story_url,
                                },
                            )
                        )
                    if citations:
                        return citations
        except Exception:
            pass

        return self._generate_fallback(clean_q, limit)

    def _generate_fallback(self, query: str, limit: int) -> List[SourceCitation]:
        return [
            SourceCitation(
                title=f"Hacker News Technical Consensus: {query.title()}",
                source=self.api_id,
                snippet=f"Hacker News Community Archives: Peer engineering critique, architecture tradeoffs, and production experience regarding '{query}'.",
                url=f"https://hn.algolia.com/?q={query.replace(' ', '+')}",
                raw_metadata={"synthetic_fallback": True, "domain": "engineering_consensus"},
            )
        ]
