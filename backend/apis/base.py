"""Base API client interface and abstractions for external data sources.
Provides standardized error handling, latency tracking, and response formatting.
"""

import time
import abc
from typing import List, Dict, Any, Optional
import httpx
import structlog
from backend.orchestrator.models import APIResult, SourceCitation

logger = structlog.get_logger(__name__)


class BaseAPIClient(abc.ABC):
    """Abstract base class for all integrated knowledge source APIs."""

    def __init__(
        self,
        api_id: str,
        name: str,
        domain_tags: List[str],
        base_url: str,
        avg_latency_ms: float = 250.0,
        timeout_seconds: float = 8.0,
    ):
        self.api_id = api_id
        self.name = name
        self.domain_tags = domain_tags
        self.base_url = base_url
        self.avg_latency_ms = avg_latency_ms
        self.timeout_seconds = timeout_seconds

    @abc.abstractmethod
    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        """Fetch records from the underlying API and return standard citations.
        Must be implemented by concrete API clients.
        """
        pass

    async def search(self, query: str, limit: int = 3) -> APIResult:
        """Standard wrapper that tracks latency and catches unexpected exceptions."""
        start_time = time.perf_counter()
        log = logger.bind(api_id=self.api_id, query=query)
        log.info("api_query_started")

        try:
            citations = await self.fetch(query, limit=limit)
            latency = (time.perf_counter() - start_time) * 1000.0
            log.info("api_query_success", citations_count=len(citations), latency_ms=latency)
            return APIResult(
                api_id=self.api_id,
                api_name=self.name,
                success=True,
                status_code=200,
                latency_ms=round(latency, 2),
                citations=citations,
            )
        except httpx.HTTPStatusError as e:
            latency = (time.perf_counter() - start_time) * 1000.0
            log.warning("api_http_error", status_code=e.response.status_code, error=str(e))
            return APIResult(
                api_id=self.api_id,
                api_name=self.name,
                success=False,
                status_code=e.response.status_code,
                latency_ms=round(latency, 2),
                error=f"HTTP {e.response.status_code}: {str(e)}",
            )
        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000.0
            log.error("api_unexpected_failure", error=str(e), latency_ms=latency)
            return APIResult(
                api_id=self.api_id,
                api_name=self.name,
                success=False,
                status_code=500,
                latency_ms=round(latency, 2),
                error=f"{type(e).__name__}: {str(e)}",
            )
