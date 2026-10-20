"""Quran API Client for Quantum Knowledge Weaver.
Queries the Quranic corpus using public, verified translation endpoints (Al-Quran Cloud & Quran.com).
"""

from typing import List
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class QuranClient(BaseAPIClient):
    """Fetches authentic Quranic verses, English translations (Saheeh International), and surah context."""

    def __init__(self):
        super().__init__(
            api_id="quran",
            name="The Holy Quran Corpus",
            domain_tags=["religion", "theology", "ethics", "islamic_studies", "philosophy", "law"],
            base_url="https://api.alquran.cloud/v1/search",
            avg_latency_ms=220.0,
            timeout_seconds=8.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (https://github.com/qkw)"
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_query = query.strip()
        # Primary search via Al-Quran Cloud Sahih International English translation
        primary_url = f"{self.base_url}/{clean_query}/all/en.sahih"

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            try:
                resp = await client.get(primary_url)
                if resp.status_code == 200:
                    data = resp.json()
                    matches = data.get("data", {}).get("matches", [])
                    for match in matches[:limit]:
                        surah_info = match.get("surah", {})
                        surah_name = surah_info.get("englishName", "Surah")
                        surah_num = surah_info.get("number", 0)
                        ayah_num = match.get("numberInSurah", 0)
                        verse_text = match.get("text", "").strip()

                        title = f"Surah {surah_name} ({surah_num}:{ayah_num})"
                        url = f"https://quran.com/{surah_num}/{ayah_num}"

                        citations.append(
                            SourceCitation(
                                source_id=f"quran-{surah_num}-{ayah_num}",
                                source_name=self.name,
                                title=title,
                                url=url,
                                snippet=verse_text,
                                relevance_score=0.92,
                                extra_metadata={
                                    "surah_number": surah_num,
                                    "ayah_number": ayah_num,
                                    "surah_translation": surah_info.get("englishNameTranslation", ""),
                                },
                            )
                        )
            except Exception:
                pass

            # Fallback to Quran.com API v4 if no matches from Al-Quran Cloud
            if not citations:
                try:
                    fallback_url = "https://api.quran.com/api/v4/search"
                    fb_resp = await client.get(fallback_url, params={"q": clean_query, "size": limit})
                    if fb_resp.status_code == 200:
                        fb_data = fb_resp.json()
                        results = fb_data.get("search", {}).get("results", [])
                        for res in results[:limit]:
                            verse_key = res.get("verse_key", "")
                            text = res.get("text", "")
                            title = f"Surah Ayah {verse_key}"
                            url = f"https://quran.com/{verse_key.replace(':', '/')}"
                            citations.append(
                                SourceCitation(
                                    source_id=f"quran-{verse_key}",
                                    source_name=self.name,
                                    title=title,
                                    url=url,
                                    snippet=text,
                                    relevance_score=0.88,
                                )
                            )
                except Exception:
                    pass

        return citations
