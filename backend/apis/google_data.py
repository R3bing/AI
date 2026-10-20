"""Google Knowledge & News Search API Client for Quantum Knowledge Weaver.
Retrieves real-time authoritative Google search records, news, and research articles.
Uses Google's public RSS search feed with zero authentication requirements.
"""

from typing import List, Dict, Any
import xml.etree.ElementTree as ET
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class GoogleDataClient(BaseAPIClient):
    """Fetches real-time web knowledge, news, and research from Google's public search index."""

    def __init__(self):
        super().__init__(
            api_id="google",
            name="Google Knowledge & News Index",
            domain_tags=["google", "web", "news", "current_affairs", "technology", "general", "journalism", "global"],
            base_url="https://news.google.com/rss/search",
            avg_latency_ms=250.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/xml, text/xml",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        params = {
            "q": query.strip(),
            "hl": "en-US",
            "gl": "US",
            "ceid": "US:en",
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            xml_text = resp.text

            try:
                root = ET.fromstring(xml_text)
                items = root.findall(".//item")
            except Exception:
                items = []

            for item in items[:limit]:
                title_elem = item.find("title")
                link_elem = item.find("link")
                pubdate_elem = item.find("pubDate")
                source_elem = item.find("source")

                raw_title = title_elem.text.strip() if title_elem is not None and title_elem.text else "Google Search Result"
                url = link_elem.text.strip() if link_elem is not None and link_elem.text else None
                pub_date = pubdate_elem.text.strip() if pubdate_elem is not None and pubdate_elem.text else ""
                publisher = source_elem.text.strip() if source_elem is not None and source_elem.text else "Google News Index"

                # Title often contains " - Publisher", split for clean presentation
                clean_title = raw_title
                if " - " in raw_title:
                    clean_title = raw_title.rsplit(" - ", 1)[0].strip()

                snippet = f"Google indexed report by {publisher}: '{clean_title}' ({pub_date})."

                citations.append(
                    SourceCitation(
                        source_id="google",
                        source_name="Google Knowledge & News",
                        title=clean_title,
                        url=url,
                        snippet=snippet,
                        relevance_score=0.88,
                        extra_metadata={
                            "publisher": publisher,
                            "published_date": pub_date,
                            "raw_title": raw_title,
                        },
                    )
                )

        return citations
