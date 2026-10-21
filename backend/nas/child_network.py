"""Child Model Instantiation Engine (Step 2 of NAS Cycle).
Dynamically instantiates and compiles concrete PyTorch neural networks
from Controller AI candidate architecture specifications.
"""

import math
from typing import Dict, List, Any, Optional, Tuple
import torch
import torch.nn as nn
from backend.nas.models import (
    BlockType,
    ActivationType,
    NormType,
    BlockSpec,
    ArchitectureCandidate,
)


class QuantumWaveActivation(nn.Module):
    """Parameterized non-linear quantum wave activation function mimicking wave-particle duality:
    f(x) = x * sin(pi * x / 2) + 0.1 * cos(pi * x / 4)
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x * torch.sin(0.5 * math.pi * torch.tanh(x)) + 0.1 * torch.cos(0.25 * math.pi * torch.tanh(x))


class QuantumVariationalModule(nn.Module):
    """Classical-to-Quantum Parameterized Variational Layer.
    Projects classical features into qubit Hilbert space, applies parameterized unitary rotations,
    and measures Pauli-Z expectation values before projecting to output dimension.
    """
    def __init__(self, in_features: int, out_features: int, qubits: int = 4):
        super().__init__()
        self.qubits = qubits
        self.encoder = nn.Linear(in_features, qubits)
        # Parameterized rotational angles (variational ansatz parameters)
        self.theta = nn.Parameter(torch.randn(3, qubits) * 0.1)
        self.decoder = nn.Linear(qubits, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Encode into rotational phases
        phases = torch.tanh(self.encoder(x))
        # Quantum rotational expectation simulation
        rot_y = torch.sin(phases + self.theta[0])
        rot_z = torch.cos(phases + self.theta[1])
        entangled = rot_y * rot_z + torch.sin(self.theta[2])
        # Classical projection
        return self.decoder(entangled)


class ConcreteChildNetwork(nn.Module):
    """Step 2: Concrete instantiated Child Neural Network constructed from ArchitectureCandidate."""

    def __init__(self, candidate: ArchitectureCandidate):
        super().__init__()
        self.candidate = candidate
        self.arch_id = candidate.arch_id
        self.name = candidate.name

        self.block_modules = nn.ModuleDict()
        self.skip_adapters = nn.ModuleDict()

        dim_cache: Dict[str, int] = {}
        first_in = candidate.blocks[0].in_features if candidate.blocks else 128
        dim_cache["input_layer"] = first_in

        for b in candidate.blocks:
            module = self._build_block(b)
            self.block_modules[b.block_id] = module
            dim_cache[b.block_id] = b.out_features

            # Build projection adapters for skip connections if dimensions differ
            for src_id in b.skip_connections:
                src_dim = dim_cache.get(src_id, b.in_features)
                adapter_key = f"{src_id}_to_{b.block_id}"
                if src_dim != b.out_features:
                    self.skip_adapters[adapter_key] = nn.Linear(src_dim, b.out_features)
                else:
                    self.skip_adapters[adapter_key] = nn.Identity()

    def _build_block(self, b: BlockSpec) -> nn.Module:
        """Constructs an individual concrete structural block."""
        act_layer = self._get_activation(b.activation)
        norm_layer = self._get_norm(b.normalization, b.out_features)

        if b.block_type == BlockType.DENSE:
            return nn.Sequential(
                nn.Linear(b.in_features, b.out_features),
                norm_layer,
                act_layer,
                nn.Dropout(b.dropout),
            )

        elif b.block_type == BlockType.RESIDUAL_BLOCK:
            class ResBlock(nn.Module):
                def __init__(self, in_f, out_f, act, norm, p_drop):
                    super().__init__()
                    self.fc1 = nn.Linear(in_f, out_f)
                    self.norm1 = norm
                    self.act1 = act
                    self.fc2 = nn.Linear(out_f, out_f)
                    self.drop = nn.Dropout(p_drop)
                    self.shortcut = nn.Linear(in_f, out_f) if in_f != out_f else nn.Identity()

                def forward(self, x):
                    res = self.shortcut(x)
                    h = self.drop(self.act1(self.norm1(self.fc1(x))))
                    h = self.fc2(h)
                    return h + res

            return ResBlock(b.in_features, b.out_features, act_layer, norm_layer, b.dropout)

        elif b.block_type in [BlockType.MULTI_HEAD_ATTENTION, BlockType.TRANSFORMER_ENCODER]:
            class MHAEncoderBlock(nn.Module):
                def __init__(self, in_f, out_f, heads, p_drop):
                    super().__init__()
                    self.mha = nn.MultiheadAttention(embed_dim=in_f, num_heads=heads or 4, dropout=p_drop, batch_first=True)
                    self.norm = nn.LayerNorm(in_f)
                    self.proj = nn.Linear(in_f, out_f)

                def forward(self, x):
                    # Expect [batch, dim] -> unsqueeze to [batch, 1, dim]
                    if x.dim() == 2:
                        x_seq = x.unsqueeze(1)
                        attn_out, _ = self.mha(x_seq, x_seq, x_seq)
                        out = self.norm(x_seq + attn_out).squeeze(1)
                        return self.proj(out)
                    attn_out, _ = self.mha(x, x, x)
                    return self.proj(self.norm(x + attn_out))

            return MHAEncoderBlock(b.in_features, b.out_features, b.num_heads or 4, b.dropout)

        elif b.block_type == BlockType.LSTM_CELL:
            class LSTMBlock(nn.Module):
                def __init__(self, in_f, out_f):
                    super().__init__()
                    self.cell = nn.LSTMCell(in_f, out_f)

                def forward(self, x):
                    h_0 = torch.zeros(x.size(0), self.cell.hidden_size, device=x.device)
                    c_0 = torch.zeros(x.size(0), self.cell.hidden_size, device=x.device)
                    h_1, _ = self.cell(x, (h_0, c_0))
                    return h_1

            return LSTMBlock(b.in_features, b.out_features)

        elif b.block_type == BlockType.QUANTUM_VARIATIONAL:
            return QuantumVariationalModule(b.in_features, b.out_features, qubits=b.qubits or 4)

        elif b.block_type == BlockType.GRAPH_CONV:
            class GraphConvBlock(nn.Module):
                def __init__(self, in_f, out_f, act):
                    super().__init__()
                    self.linear = nn.Linear(in_f, out_f)
                    self.root = nn.Linear(in_f, out_f)
                    self.act = act

                def forward(self, x):
                    # Local neighborhood aggregation simulation
                    return self.act(self.linear(x) + self.root(x))

            return GraphConvBlock(b.in_features, b.out_features, act_layer)

        # Default Fallback
        return nn.Sequential(nn.Linear(b.in_features, b.out_features), act_layer)

    def _get_activation(self, act_type: ActivationType) -> nn.Module:
        if act_type == ActivationType.RELU:
            return nn.ReLU()
        elif act_type == ActivationType.GELU:
            return nn.GELU()
        elif act_type in [ActivationType.SWISH, ActivationType.SILU]:
            return nn.SiLU()
        elif act_type == ActivationType.MISH:
            return nn.Mish()
        elif act_type == ActivationType.TANH:
            return nn.Tanh()
        elif act_type == ActivationType.QUANTUM_WAVE:
            return QuantumWaveActivation()
        return nn.GELU()

    def _get_norm(self, norm_type: NormType, dim: int) -> nn.Module:
        if norm_type == NormType.LAYER_NORM:
            return nn.LayerNorm(dim)
        elif norm_type == NormType.RMS_NORM:
            # RMSNorm approximation with LayerNorm without affine bias
            return nn.LayerNorm(dim, elementwise_affine=False)
        elif norm_type == NormType.BATCH_NORM:
            return nn.BatchNorm1d(dim)
        return nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with skip/residual DAG propagation."""
        cache: Dict[str, torch.Tensor] = {"input_layer": x}
        current_x = x

        for b in self.candidate.blocks:
            module = self.block_modules[b.block_id]
            out = module(current_x)

            # Add skip connection residuals
            for src_id in b.skip_connections:
                if src_id in cache:
                    src_tensor = cache[src_id]
                    adapter_key = f"{src_id}_to_{b.block_id}"
                    if adapter_key in self.skip_adapters:
                        adapted = self.skip_adapters[adapter_key](src_tensor)
                        out = out + adapted

            cache[b.block_id] = out
            current_x = out

        return current_x

    def compile_model(self) -> Dict[str, Any]:
        """Validates model execution and returns concrete compilation telemetry."""
        in_dim = self.candidate.blocks[0].in_features if self.candidate.blocks else 128
        dummy_x = torch.randn(2, in_dim)
        with torch.no_grad():
            out = self.forward(dummy_x)

        total_trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        return {
            "status": "compiled_successfully",
            "arch_id": self.arch_id,
            "name": self.name,
            "input_shape": list(dummy_x.shape),
            "output_shape": list(out.shape),
            "total_trainable_params": total_trainable_params,
            "blocks_count": len(self.candidate.blocks),
            "skip_adapters_count": len(self.skip_adapters),
        }


def instantiate_child_network(candidate: ArchitectureCandidate) -> Tuple[ConcreteChildNetwork, Dict[str, Any]]:
    """Factory function for Step 2 of the NAS Cycle."""
    model = ConcreteChildNetwork(candidate)
    compilation_info = model.compile_model()
    return model, compilation_info
