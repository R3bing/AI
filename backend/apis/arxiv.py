"""arXiv API Client for Quantum Knowledge Weaver.
Queries the arXiv API (Atom 1.0 XML) for scientific preprints across Physics, Math, CS, and Quantum.
"""

import xml.etree.ElementTree as ET
from typing import List
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class ArxivClient(BaseAPIClient):
    """Fetches peer-reviewed preprints and research papers from arXiv."""

    def __init__(self):
        super().__init__(
            api_id="arxiv",
            name="arXiv Scientific Preprints",
            domain_tags=["quantum", "physics", "computer_science", "mathematics", "ai", "machine_learning"],
            base_url="https://export.arxiv.org/api/query",
            avg_latency_ms=450.0,
            timeout_seconds=10.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (https://github.com/qkw)"
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_query = query.replace('"', "").strip()
        params = {
            "search_query": f"all:{clean_query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()

            # Parse Atom XML
            root = ET.fromstring(resp.text)
            ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

            for entry in root.findall("atom:entry", ns):
                title_elem = entry.find("atom:title", ns)
                summary_elem = entry.find("atom:summary", ns)
                id_elem = entry.find("atom:id", ns)
                published_elem = entry.find("atom:published", ns)

                raw_title = title_elem.text if title_elem is not None and title_elem.text else "Untitled"
                title = " ".join(raw_title.split())

                raw_summary = summary_elem.text if summary_elem is not None and summary_elem.text else ""
                snippet = " ".join(raw_summary.split())

                paper_url = id_elem.text.strip() if id_elem is not None and id_elem.text else ""
                published = published_elem.text.strip() if published_elem is not None and published_elem.text else ""

                authors = []
                for author in entry.findall("atom:author", ns):
                    name_elem = author.find("atom:name", ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                paper_id = paper_url.split("/abs/")[-1] if "/abs/" in paper_url else paper_url

                citations.append(
                    SourceCitation(
                        source_id=f"arxiv-{paper_id}",
                        source_name=self.name,
                        title=title,
                        url=paper_url,
                        snippet=snippet,
                        relevance_score=0.95,
                        extra_metadata={
                            "authors": authors[:4],
                            "published": published,
                            "arxiv_id": paper_id,
                        },
                    )
                )

        return citations
