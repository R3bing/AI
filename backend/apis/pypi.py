"""PyPI (Python Package Index) API Client for Quantum Knowledge Weaver.
Queries the official Python ecosystem registry of 500,000+ open-source libraries,
software dependencies, security metadata, and author manifests.
Keyless, open-access public API.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class PyPIClient(BaseAPIClient):
    """Fetches package architecture, releases, and dependencies from PyPI."""

    def __init__(self):
        super().__init__(
            api_id="pypi",
            name="PyPI Python Software Ecosystem",
            domain_tags=["python", "packages", "code", "software", "libraries", "dependencies", "ecosystem", "pypi"],
            base_url="https://pypi.org/pypi",
            avg_latency_ms=220.0,
            timeout_seconds=7.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:python@qkw.local)",
            "Accept": "application/json",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_q = query.strip().lower()

        # Extract primary package candidate word (e.g. "numpy", "torch", "scipy", "fastapi")
        words = [w for w in clean_q.split() if len(w) > 2]
        candidate_pkgs = words[:limit] if words else [clean_q]

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            for pkg in candidate_pkgs:
                try:
                    url = f"{self.base_url}/{pkg}/json"
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        data = resp.json()
                        info = data.get("info", {})
                        name = info.get("name", pkg)
                        version = info.get("version", "Latest")
                        summary = info.get("summary", "Python library registered on PyPI.")
                        author = info.get("author") or "Open Source Maintainers"
                        license_type = info.get("license") or "OSI Approved"
                        home_page = info.get("home_page") or info.get("package_url") or f"https://pypi.org/project/{pkg}/"

                        snippet = (
                            f"PyPI Official Library {name} v{version} [{license_type}] by {author}: "
                            f"{summary[:200]}..."
                        )

                        citations.append(
                            SourceCitation(
                                title=f"PyPI Package: {name} (v{version})",
                                source=self.api_id,
                                snippet=snippet,
                                url=home_page,
                                raw_metadata={
                                    "package": name,
                                    "version": version,
                                    "license": license_type,
                                    "author": author,
                                },
                            )
                        )
                except Exception:
                    continue

        if citations:
            return citations

        return self._generate_fallback(query, limit)

    def _generate_fallback(self, query: str, limit: int) -> List[SourceCitation]:
        return [
            SourceCitation(
                title=f"PyPI Open Source Ecosystem: {query.title()}",
                source=self.api_id,
                snippet=f"PyPI Software Index: Module specifications, dependency trees, and package metadata for Python implementations of '{query}'.",
                url=f"https://pypi.org/search/?q={query.replace(' ', '+')}",
                raw_metadata={"synthetic_fallback": True, "domain": "python_ecosystem"},
            )
        ]
