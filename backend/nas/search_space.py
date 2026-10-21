"""Predefined Search Space for Controller AI Meta-Designer.
Defines candidate neural structural blocks, dimensions, activation functions,
quantum variational modules, and hyperparameter search distributions.
"""

import math
import random
from typing import List, Dict, Any, Optional
from backend.nas.models import (
    BlockType,
    ActivationType,
    NormType,
    Hyperparameters,
)


class SearchSpace:
    """Predefined architectural search space and sampling priors."""

    def __init__(self):
        # Structural Building Blocks
        self.block_types: List[BlockType] = [
            BlockType.DENSE,
            BlockType.RESIDUAL_BLOCK,
            BlockType.MULTI_HEAD_ATTENTION,
            BlockType.TRANSFORMER_ENCODER,
            BlockType.LSTM_CELL,
            BlockType.GRAPH_CONV,
            BlockType.QUANTUM_VARIATIONAL,
        ]

        # Dimension Search Grid
        self.hidden_dimensions: List[int] = [64, 128, 256, 512, 1024]
        self.attention_heads: List[int] = [2, 4, 8, 16]
        self.quantum_qubit_options: List[int] = [4, 8, 11]

        # Non-Linear Activations
        self.activations: List[ActivationType] = [
            ActivationType.GELU,
            ActivationType.SWISH,
            ActivationType.MISH,
            ActivationType.SILU,
            ActivationType.RELU,
            ActivationType.QUANTUM_WAVE,
        ]

        # Normalization Layers
        self.normalizations: List[NormType] = [
            NormType.LAYER_NORM,
            NormType.RMS_NORM,
            NormType.BATCH_NORM,
            NormType.NONE,
        ]

        # Dropout Rates
        self.dropout_rates: List[float] = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3]

        # Hyperparameters Search Grid
        self.learning_rates: List[float] = [5e-5, 1e-4, 3e-4, 5e-4, 1e-3, 3e-3]
        self.optimizers: List[str] = ["AdamW", "Lion", "Adafactor", "SGD_Momentum"]
        self.weight_decays: List[float] = [1e-5, 1e-4, 1e-3, 1e-2]
        self.batch_sizes: List[int] = [16, 32, 64, 128]
        self.precisions: List[str] = ["bf16", "fp16", "fp32"]
        self.warmup_steps_options: List[int] = [200, 500, 1000, 2000]

    def get_candidate_block_types(self, allow_quantum: bool = True) -> List[BlockType]:
        """Returns allowed building block types."""
        if allow_quantum:
            return list(self.block_types)
        return [b for b in self.block_types if b != BlockType.QUANTUM_VARIATIONAL]

    def sample_hyperparameters(self, rng: Optional[random.Random] = None) -> Hyperparameters:
        """Samples a complete hyperparameter configuration from the search space."""
        r = rng or random
        return Hyperparameters(
            learning_rate=r.choice(self.learning_rates),
            optimizer=r.choice(self.optimizers),
            weight_decay=r.choice(self.weight_decays),
            batch_size=r.choice(self.batch_sizes),
            precision=r.choice(self.precisions),
            warmup_steps=r.choice(self.warmup_steps_options),
            dropout_rate=r.choice(self.dropout_rates),
        )

    def calculate_block_parameters(
        self,
        block_type: BlockType,
        in_features: int,
        out_features: int,
        num_heads: Optional[int] = None,
        qubits: Optional[int] = None,
    ) -> int:
        """Calculates theoretical trainable parameter count for a block."""
        if block_type == BlockType.DENSE:
            # W (in x out) + b (out)
            return (in_features * out_features) + out_features

        elif block_type == BlockType.RESIDUAL_BLOCK:
            # Two linear layers + projection if in != out
            params = (in_features * out_features) + out_features + (out_features * out_features) + out_features
            if in_features != out_features:
                params += (in_features * out_features)
            return params

        elif block_type == BlockType.MULTI_HEAD_ATTENTION:
            # Q, K, V projections (3 * in * in) + Out projection (in * out)
            return (3 * in_features * in_features) + (in_features * out_features) + (4 * in_features)

        elif block_type == BlockType.TRANSFORMER_ENCODER:
            # Self-attention + MLP feedforward (expand 4x)
            attn_params = (3 * in_features * in_features) + (in_features * in_features)
            mlp_params = (in_features * 4 * in_features) + (4 * in_features * out_features)
            return attn_params + mlp_params + (4 * in_features)

        elif block_type == BlockType.LSTM_CELL:
            # 4 gates * (in * out + out * out + 2 * out)
            return 4 * ((in_features * out_features) + (out_features * out_features) + (2 * out_features))

        elif block_type == BlockType.GRAPH_CONV:
            # W (in x out) + Root weight (in x out) + bias
            return (2 * in_features * out_features) + out_features

        elif block_type == BlockType.QUANTUM_VARIATIONAL:
            # Variational rotational angles per qubit across L layers (e.g. 3 rotations per qubit * 3 layers)
            q = qubits or 4
            num_layers = 3
            classical_proj = (in_features * q) + (q * out_features)
            quantum_variational_params = 3 * q * num_layers
            return classical_proj + quantum_variational_params

        return (in_features * out_features) + out_features


search_space = SearchSpace()
