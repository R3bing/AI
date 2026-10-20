"""PubMed API Client for Quantum Knowledge Weaver.
Queries the NCBI Entrez E-utilities (esearch & esummary) for biomedical and clinical literature.
"""

from typing import List
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class PubMedClient(BaseAPIClient):
    """Fetches biomedical literature and clinical publications from NIH / PubMed."""

    def __init__(self):
        super().__init__(
            api_id="pubmed",
            name="PubMed Biomedical Database",
            domain_tags=["medicine", "biology", "health", "clinical", "genetics", "neuroscience", "pharmacology"],
            base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
            avg_latency_ms=380.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (https://github.com/qkw)"
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_query = query.strip()

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            # 1. Search for PMIDs
            search_url = f"{self.base_url}/esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": clean_query,
                "retmode": "json",
                "retmax": limit,
                "sort": "pub_date",
            }
            search_resp = await client.get(search_url, params=search_params)
            search_resp.raise_for_status()
            search_data = search_resp.json()

            id_list = search_data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                return citations

            # 2. Fetch summaries for PMIDs
            summary_url = f"{self.base_url}/esummary.fcgi"
            summary_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "json",
            }
            sum_resp = await client.get(summary_url, params=summary_params)
            sum_resp.raise_for_status()
            sum_data = sum_resp.json().get("result", {})

            for pmid in id_list:
                item = sum_data.get(pmid)
                if not item or not isinstance(item, dict):
                    continue

                title = item.get("title", f"PubMed Article {pmid}").rstrip(".")
                source_journal = item.get("source", "PubMed")
                pub_date = item.get("pubdate", "")
                authors_list = [a.get("name", "") for a in item.get("authors", []) if "name" in a]

                snippet = f"Published in {source_journal} ({pub_date}). Authors: {', '.join(authors_list[:3])}."

                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

                citations.append(
                    SourceCitation(
                        source_id=f"pubmed-{pmid}",
                        source_name=self.name,
                        title=title,
                        url=url,
                        snippet=snippet,
                        relevance_score=0.91,
                        extra_metadata={
                            "pmid": pmid,
                            "journal": source_journal,
                            "pub_date": pub_date,
                            "authors": authors_list[:5],
                        },
                    )
                )

        return citations
