
"""FastAPI Backend Application for Quantum Knowledge Weaver (QKW).
Exposes /query, /health, /apis, /quantum/route, and /memory/graph endpoints.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
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


@app.post("/nas/propose", tags=["NAS Controller AI"])
async def nas_propose_architecture(
    request: Optional[dict] = None,
):
    """Controller AI Meta-Designer: Proposes a new candidate architecture by sampling
    hyperparameters and structural building blocks from the search space.
    """
    from backend.nas.models import ArchitectureProposalRequest, SearchStrategy
    from backend.nas.controller import controller_ai
    req = ArchitectureProposalRequest(**(request or {}))
    candidate = controller_ai.propose_architecture(req)
    return {
        "candidate": candidate.model_dump(),
        "mermaid_dag": controller_ai.to_mermaid_dag(candidate),
        "pytorch_code": controller_ai.to_pytorch_code(candidate),
    }


@app.get("/nas/search-space", tags=["NAS Controller AI"])
async def nas_get_search_space():
    """Returns the predefined search space building blocks, dimensions, and hyperparameters."""
    from backend.nas.search_space import search_space
    return {
        "block_types": [b.value for b in search_space.block_types],
        "hidden_dimensions": search_space.hidden_dimensions,
        "attention_heads": search_space.attention_heads,
        "activations": [a.value for a in search_space.activations],
        "normalizations": [n.value for n in search_space.normalizations],
        "learning_rates": search_space.learning_rates,
        "optimizers": search_space.optimizers,
        "precisions": search_space.precisions,
    }


@app.post("/nas/cycle", tags=["NAS Closed-Loop"])
async def nas_run_single_cycle(
    request: Optional[dict] = None,
    epochs: int = 3,
):
    """Executes a complete 5-step closed-loop NAS cycle:
    Step 1: Architecture Proposal -> Step 2: Child Model Instantiation ->
    Step 3: Model Training -> Step 4: Performance Evaluation ->
    Step 5: Feedback Policy Update (REINFORCE).
    """
    from backend.nas.models import ArchitectureProposalRequest
    from backend.nas.orchestrator import nas_orchestrator
    req = ArchitectureProposalRequest(**(request or {}))
    cycle_result = nas_orchestrator.run_single_cycle(request=req, epochs=epochs)
    return cycle_result


@app.post("/nas/experiment", tags=["NAS Closed-Loop"])
async def nas_run_experiment(
    num_cycles: int = 3,
    request: Optional[dict] = None,
    epochs_per_child: int = 2,
):
    """Runs an autonomous multi-cycle NAS experiment looping across steps 1 to 5."""
    from backend.nas.models import ArchitectureProposalRequest
    from backend.nas.orchestrator import nas_orchestrator
    req = ArchitectureProposalRequest(**(request or {}))
    exp_state = nas_orchestrator.run_experiment(
        num_cycles=num_cycles,
        request=req,
        epochs_per_child=epochs_per_child,
    )
    return exp_state


@app.get("/nas/experiment-state", tags=["NAS Closed-Loop"])
async def nas_get_experiment_state():
    """Returns the cumulative Pareto frontier and reward history from the NAS experiment."""
    from backend.nas.orchestrator import nas_orchestrator
    return nas_orchestrator.experiment_state


@app.post("/dataset/sample", tags=["Training Data Hub"])

async def add_training_sample(payload: dict):
    """Saves a paired training record (query, grounded synthesis, raw AI completion, citations)
    for model fine-tuning and NAS child training.
    """
    from backend.synthesis.training_data_generator import training_data_generator
    sample = training_data_generator.create_paired_sample(
        query=payload.get("query", ""),
        grounded_synthesis=payload.get("grounded_synthesis", ""),
        citations=payload.get("citations", []),
        raw_ai_completion=payload.get("raw_ai_completion"),
        dominant_mode=payload.get("dominant_mode", "Aql & Qalb Balanced"),
        entropy_score=payload.get("entropy_score", 0.5),
    )
    return sample


@app.get("/dataset/samples", tags=["Training Data Hub"])
async def list_training_samples():
    """Lists all stored training samples."""
    from backend.synthesis.training_data_generator import training_data_generator
    return {"samples": training_data_generator.get_samples()}


@app.get("/dataset/export", tags=["Training Data Hub"])
async def export_training_dataset(format_type: str = "sft"):
    """Exports dataset formatted as JSONL string (sft, dpo, or sharegpt)."""
    from backend.synthesis.training_data_generator import training_data_generator
    content = training_data_generator.export_as_jsonl(format_type=format_type)
    return {"format": format_type, "jsonl": content}


@app.get("/dataset/stats", tags=["Training Data Hub"])
async def get_training_dataset_stats():
    """Returns dataset count, formats supported, and disk location."""
    from backend.synthesis.training_data_generator import training_data_generator
@app.get("/public-apis/stats", tags=["Public APIs Catalog"])
async def get_public_apis_stats():
    """Returns catalog statistics of 2,238+ public APIs across 52 categories."""
    from backend.apis.public_apis_catalog import public_apis_catalog
    return public_apis_catalog.get_statistics()


@app.get("/public-apis/search", tags=["Public APIs Catalog"])
async def search_public_apis(
    query: str,
    category: Optional[str] = None,
    no_auth_only: bool = False,
    limit: int = 10,
):
    """Searches the 2,238+ public APIs catalog."""
    from backend.apis.public_apis_catalog import public_apis_catalog
    results = public_apis_catalog.search_apis(query, category=category, no_auth_only=no_auth_only, limit=limit)
    return {"query": query, "count": len(results), "apis": results}


@app.post("/council/arena-session", tags=["Multi-AI Council Majlis"])
async def run_council_arena_session(payload: dict):
    """Executes a 5-participant multi-agent council debate observed by the Quantum Observer."""
    from backend.synthesis.multi_ai_council_arena import multi_ai_council_arena
    query = payload.get("query", "Universal duality and quantum observation")
    rounds = int(payload.get("rounds", 1))
    auto_learn = bool(payload.get("auto_learn", True))
    result = multi_ai_council_arena.run_council_session(query=query, rounds=rounds, auto_learn=auto_learn)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
