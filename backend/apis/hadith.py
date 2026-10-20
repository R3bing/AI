"""Hadith API Client for Quantum Knowledge Weaver.
Queries authentic collections (Sahih Bukhari, Sahih Muslim, etc.) with verified English translations.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class HadithClient(BaseAPIClient):
    """Fetches prophetic traditions (Hadith) with narrator chains and reference numbers."""

    # Built-in high-value index of major prophetic traditions for instant, zero-latency retrieval
    CURATED_HADITH_CORPUS = [
        {
            "id": "bukhari-1",
            "collection": "Sahih al-Bukhari",
            "number": 1,
            "title": "Sahih al-Bukhari 1: Actions are by Intentions",
            "url": "https://sunnah.com/bukhari:1",
            "snippet": "I heard Allah's Messenger saying, 'The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.'",
            "keywords": ["intention", "action", "reward", "deed", "niyyah", "motivation"],
        },
        {
            "id": "bukhari-5678",
            "collection": "Sahih al-Bukhari",
            "number": 5678,
            "title": "Sahih al-Bukhari 5678: Medicine and Healing",
            "url": "https://sunnah.com/bukhari:5678",
            "snippet": "There is no disease that Allah has created, except that He also has created its treatment and cure.",
            "keywords": ["medicine", "cure", "disease", "healing", "health", "doctor", "treatment", "sick"],
        },
        {
            "id": "muslim-2699",
            "collection": "Sahih Muslim",
            "number": 2699,
            "title": "Sahih Muslim 2699: Seeking Knowledge",
            "url": "https://sunnah.com/muslim:2699",
            "snippet": "Whoever travels a path in search of knowledge, Allah will make easy for him a path to Paradise.",
            "keywords": ["knowledge", "learning", "education", "study", "science", "scholar", "wisdom"],
        },
        {
            "id": "bukhari-13",
            "collection": "Sahih al-Bukhari",
            "number": 13,
            "title": "Sahih al-Bukhari 13: The Golden Rule in Faith",
            "url": "https://sunnah.com/bukhari:13",
            "snippet": "None of you truly believes until he loves for his brother what he loves for himself.",
            "keywords": ["love", "brotherhood", "faith", "golden rule", "kindness", "neighbor", "ethics", "charity"],
        },
        {
            "id": "tirmidhi-1987",
            "collection": "Jami at-Tirmidhi",
            "number": 1987,
            "title": "Jami at-Tirmidhi 1987: Mercy to all Creation",
            "url": "https://sunnah.com/tirmidhi:1987",
            "snippet": "The merciful will be shown mercy by the Most Merciful. Be merciful to those on the earth and the One in the heavens will have mercy upon you.",
            "keywords": ["mercy", "compassion", "earth", "creation", "animals", "environment", "pity"],
        },
        {
            "id": "bukhari-6018",
            "collection": "Sahih al-Bukhari",
            "number": 6018,
            "title": "Sahih al-Bukhari 6018: Honesty and Truthfulness",
            "url": "https://sunnah.com/bukhari:6018",
            "snippet": "Truthfulness leads to righteousness, and righteousness leads to Paradise. A person continues to tell the truth until he is recorded with Allah as truthful.",
            "keywords": ["truth", "honesty", "righteousness", "integrity", "lying", "character"],
        },
        {
            "id": "muslim-223",
            "collection": "Sahih Muslim",
            "number": 223,
            "title": "Sahih Muslim 223: Cleanliness and Purity",
            "url": "https://sunnah.com/muslim:223",
            "snippet": "Cleanliness and purity are half of faith, and saying 'Al-hamdulillah' (praise be to Allah) fills the scale.",
            "keywords": ["cleanliness", "purity", "faith", "hygiene", "wudu", "health"],
        },
    ]

    def __init__(self):
        super().__init__(
            api_id="hadith",
            name="Hadith Traditions Corpus",
            domain_tags=["religion", "ethics", "hadith", "sunnah", "prophetic_tradition", "morality"],
            base_url="https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions",
            avg_latency_ms=190.0,
            timeout_seconds=8.0,
        )

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        query_words = set(query.lower().replace("?", "").replace(",", "").split())

        # First score our curated verified corpus
        scored_curated = []
        for item in self.CURATED_HADITH_CORPUS:
            score = 0
            for kw in item["keywords"]:
                if kw in query.lower() or any(w in kw for w in query_words if len(w) > 3):
                    score += 2
            for word in query_words:
                if len(word) > 3 and word in item["snippet"].lower():
                    score += 1
            if score > 0:
                scored_curated.append((score, item))

        scored_curated.sort(key=lambda x: x[0], reverse=True)

        for score, item in scored_curated[:limit]:
            citations.append(
                SourceCitation(
                    source_id=item["id"],
                    source_name=f"{self.name} ({item['collection']})",
                    title=item["title"],
                    url=item["url"],
                    snippet=item["snippet"],
                    relevance_score=min(0.98, 0.7 + score * 0.05),
                    extra_metadata={
                        "collection": item["collection"],
                        "hadith_number": item["number"],
                    },
                )
            )

        # If not enough matches, search the public CDN Bukhari edition
        if len(citations) < limit:
            try:
                async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                    cdn_url = f"{self.base_url}/eng-bukhari.min.json"
                    resp = await client.get(cdn_url)
                    if resp.status_code == 200:
                        data = resp.json()
                        hadiths = data.get("hadiths", [])
                        matches_found = 0
                        for h in hadiths:
                            text = h.get("text", "")
                            if any(w in text.lower() for w in query_words if len(w) > 4):
                                h_num = h.get("hadithnumber", 0)
                                h_id = f"bukhari-cdn-{h_num}"
                                if not any(c.source_id == h_id for c in citations):
                                    citations.append(
                                        SourceCitation(
                                            source_id=h_id,
                                            source_name=f"{self.name} (Sahih al-Bukhari)",
                                            title=f"Sahih al-Bukhari Hadith #{h_num}",
                                            url=f"https://sunnah.com/bukhari:{h_num}",
                                            snippet=text[:400] + "..." if len(text) > 400 else text,
                                            relevance_score=0.85,
                                            extra_metadata={"hadith_number": h_num},
                                        )
                                    )
                                    matches_found += 1
                                    if len(citations) >= limit:
                                        break
            except Exception:
                pass

        return citations
