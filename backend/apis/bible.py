"""Bible API Comparative Scripture Client for Quantum Knowledge Weaver.
Queries the biblical scriptures, historical wisdom literature, Proverbs, Psalms,
and classical moral traditions for comparative spiritual ethics.
Keyless, open-access public API.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class BibleClient(BaseAPIClient):
    """Fetches comparative biblical scripture and historical wisdom texts from Bible-API."""

    # Curated thematic passages mapped to scientific and existential concepts
    PASSAGE_THEMES = {
        "creation": "Genesis 1:1-3",
        "universe": "Genesis 1:1-3",
        "light": "Genesis 1:3",
        "optics": "Genesis 1:3",
        "wisdom": "Proverbs 3:19-20",
        "knowledge": "Proverbs 2:6",
        "nature": "Job 12:7-10",
        "biology": "Job 12:7-10",
        "peace": "Philippians 4:7",
        "tranquility": "Psalm 23:1-3",
        "healing": "Jeremiah 30:17",
        "justice": "Micah 6:8",
        "balance": "Ecclesiastes 3:1-2",
        "order": "1 Corinthians 14:33",
    }

    def __init__(self):
        super().__init__(
            api_id="bible",
            name="Bible Comparative Scripture",
            domain_tags=["scripture", "theology", "bible", "comparative_religion", "ethics", "wisdom", "sacred", "proverbs"],
            base_url="https://bible-api.com",
            avg_latency_ms=260.0,
            timeout_seconds=8.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:comparative@qkw.local)",
            "Accept": "application/json",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_q = query.strip().lower()

        # Match thematic passage or default to Proverbs / Genesis
        target_passage = "Proverbs 3:19-20"
        for kw, passage in self.PASSAGE_THEMES.items():
            if kw in clean_q:
                target_passage = passage
                break

        url = f"{self.base_url}/{target_passage.replace(' ', '+')}"

        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    ref = data.get("reference", target_passage)
                    text = data.get("text", "").strip().replace("\n", " ")
                    translation = data.get("translation_name", "World English Bible")

                    snippet = f"Comparative Scripture [{ref} · {translation}]: \"{text[:220]}...\""

                    citations.append(
                        SourceCitation(
                            title=f"Comparative Scripture: {ref}",
                            source=self.api_id,
                            snippet=snippet,
                            url=f"https://www.biblegateway.com/passage/?search={target_passage.replace(' ', '+')}",
                            raw_metadata={
                                "reference": ref,
                                "translation": translation,
                                "passage_theme": target_passage,
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
                title=f"Comparative Moral Wisdom: {query.title()}",
                source=self.api_id,
                snippet=f"Classical Biblical Wisdom & Ethical Canon: Comparative theological and philosophical reflections on cosmic order, moral balance, and universal human conscience regarding '{query}'.",
                url="https://bible-api.com",
                raw_metadata={"synthetic_fallback": True, "domain": "comparative_scripture"},
            )
        ]
