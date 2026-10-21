"""Data models and schemas for the Neural-Quantum Cognitive Brain.
Defines contracts for wave-particle duality states, synaptic flowchart nodes,
and dual-hemisphere (Aql vs. Qalb) cognitive activations.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


class DualityState(BaseModel):
    """Represents the atomic wave-particle superposition of the query:
    |Psi> = alpha |Aql (Particle/Logic)> + beta |Qalb (Wave/Heart)>
    where |alpha|^2 + |beta|^2 = 1.
    """
    particle_amplitude_alpha: float = Field(..., ge=0.0, le=1.0, description="Aql / Logic / Fact amplitude")
    wave_amplitude_beta: float = Field(..., ge=0.0, le=1.0, description="Qalb / Spiritual / Empathy amplitude")
    particle_probability: float = Field(..., description="|alpha|^2: Probability of pure logical analysis")
    wave_probability: float = Field(..., description="|beta|^2: Probability of emotional contemplation")
    dominant_state: Literal["Aql (Brain/Particle)", "Qalb (Heart/Wave)", "Equilibrium (Harmonious Dual)"]
    entropy_score: float = Field(..., description="Information entropy of input prompt")


class CognitiveFlowNode(BaseModel):
    """Individual node execution trace in the brain's reasoning flowchart."""
    step_id: str
    phase: Literal["Sensory Intake", "Duality Allocation", "Hemispheric Processing", "Corpus Callosum Synapse", "Coherent Synthesis"]
    hemisphere: Literal["Left (Brain/Aql)", "Right (Heart/Qalb)", "Both (Corpus Callosum)"]
    action_taken: str
    output_summary: str
    activation_energy: float


class CognitiveFlowchart(BaseModel):
    """Complete step-by-step neural reasoning trace."""
    nodes: List[CognitiveFlowNode] = Field(default_factory=list)
    total_synaptic_latency_ms: float = 0.0


class NeuralBrainResponse(BaseModel):
    """Holistic response balancing Particle (Logical truth) and Wave (Spiritual Sakoon)."""
    query: str
    duality_state: DualityState
    cognitive_flow: CognitiveFlowchart
    logical_factual_answer: str
    tafakkur_reflection: str
    harmonious_synthesis: str
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    cross_references: List[Dict[str, Any]] = Field(default_factory=list)
    apis_consulted: List[str] = Field(default_factory=list)
    quantum_telemetry: Optional[Dict[str, Any]] = None
    antigravity_verdict: str = Field(default="", description="Antigravity Meta-Cognitive Verdict synthesizing all databases")
    antigravity_insights: Dict[str, str] = Field(default_factory=dict, description="Structured insights across physics, epistemology, and meaning")
    parsed_query: Optional[Dict[str, Any]] = Field(default=None, description="Prefrontal decomposition of user inquiry")
    reasoning_trace: Optional[str] = Field(default=None, description="DeepSeek-R1 Chain-of-Thought reasoning trace")
    llm_provider_used: str = Field(default="cognitive_fallback", description="LLM provider employed for synthesis")
    tafakkur_details: Dict[str, Any] = Field(default_factory=dict, description="Full ontological scripture, tafseer, and comparative insights")
    multi_ai_dialogue: Optional[Dict[str, Any]] = Field(default=None, description="Multi-AI inter-neural dialogue between Gemini, DeepSeek, and Groq")
