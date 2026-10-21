"""Classical-Quantum Orchestrator Engine for Quantum Knowledge Weaver (QKW).
Coordinates vector cache lookup, QAOA quantum routing, asynchronous parallel API dispatch,
semantic cross-referencing, LLM synthesis, and knowledge graph persistence.
"""

import asyncio
import time
from typing import List, Optional
import structlog
from backend.config import settings
from backend.orchestrator.models import (
    QueryRequest,
    QueryResponse,
    SourceCitation,
    APIResult,
    CrossRefConnection,
)
from backend.apis.registry import registry
from backend.quantum.router import quantum_router
from backend.cross_reference.comparator import cross_referencer
from backend.synthesis.synthesizer import llm_synthesizer
from backend.memory.qdrant_store import vector_memory
from backend.memory.neo4j_store import graph_memory

logger = structlog.get_logger(__name__)


class OrchestratorEngine:
    """Master asynchronous orchestrator uniting classical concurrency with quantum optimization."""

    def __init__(self):
        self.registry = registry
        self.quantum_router = quantum_router
        self.cross_referencer = cross_referencer
        self.synthesizer = llm_synthesizer
        self.vector_memory = vector_memory
        self.graph_memory = graph_memory

    async def execute_query(self, request: QueryRequest) -> QueryResponse:
        """Executes the full QKW hybrid quantum-classical pipeline."""
        start_time = time.perf_counter()
        query = request.text.strip()
        log = logger.bind(query=query)
        log.info("qkw_pipeline_started")

        # 1. Neuro-Cognitive Query Parsing & Intent Deconstruction
        from backend.neural_brain.query_parser import query_parser
        parsed_query = query_parser.parse(query)
        log.info("query_cognitively_parsed", intent=parsed_query.cleaned_intent, domains=parsed_query.epistemic_domains)

        # 2. Semantic Vector Cache Check (Qdrant)
        query_embedding = self.cross_referencer._get_embedding(parsed_query.cleaned_intent or query)
        cached_result = self.vector_memory.lookup_cache(query_embedding, threshold=0.96)
        if cached_result:
            log.info("qkw_cache_hit_returning_cached_response")
            cached_result["cached"] = True
            cached_result["total_latency_ms"] = round((time.perf_counter() - start_time) * 1000.0, 2)
            cached_result["parsed_query"] = parsed_query.model_dump()
            return QueryResponse(**cached_result)

        # 3. Quantum or Classical API Routing
        apis_metadata = self.registry.get_api_metadata()
        quantum_telemetry = None

        if request.use_quantum:
            log.info("executing_qaoa_quantum_routing")
            target_k = min(request.max_sources, len(apis_metadata))
            selected_api_ids, quantum_telemetry = self.quantum_router.route_query(
                query=query,
                apis_metadata=apis_metadata,
                target_k=target_k,
                force_apis=request.force_apis,
                mixer_type=getattr(request, "mixer_type", "xy_mixer"),
            )
        else:
            # Classical heuristic selection
            if request.force_apis:
                selected_api_ids = [a for a in request.force_apis if a in self.registry.list_api_ids()]
            else:
                rel_scores = self.quantum_router.formulator.compute_relevance_scores(query, apis_metadata)
                sorted_apis = sorted(rel_scores.items(), key=lambda x: x[1], reverse=True)
                selected_api_ids = [item[0] for item in sorted_apis[: request.max_sources]]

        log.info("apis_selected_for_query", selected=selected_api_ids)

        # 4. Asynchronous Parallel API Dispatch with Targeted Queries
        # Each external engine receives clean, domain-adapted search tokens rather than conversational sentences.
        tasks = []
        for api_id in selected_api_ids:
            client = self.registry.get(api_id)
            if client:
                targeted_search_term = parsed_query.api_targeted_queries.get(api_id, parsed_query.cleaned_intent or query)
                tasks.append(client.search(query=targeted_search_term, limit=2))

        # Run all selected APIs concurrently with resilient timeout protection:
        # Completed tasks are preserved even if a slower API takes longer.
        results: List[APIResult] = []
        if tasks:
            task_objs = [asyncio.create_task(t) for t in tasks]
            done, pending = await asyncio.wait(task_objs, timeout=8.5)
            for p in pending:
                p.cancel()
            for t in done:
                try:
                    out = t.result()
                    if isinstance(out, APIResult):
                        results.append(out)
                except Exception as e:
                    log.warning("api_dispatch_exception", error=str(e))

        # Collect citations from all successful APIs
        all_citations: List[SourceCitation] = []
        apis_consulted: List[str] = []
        for r in results:
            if r.success and r.citations:
                all_citations.extend(r.citations)
                apis_consulted.append(r.api_name)

        # 5. Cross-Reference & Contradiction Detection
        cross_references: List[CrossRefConnection] = self.cross_referencer.compare_citations(all_citations)

        # 6. Universal Multi-Provider LLM Synthesis (DeepSeek / Gemini / Groq / OpenAI / Ollama / Cognitive Local)
        runtime_keys = dict(request.api_keys or {})
        if request.deepseek_api_key:
            runtime_keys["deepseek"] = request.deepseek_api_key
        if request.llm_provider:
            self.synthesizer.provider = request.llm_provider

        synthesized_answer = await self.synthesizer.synthesize(
            query=query,
            citations=all_citations,
            cross_references=cross_references,
            parsed_query=parsed_query,
            runtime_keys=runtime_keys,
        )

        total_latency = (time.perf_counter() - start_time) * 1000.0

        response_payload = {
            "query": query,
            "synthesized_answer": synthesized_answer,
            "citations": all_citations,
            "cross_references": cross_references,
            "quantum_routing": quantum_telemetry,
            "apis_consulted": apis_consulted,
            "cached": False,
            "total_latency_ms": round(total_latency, 2),
            "parsed_query": parsed_query.model_dump(),
            "reasoning_trace": self.synthesizer.last_reasoning_trace,
            "llm_provider_used": self.synthesizer.last_provider_used,
        }

        # 7. Memory Persistence (Vector DB + Knowledge Graph)
        try:
            self.vector_memory.cache_query(query, query_embedding, response_payload)
            self.graph_memory.store_knowledge_triples(query, all_citations, cross_references)
        except Exception as e:
            log.warning("memory_persistence_error", error=str(e))

        log.info("qkw_pipeline_completed", total_latency_ms=round(total_latency, 2), citations_count=len(all_citations))
        return QueryResponse(**response_payload)


# Global singleton orchestrator
orchestrator = OrchestratorEngine()
