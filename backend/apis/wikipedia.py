"""Wikipedia API Client for Quantum Knowledge Weaver.
Uses Wikipedia Action API and REST summary endpoint. Free and public.
"""

import re
from typing import List
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class WikipediaClient(BaseAPIClient):
    """Fetches encyclopedic context from Wikipedia."""

    def __init__(self):
        super().__init__(
            api_id="wikipedia",
            name="Wikipedia Encyclopedia",
            domain_tags=["general", "science", "history", "biography", "technology", "philosophy"],
            base_url="https://en.wikipedia.org/w/api.php",
            avg_latency_ms=180.0,
            timeout_seconds=8.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (https://github.com/qkw; info@qkw.local)"
        }

    def _clean_html(self, raw_html: str) -> str:
        """Removes span tags and search highlight marks."""
        clean = re.sub(r"<.*?>", "", raw_html)
        return clean.replace("&quot;", '"').replace("&#039;", "'").strip()

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": limit,
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            data = resp.json()

            search_results = data.get("query", {}).get("search", [])

            for item in search_results:
                title = item.get("title", "")
                page_id = str(item.get("pageid", ""))
                snippet = self._clean_html(item.get("snippet", ""))

                # Attempt to fetch high quality intro summary
                summary_snippet = snippet
                try:
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{httpx.URL(title).path}"
                    sum_resp = await client.get(summary_url, timeout=3.0)
                    if sum_resp.status_code == 200:
                        sum_data = sum_resp.json()
                        extract = sum_data.get("extract", "")
                        if extract:
                            summary_snippet = extract
                except Exception:
                    pass  # fallback to snippet

                url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                citations.append(
                    SourceCitation(
                        source_id=f"wiki-{page_id}",
                        source_name=self.name,
                        title=title,
                        url=url,
                        snippet=summary_snippet,
                        relevance_score=0.9,
                        extra_metadata={"wordcount": item.get("wordcount", 0)},
                    )
                )

        return citations
