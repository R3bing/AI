"""Data models and schemas for Quantum Knowledge Weaver (QKW).
Defines contracts for requests, responses, citations, and quantum routing telemetry.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Incoming user question request."""
    text: str = Field(..., description="The user question or research prompt", min_length=2)
    use_quantum: bool = Field(default=True, description="Enable QAOA quantum routing for API selection")
    force_apis: Optional[List[str]] = Field(default=None, description="Explicitly override API selection")
    max_sources: int = Field(default=4, ge=1, le=11, description="Maximum number of sources to retrieve")
    mixer_type: str = Field(default="xy_mixer", description="QAOA Mixer Hamiltonian: xy_mixer or standard")
    llm_provider: Optional[str] = Field(default=None, description="Explicit LLM provider override ('deepseek', 'gemini', 'groq', 'openai', 'ollama')")
    deepseek_api_key: Optional[str] = Field(default=None, description="Optional DeepSeek API key for runtime synthesis")
    api_keys: Optional[Dict[str, str]] = Field(default=None, description="Optional runtime API keys for Gemini, Groq, or OpenAI")


class SourceCitation(BaseModel):
    """Individual citation ground truth extracted from an API."""
    source_id: str
    source_name: str
    title: str
    url: Optional[str] = None
    snippet: str
    relevance_score: float = 0.0
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)


class APIResult(BaseModel):
    """Raw response payload from an individual API client."""
    api_id: str
    api_name: str
    success: bool
    status_code: int = 200
    latency_ms: float = 0.0
    citations: List[SourceCitation] = Field(default_factory=list)
    raw_snippet: Optional[str] = None
    error: Optional[str] = None


class CrossRefConnection(BaseModel):
    """Cross-reference link discovered between two distinct sources."""
    source_a_id: str
    source_a_name: str
    source_b_id: str
    source_b_name: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    relationship: Literal["corroborates", "contradicts", "complements"] = "complements"
    notes: str = ""


class QuantumRoutingDetails(BaseModel):
    """Telemetry describing the QAOA routing optimization."""
    algorithm: str = "QAOA (Quantum Approximate Optimization Algorithm)"
    qubits_count: int
    qubo_variables: List[str]
    selected_apis: List[str]
    quantum_energy: float
    execution_time_ms: float
    backend_used: str = "Qiskit Aer Simulator"
    solution_probabilities: Dict[str, float] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    """Final response returned to the user or frontend."""
    query: str
    synthesized_answer: str
    citations: List[SourceCitation]
    cross_references: List[CrossRefConnection] = Field(default_factory=list)
    quantum_routing: Optional[QuantumRoutingDetails] = None
    apis_consulted: List[str] = Field(default_factory=list)
    cached: bool = False
    total_latency_ms: float = 0.0
    parsed_query: Optional[Dict[str, Any]] = None
    reasoning_trace: Optional[str] = Field(default=None, description="DeepSeek-R1 / CoT reasoning chain-of-thought")
    llm_provider_used: str = Field(default="cognitive_fallback", description="Provider used for synthesis")
    multi_ai_dialogue: Optional[Dict[str, Any]] = Field(default=None, description="Inter-AI dialogue debate trace across Gemini, DeepSeek, and Groq")


class HealthResponse(BaseModel):
    """System health check payload."""
    status: str = "healthy"
    version: str
    apis_available: List[str]
    quantum_engine: str
    llm_connected: bool
    vector_memory_status: str
    graph_memory_status: str
