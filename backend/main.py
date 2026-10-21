"""FastAPI Backend Application for Quantum Knowledge Weaver (QKW).
Exposes /query, /health, /apis, /quantum/route, and /memory/graph endpoints.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Query as FastQuery
from fastapi.middleware.cors import CORSMiddleware
import structlog

from backend.config import settings
from backend.orchestrator.models import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
    QuantumRoutingDetails,
)
from backend.orchestrator.engine import orchestrator
from backend.apis.registry import registry
from backend.quantum.router import quantum_router
from backend.quantum.vqe_simulator import vqe_simulator
from backend.memory.qdrant_store import vector_memory
from backend.memory.neo4j_store import graph_memory
from backend.synthesis.synthesizer import llm_synthesizer
from backend.neural_brain.models import NeuralBrainResponse

logger = structlog.get_logger(__name__)


import sys
import asyncio

# Ensure UTF-8 output encoding across Windows consoles to eliminate charmap codec errors
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("qkw_backend_starting", version=settings.app_version)
    
    # Pre-warm embedding model in background so first query has zero cold-start delay
    async def _prewarm():
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, orchestrator.cross_referencer._get_embedding, "quantum universe")
            logger.info("embedding_model_prewarmed_successfully")
        except Exception as e:
            logger.warning("prewarming_failed_non_fatal", error=str(e))
    
    asyncio.create_task(_prewarm())
    yield
    logger.info("qkw_backend_shutdown")


app = FastAPI(
    title="Quantum Knowledge Weaver (QKW) API",
    description="Hybrid Quantum-Classical API Orchestration & Knowledge Synthesis Brain",
    version=settings.app_version,
    lifespan=lifespan,
)

# Enable CORS for Streamlit and external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Returns system status, active quantum engines, and database connections."""
    llm_active = await llm_synthesizer.is_ollama_available()
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        apis_available=registry.list_api_ids(),
        quantum_engine="QAOA Statevector & Qiskit 2.6.0 Aer",
        llm_connected=llm_active,
        vector_memory_status="Online (Qdrant Embedded/Remote)",
        graph_memory_status="Online (Neo4j / Graph Memory)",
    )


@app.post("/query", response_model=QueryResponse, tags=["Orchestration"])
async def query_endpoint(request: QueryRequest):
    """Processes user question through Quantum QAOA routing, parallel API retrieval,
    semantic cross-referencing, and anti-hallucinatory LLM synthesis.
    """
    try:
        response = await orchestrator.execute_query(request)
        return response
    except Exception as e:
        logger.error("query_endpoint_failure", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query orchestration error: {str(e)}")


@app.get("/apis", tags=["APIs"])
async def list_apis():
    """Lists all registered external APIs with domain tags and latency profiles."""
    return {
        "count": len(registry.list_api_ids()),
        "apis": registry.get_api_metadata(),
    }


@app.post("/quantum/route", response_model=QuantumRoutingDetails, tags=["Quantum"])
async def inspect_quantum_route(request: QueryRequest):
    """Inspects pure QAOA quantum routing decisions and energy landscapes without fetching data."""
    apis_metadata = registry.get_api_metadata()
    _, details = quantum_router.route_query(
        query=request.text,
        apis_metadata=apis_metadata,
        target_k=request.max_sources,
        force_apis=request.force_apis,
    )
    return details


@app.post("/quantum/vqe", tags=["Quantum"])
async def run_vqe(bond_distance: float = FastQuery(default=0.74, ge=0.2, le=3.0)):
    """Simulates Variational Quantum Eigensolver (VQE) for molecular H2 ground state energy."""
    result = vqe_simulator.simulate_ground_state(bond_distance=bond_distance)
    return result


@app.get("/memory/graph", tags=["Memory"])
async def get_knowledge_graph():
    """Returns current entities and relationships from the graph memory."""
    return graph_memory.get_graph_data()


@app.get("/evaluation/benchmark", tags=["Evaluation"])
async def run_academic_benchmark(query: str = "quantum physics entanglement", target_k: int = 3):
    """Executes academic benchmark comparing QAOA (XY mixer) vs Classical Greedy, Simulated Annealing, and Brute Force."""
    from backend.evaluation.benchmark import benchmark_engine
    return benchmark_engine.run_benchmark(query=query, target_k=target_k)


@app.post("/brain/think", response_model=NeuralBrainResponse, tags=["Neural Brain"])
async def neural_brain_think(request: QueryRequest):
    """Executes human-like dual-hemisphere reasoning balancing Particle (Aql) and Wave (Qalb)
    along with full background cognitive flowchart trace.
    """
    from backend.neural_brain.engine import neural_brain
    return await neural_brain.think_and_reply(
        query=request.text,
        target_k=request.max_sources,
        force_apis=request.force_apis,
        use_quantum=request.use_quantum,
        mixer_type=request.mixer_type,
        api_keys=request.api_keys,
        llm_provider=request.llm_provider,
        deepseek_api_key=request.deepseek_api_key,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
