"""Central Registry of Knowledge Source APIs for Quantum Knowledge Weaver.
Registers clients, indexes their semantic domains, latency metrics, and retrieval limits.
"""

from typing import Dict, List, Optional
from backend.apis.base import BaseAPIClient
from backend.apis.wikipedia import WikipediaClient
from backend.apis.arxiv import ArxivClient
from backend.apis.quran import QuranClient
from backend.apis.hadith import HadithClient
from backend.apis.pubmed import PubMedClient
from backend.apis.nasa import NasaClient
from backend.apis.openalex import OpenAlexClient
from backend.apis.pubchem import PubChemClient


class APIRegistry:
    """Manages available API clients and provides metadata for Quantum QAOA routing."""

    def __init__(self):
        self._clients: Dict[str, BaseAPIClient] = {}
        self._register_default_clients()

    def _register_default_clients(self):
        self.register(WikipediaClient())
        self.register(ArxivClient())
        self.register(QuranClient())
        self.register(HadithClient())
        self.register(PubMedClient())
        self.register(NasaClient())
        self.register(OpenAlexClient())
        self.register(PubChemClient())

    def register(self, client: BaseAPIClient):
        self._clients[client.api_id] = client

    def get(self, api_id: str) -> Optional[BaseAPIClient]:
        return self._clients.get(api_id)

    def list_api_ids(self) -> List[str]:
        return list(self._clients.keys())

    def list_clients(self) -> List[BaseAPIClient]:
        return list(self._clients.values())

    def get_api_metadata(self) -> List[Dict]:
        return [
            {
                "id": client.api_id,
                "name": client.name,
                "domain_tags": client.domain_tags,
                "avg_latency_ms": client.avg_latency_ms,
                "base_url": client.base_url,
            }
            for client in self._clients.values()
        ]


# Global singleton instance
registry = APIRegistry()
