"""Data models for Neural Architecture Search (NAS) and Controller AI.
Defines specifications for architectural building blocks, hyperparameters,
DAG connections, and candidate network proposals.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class BlockType(str, Enum):
    """Structural neural building blocks supported in the search space."""
    DENSE = "Dense"
    RESIDUAL_BLOCK = "ResidualBlock"
    MULTI_HEAD_ATTENTION = "MultiHeadAttention"
    TRANSFORMER_ENCODER = "TransformerEncoder"
    CONV2D = "Conv2D"
    LSTM_CELL = "LSTMCell"
    GRAPH_CONV = "GraphConv"
    QUANTUM_VARIATIONAL = "QuantumVariationalBlock"


class ActivationType(str, Enum):
    """Non-linear activation functions in the search space."""
    RELU = "relu"
    GELU = "gelu"
    SWISH = "swish"
    MISH = "mish"
    SILU = "silu"
    TANH = "tanh"
    QUANTUM_WAVE = "quantum_wave"


class NormType(str, Enum):
    """Normalization layers in the search space."""
    LAYER_NORM = "layer_norm"
    RMS_NORM = "rms_norm"
    BATCH_NORM = "batch_norm"
    NONE = "none"


class SearchStrategy(str, Enum):
    """Controller AI sampling and search strategies."""
    AUTOREGRESSIVE_RNN = "autoregressive_rnn"
    TRANSFORMER_SAMPLER = "transformer_sampler"
    EVOLUTIONARY_GENETIC = "evolutionary_genetic"
    RANDOM_UNIFORM = "random_uniform"


class BlockSpec(BaseModel):
    """Specification of an individual structural building block."""
    block_id: str = Field(..., description="Unique identifier for the block (e.g. block_1)")
    block_type: BlockType = Field(..., description="Type of neural building block")
    in_features: int = Field(..., description="Input feature dimension")
    out_features: int = Field(..., description="Output feature dimension")
    activation: ActivationType = Field(default=ActivationType.GELU, description="Non-linear activation")
    normalization: NormType = Field(default=NormType.LAYER_NORM, description="Normalization layer")
    dropout: float = Field(default=0.1, ge=0.0, le=0.8, description="Dropout rate")
    num_heads: Optional[int] = Field(default=None, description="Attention heads (if attention block)")
    kernel_size: Optional[int] = Field(default=None, description="Kernel size (if convolution block)")
    qubits: Optional[int] = Field(default=None, description="Number of qubits (if quantum variational block)")
    skip_connections: List[str] = Field(
        default_factory=list,
        description="List of predecessor block_ids that feed residual connections into this block"
    )
    estimated_params: int = Field(default=0, description="Estimated trainable parameters in this block")


class Hyperparameters(BaseModel):
    """Candidate architecture training hyperparameters sampled by the Controller."""
    learning_rate: float = Field(default=3e-4, description="Peak learning rate")
    optimizer: str = Field(default="AdamW", description="Optimizer choice (AdamW, Lion, Adafactor, SGD)")
    weight_decay: float = Field(default=1e-4, description="Weight decay / L2 regularization")
    batch_size: int = Field(default=32, description="Batch size")
    precision: str = Field(default="bf16", description="Floating-point precision (fp32, fp16, bf16)")
    warmup_steps: int = Field(default=500, description="Linear warmup learning rate schedule steps")
    dropout_rate: float = Field(default=0.1, description="Global dropout rate")


class ArchitectureCandidate(BaseModel):
    """Complete candidate neural architecture proposed by the Controller AI."""
    arch_id: str = Field(..., description="Unique UUID for candidate architecture")
    name: str = Field(..., description="Human-readable architectural designation (e.g. Q-NAS-Gen1-Alpha)")
    generation: int = Field(default=0, description="Evolutionary generation or controller iteration index")
    parent_ids: List[str] = Field(default_factory=list, description="IDs of parent architectures if mutated/crossover")
    strategy_used: SearchStrategy = Field(..., description="Search strategy employed by Controller AI")
    target_task: str = Field(default="multimodal_reasoning", description="Intended machine learning task")
    blocks: List[BlockSpec] = Field(..., description="Ordered sequence / DAG of neural building blocks")
    hyperparameters: Hyperparameters = Field(..., description="Sampled hyperparameter configuration")
    dag_topology: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Graph adjacency list mapping block_id to its input source block_ids"
    )
    estimated_parameters: int = Field(default=0, description="Total trainable parameter count")
    estimated_macs: int = Field(default=0, description="Estimated Multiply-Accumulate operations per forward pass")
    depth: int = Field(default=0, description="Total block depth")
    entropy: float = Field(default=0.0, description="Information entropy of controller decision distribution")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Auxiliary architectural telemetry")


class ArchitectureProposalRequest(BaseModel):
    """Incoming request to Controller AI for proposing candidate architectures."""
    strategy: SearchStrategy = Field(
        default=SearchStrategy.AUTOREGRESSIVE_RNN,
        description="Meta-designer search strategy"
    )
    target_task: str = Field(default="multimodal_reasoning", description="Target ML task")
    num_candidates: int = Field(default=1, ge=1, le=50, description="Number of candidate architectures to sample")
    min_layers: int = Field(default=3, ge=1, le=64, description="Minimum layers in candidate network")
    max_layers: int = Field(default=8, ge=2, le=128, description="Maximum layers in candidate network")
    input_dim: int = Field(default=128, ge=8, description="Input feature dimension")
    output_dim: int = Field(default=64, ge=1, description="Final output feature dimension")
    max_parameters: Optional[int] = Field(default=None, description="Optional parameter budget ceiling")
    temperature: float = Field(default=1.0, ge=0.05, le=5.0, description="Sampling softmax temperature")
    allow_quantum_blocks: bool = Field(default=True, description="Allow hybrid quantum variational layers")
