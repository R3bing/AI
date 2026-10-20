"""NASA Open Science & Image API Client for Quantum Knowledge Weaver.
Queries the NASA Open Data repository (images-api.nasa.gov) for astrophysics, astronomy, and planetary science.
"""

from typing import List
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class NasaClient(BaseAPIClient):
    """Fetches astronomy, astrophysics, space exploration, and cosmology records from NASA."""

    def __init__(self):
        super().__init__(
            api_id="nasa",
            name="NASA Astrophysics & Space Science",
            domain_tags=["astronomy", "astrophysics", "space", "cosmology", "planets", "physics", "nasa", "universe"],
            base_url="https://images-api.nasa.gov/search",
            avg_latency_ms=320.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (https://github.com/qkw)"
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        params = {
            "q": query.strip(),
            "media_type": "image",
            "page_size": limit,
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("collection", {}).get("items", [])
            for item in items[:limit]:
                data_list = item.get("data", [])
                if not data_list:
                    continue

                rec = data_list[0]
                nasa_id = rec.get("nasa_id", "nasa-item")
                title = rec.get("title", "NASA Discovery")
                description = rec.get("description", "")
                date_created = rec.get("date_created", "")[:10]
                center = rec.get("center", "NASA")

                # Truncate clean snippet
                clean_snippet = " ".join(description.split())
                if len(clean_snippet) > 400:
                    clean_snippet = clean_snippet[:397] + "..."

                url = f"https://images.nasa.gov/details/{nasa_id}"

                citations.append(
                    SourceCitation(
                        source_id=f"nasa-{nasa_id}",
                        source_name=self.name,
                        title=f"{title} ({center})",
                        url=url,
                        snippet=clean_snippet if clean_snippet else f"NASA observation recorded at {center}.",
                        relevance_score=0.92,
                        extra_metadata={
                            "nasa_id": nasa_id,
                            "center": center,
                            "date_created": date_created,
                        },
                    )
                )

        return citations
