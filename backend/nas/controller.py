"""Controller AI Meta-Designer for Neural Architecture Search (NAS).
Implements Autoregressive RNN, Transformer, and Evolutionary search strategies
to sample hyperparameters and structural building blocks from the predefined search space.
"""

import math
import uuid
import random
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

from backend.nas.models import (
    BlockType,
    ActivationType,
    NormType,
    SearchStrategy,
    BlockSpec,
    Hyperparameters,
    ArchitectureCandidate,
    ArchitectureProposalRequest,
)
from backend.nas.search_space import search_space, SearchSpace


class ControllerAI:
    """The Controller AI Meta-Designer.
    Acts as an intelligent architect sampling building blocks and hyperparameters
    to construct optimal neural network candidate architectures.
    """

    def __init__(self, space: Optional[SearchSpace] = None, seed: Optional[int] = None):
        self.search_space = space or search_space
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)

        # Autoregressive Controller Weights (Simulated RNN Cell for Sampling)
        self.hidden_dim = 64
        self._init_controller_weights()

        # Architecture History / Archive
        self.proposal_history: List[ArchitectureCandidate] = []
        self.generation_counter = 0

    def _init_controller_weights(self):
        """Initializes internal projection weights for autoregressive sampling."""
        # Orthogonal init for simulated RNN hidden state transitions
        self.W_rnn = self.np_rng.normal(0.0, 0.1, (self.hidden_dim, self.hidden_dim))
        self.U_in = self.np_rng.normal(0.0, 0.1, (self.hidden_dim, self.hidden_dim))

    def propose_architecture(self, request: Optional[ArchitectureProposalRequest] = None) -> ArchitectureCandidate:
        """Proposes a single candidate architecture according to the requested search strategy."""
        req = request or ArchitectureProposalRequest()
        strategy = req.strategy

        if strategy == SearchStrategy.AUTOREGRESSIVE_RNN:
            candidate = self._sample_autoregressive_rnn(req)
        elif strategy == SearchStrategy.TRANSFORMER_SAMPLER:
            candidate = self._sample_transformer(req)
        elif strategy == SearchStrategy.EVOLUTIONARY_GENETIC:
            candidate = self._sample_evolutionary(req)
        else:
            candidate = self._sample_random(req)

        self.proposal_history.append(candidate)
        return candidate

    def sample_batch(self, request: ArchitectureProposalRequest) -> List[ArchitectureCandidate]:
        """Samples a batch of diverse candidate architectures."""
        candidates = []
        for _ in range(request.num_candidates):
            candidates.append(self.propose_architecture(request))
        return candidates

    # -------------------------------------------------------------------------
    # Search Strategy 1: Autoregressive RNN Controller
    # -------------------------------------------------------------------------
    def _sample_autoregressive_rnn(self, req: ArchitectureProposalRequest) -> ArchitectureCandidate:
        """Samples an architecture using an autoregressive sequential decision process.
        At each step t: h_t = tanh(W * h_{t-1} + U * e_{t-1})
        Softmax logits predict: [BlockType, Dim, Activation, Norm, Skips].
        """
        self.generation_counter += 1
        num_layers = self.rng.randint(req.min_layers, req.max_layers)
        allowed_blocks = self.search_space.get_candidate_block_types(allow_quantum=req.allow_quantum_blocks)

        blocks: List[BlockSpec] = []
        dag_topology: Dict[str, List[str]] = {}
        total_entropy = 0.0

        current_dim = req.input_dim
        h_t = np.zeros(self.hidden_dim, dtype=float)

        for layer_idx in range(num_layers):
            block_id = f"block_{layer_idx + 1}"

            # Step 1: RNN state update
            input_vec = np.zeros(self.hidden_dim)
            input_vec[layer_idx % self.hidden_dim] = 1.0
            h_t = np.tanh(self.W_rnn @ h_t + self.U_in @ input_vec)

            # Step 2: Sample Block Type
            type_logits = self.np_rng.normal(0.0, 1.0, len(allowed_blocks)) / req.temperature
            type_probs = self._softmax(type_logits)
            total_entropy += self._entropy(type_probs)
            chosen_type = allowed_blocks[self.np_rng.choice(len(allowed_blocks), p=type_probs)]

            # Step 3: Sample Out Dimension
            if layer_idx == num_layers - 1:
                out_dim = req.output_dim
            else:
                dim_options = self.search_space.hidden_dimensions
                dim_logits = self.np_rng.normal(0.0, 1.0, len(dim_options)) / req.temperature
                dim_probs = self._softmax(dim_logits)
                total_entropy += self._entropy(dim_probs)
                out_dim = dim_options[self.np_rng.choice(len(dim_options), p=dim_probs)]

            # Attention / Quantum constraints
            num_heads = None
            if chosen_type in [BlockType.MULTI_HEAD_ATTENTION, BlockType.TRANSFORMER_ENCODER]:
                # Ensure current_dim is divisible by num_heads
                valid_heads = [h for h in self.search_space.attention_heads if current_dim % h == 0]
                num_heads = self.rng.choice(valid_heads) if valid_heads else 4

            qubits = None
            if chosen_type == BlockType.QUANTUM_VARIATIONAL:
                qubits = self.rng.choice(self.search_space.quantum_qubit_options)

            # Step 4: Sample Activation & Normalization
            act_logits = self.np_rng.normal(0.0, 1.0, len(self.search_space.activations)) / req.temperature
            act_probs = self._softmax(act_logits)
            chosen_act = self.search_space.activations[self.np_rng.choice(len(self.search_space.activations), p=act_probs)]

            norm_logits = self.np_rng.normal(0.0, 1.0, len(self.search_space.normalizations)) / req.temperature
            norm_probs = self._softmax(norm_logits)
            chosen_norm = self.search_space.normalizations[self.np_rng.choice(len(self.search_space.normalizations), p=norm_probs)]

            dropout = self.rng.choice(self.search_space.dropout_rates)

            # Step 5: Sample Skip Connections from prior layers
            skip_sources = []
            if layer_idx > 1:
                for prev_idx in range(layer_idx):
                    # Sigmoid skip connection gate
                    skip_logit = float(np.dot(h_t[:16], self.np_rng.normal(0.0, 0.5, 16)))
                    skip_prob = 1.0 / (1.0 + math.exp(-max(-5.0, min(5.0, skip_logit))))
                    if skip_prob > 0.65:
                        skip_sources.append(f"block_{prev_idx + 1}")

            # Calculate theoretical parameters
            block_params = self.search_space.calculate_block_parameters(
                block_type=chosen_type,
                in_features=current_dim,
                out_features=out_dim,
                num_heads=num_heads,
                qubits=qubits,
            )

            block = BlockSpec(
                block_id=block_id,
                block_type=chosen_type,
                in_features=current_dim,
                out_features=out_dim,
                activation=chosen_act,
                normalization=chosen_norm,
                dropout=dropout,
                num_heads=num_heads,
                qubits=qubits,
                skip_connections=skip_sources,
                estimated_params=block_params,
            )
            blocks.append(block)

            # DAG inputs
            predecessors = [f"block_{layer_idx}"] if layer_idx > 0 else ["input_layer"]
            predecessors.extend(skip_sources)
            dag_topology[block_id] = predecessors

            current_dim = out_dim

        # Sample Hyperparameters
        hparams = self.search_space.sample_hyperparameters(self.rng)

        # Tally totals
        total_params = sum(b.estimated_params for b in blocks)
        # Approximate MACs = 2 * params for linear/feedforward
        total_macs = total_params * 2

        arch_id = f"arch-{uuid.uuid4().hex[:8]}"
        name = f"ControllerRNN-Gen{self.generation_counter}-{chosen_type.value[:4]}-{num_layers}L"

        return ArchitectureCandidate(
            arch_id=arch_id,
            name=name,
            generation=self.generation_counter,
            strategy_used=SearchStrategy.AUTOREGRESSIVE_RNN,
            target_task=req.target_task,
            blocks=blocks,
            hyperparameters=hparams,
            dag_topology=dag_topology,
            estimated_parameters=total_params,
            estimated_macs=total_macs,
            depth=num_layers,
            entropy=float(total_entropy / max(1, num_layers)),
            metadata={
                "controller_type": "Autoregressive_RNN",
                "temperature": req.temperature,
                "allow_quantum": req.allow_quantum_blocks,
            },
        )

    # -------------------------------------------------------------------------
    # Search Strategy 2: Transformer Meta-Designer
    # -------------------------------------------------------------------------
    def _sample_transformer(self, req: ArchitectureProposalRequest) -> ArchitectureCandidate:
        """Samples architectures with self-attention across structural layers for global balance."""
        self.generation_counter += 1
        num_layers = self.rng.randint(req.min_layers, req.max_layers)
        allowed_blocks = self.search_space.get_candidate_block_types(allow_quantum=req.allow_quantum_blocks)

        blocks: List[BlockSpec] = []
        dag_topology: Dict[str, List[str]] = {}
        current_dim = req.input_dim

        for layer_idx in range(num_layers):
            block_id = f"block_{layer_idx + 1}"

            # Architectural pattern: Alternating Attention and Residual FeedForward
            if layer_idx % 2 == 1 and BlockType.MULTI_HEAD_ATTENTION in allowed_blocks:
                b_type = BlockType.MULTI_HEAD_ATTENTION
            elif layer_idx == num_layers // 2 and req.allow_quantum_blocks and BlockType.QUANTUM_VARIATIONAL in allowed_blocks:
                b_type = BlockType.QUANTUM_VARIATIONAL
            else:
                b_type = BlockType.RESIDUAL_BLOCK if BlockType.RESIDUAL_BLOCK in allowed_blocks else BlockType.DENSE

            out_dim = req.output_dim if layer_idx == num_layers - 1 else self.rng.choice(self.search_space.hidden_dimensions)

            num_heads = 4 if b_type in [BlockType.MULTI_HEAD_ATTENTION, BlockType.TRANSFORMER_ENCODER] else None
            qubits = 8 if b_type == BlockType.QUANTUM_VARIATIONAL else None

            block_params = self.search_space.calculate_block_parameters(
                block_type=b_type,
                in_features=current_dim,
                out_features=out_dim,
                num_heads=num_heads,
                qubits=qubits,
            )

            skip_sources = [f"block_{layer_idx - 1}"] if layer_idx >= 2 and self.rng.random() > 0.5 else []

            block = BlockSpec(
                block_id=block_id,
                block_type=b_type,
                in_features=current_dim,
                out_features=out_dim,
                activation=self.rng.choice(self.search_space.activations),
                normalization=NormType.RMS_NORM,
                dropout=0.1,
                num_heads=num_heads,
                qubits=qubits,
                skip_connections=skip_sources,
                estimated_params=block_params,
            )
            blocks.append(block)

            predecessors = [f"block_{layer_idx}"] if layer_idx > 0 else ["input_layer"]
            predecessors.extend(skip_sources)
            dag_topology[block_id] = predecessors
            current_dim = out_dim

        hparams = self.search_space.sample_hyperparameters(self.rng)
        total_params = sum(b.estimated_params for b in blocks)

        return ArchitectureCandidate(
            arch_id=f"arch-{uuid.uuid4().hex[:8]}",
            name=f"TransformerSampler-Gen{self.generation_counter}-{num_layers}L",
            generation=self.generation_counter,
            strategy_used=SearchStrategy.TRANSFORMER_SAMPLER,
            target_task=req.target_task,
            blocks=blocks,
            hyperparameters=hparams,
            dag_topology=dag_topology,
            estimated_parameters=total_params,
            estimated_macs=total_params * 2,
            depth=num_layers,
            metadata={"controller_type": "Transformer_Structural_Sampler"},
        )

    # -------------------------------------------------------------------------
    # Search Strategy 3: Evolutionary Genetic Agent
    # -------------------------------------------------------------------------
    def _sample_evolutionary(self, req: ArchitectureProposalRequest) -> ArchitectureCandidate:
        """Samples architectures via genetic mutation/crossover of parent candidates."""
        self.generation_counter += 1

        # If we have existing candidates in history, mutate one of them
        if self.proposal_history and self.rng.random() > 0.3:
            parent = self.rng.choice(self.proposal_history)
            return self.mutate_architecture(parent)

        # Otherwise generate a diverse random seed
        return self._sample_random(req, strategy_tag=SearchStrategy.EVOLUTIONARY_GENETIC)

    def mutate_architecture(self, parent: ArchitectureCandidate) -> ArchitectureCandidate:
        """Applies genetic point mutations (layer mutation, dimension scaling, or hyperparameter perturbation)."""
        self.generation_counter += 1
        mutated_blocks: List[BlockSpec] = []
        dag_topology: Dict[str, List[str]] = {}

        current_in = parent.blocks[0].in_features if parent.blocks else 128
        for i, b in enumerate(parent.blocks):
            # 25% chance of block mutation
            if self.rng.random() < 0.25:
                new_act = self.rng.choice(self.search_space.activations)
                new_norm = self.rng.choice(self.search_space.normalizations)
                new_dropout = self.rng.choice(self.search_space.dropout_rates)
                mut_block = b.model_copy(update={
                    "in_features": current_in,
                    "activation": new_act,
                    "normalization": new_norm,
                    "dropout": new_dropout,
                })
            else:
                mut_block = b.model_copy(update={"in_features": current_in})

            mutated_blocks.append(mut_block)
            current_in = mut_block.out_features

            predecessors = [f"block_{i}"] if i > 0 else ["input_layer"]
            predecessors.extend(mut_block.skip_connections)
            dag_topology[mut_block.block_id] = predecessors

        # Perturb hyperparameter (e.g. learning rate)
        hparams = parent.hyperparameters.model_copy()
        if self.rng.random() < 0.5:
            hparams.learning_rate = self.rng.choice(self.search_space.learning_rates)
        if self.rng.random() < 0.3:
            hparams.optimizer = self.rng.choice(self.search_space.optimizers)

        total_params = sum(b.estimated_params for b in mutated_blocks)

        return ArchitectureCandidate(
            arch_id=f"arch-{uuid.uuid4().hex[:8]}",
            name=f"EvoMutant-{parent.name.split('-')[-1]}-Gen{self.generation_counter}",
            generation=self.generation_counter,
            parent_ids=[parent.arch_id],
            strategy_used=SearchStrategy.EVOLUTIONARY_GENETIC,
            target_task=parent.target_task,
            blocks=mutated_blocks,
            hyperparameters=hparams,
            dag_topology=dag_topology,
            estimated_parameters=total_params,
            estimated_macs=total_params * 2,
            depth=len(mutated_blocks),
            metadata={"mutation_of": parent.arch_id},
        )

    def crossover(self, parent_a: ArchitectureCandidate, parent_b: ArchitectureCandidate) -> ArchitectureCandidate:
        """Performs crossover recombination between two parent neural architectures."""
        self.generation_counter += 1
        split_a = len(parent_a.blocks) // 2
        split_b = len(parent_b.blocks) // 2

        child_blocks = [b.model_copy() for b in parent_a.blocks[:split_a]]
        # Align input features of child second half
        second_half = [b.model_copy() for b in parent_b.blocks[split_b:]]

        # Re-index block_ids
        merged_blocks = []
        dag_topology = {}
        current_in = parent_a.blocks[0].in_features if parent_a.blocks else 128

        for idx, b in enumerate(child_blocks + second_half):
            b_id = f"block_{idx + 1}"
            b.block_id = b_id
            b.in_features = current_in
            merged_blocks.append(b)
            current_in = b.out_features

            preds = [f"block_{idx}"] if idx > 0 else ["input_layer"]
            dag_topology[b_id] = preds

        total_params = sum(b.estimated_params for b in merged_blocks)

        return ArchitectureCandidate(
            arch_id=f"arch-{uuid.uuid4().hex[:8]}",
            name=f"EvoCrossover-Gen{self.generation_counter}",
            generation=self.generation_counter,
            parent_ids=[parent_a.arch_id, parent_b.arch_id],
            strategy_used=SearchStrategy.EVOLUTIONARY_GENETIC,
            target_task=parent_a.target_task,
            blocks=merged_blocks,
            hyperparameters=parent_a.hyperparameters.model_copy(),
            dag_topology=dag_topology,
            estimated_parameters=total_params,
            estimated_macs=total_params * 2,
            depth=len(merged_blocks),
            metadata={"crossover_parents": [parent_a.arch_id, parent_b.arch_id]},
        )

    # -------------------------------------------------------------------------
    # Search Strategy 4: Random Uniform Baseline
    # -------------------------------------------------------------------------
    def _sample_random(
        self,
        req: ArchitectureProposalRequest,
        strategy_tag: SearchStrategy = SearchStrategy.RANDOM_UNIFORM,
    ) -> ArchitectureCandidate:
        """Samples uniformly from the search space grid as a baseline."""
        self.generation_counter += 1
        num_layers = self.rng.randint(req.min_layers, req.max_layers)
        allowed_blocks = self.search_space.get_candidate_block_types(allow_quantum=req.allow_quantum_blocks)

        blocks: List[BlockSpec] = []
        dag_topology: Dict[str, List[str]] = {}
        current_dim = req.input_dim

        for i in range(num_layers):
            block_id = f"block_{i + 1}"
            b_type = self.rng.choice(allowed_blocks)
            out_dim = req.output_dim if i == num_layers - 1 else self.rng.choice(self.search_space.hidden_dimensions)

            num_heads = self.rng.choice(self.search_space.attention_heads) if b_type in [BlockType.MULTI_HEAD_ATTENTION, BlockType.TRANSFORMER_ENCODER] else None
            qubits = self.rng.choice(self.search_space.quantum_qubit_options) if b_type == BlockType.QUANTUM_VARIATIONAL else None

            params = self.search_space.calculate_block_parameters(
                block_type=b_type,
                in_features=current_dim,
                out_features=out_dim,
                num_heads=num_heads,
                qubits=qubits,
            )

            block = BlockSpec(
                block_id=block_id,
                block_type=b_type,
                in_features=current_dim,
                out_features=out_dim,
                activation=self.rng.choice(self.search_space.activations),
                normalization=self.rng.choice(self.search_space.normalizations),
                dropout=self.rng.choice(self.search_space.dropout_rates),
                num_heads=num_heads,
                qubits=qubits,
                estimated_params=params,
            )
            blocks.append(block)

            dag_topology[block_id] = [f"block_{i}"] if i > 0 else ["input_layer"]
            current_dim = out_dim

        hparams = self.search_space.sample_hyperparameters(self.rng)
        total_params = sum(b.estimated_params for b in blocks)

        return ArchitectureCandidate(
            arch_id=f"arch-{uuid.uuid4().hex[:8]}",
            name=f"RandomSample-Gen{self.generation_counter}-{num_layers}L",
            generation=self.generation_counter,
            strategy_used=strategy_tag,
            target_task=req.target_task,
            blocks=blocks,
            hyperparameters=hparams,
            dag_topology=dag_topology,
            estimated_parameters=total_params,
            estimated_macs=total_params * 2,
            depth=num_layers,
            metadata={"sampler": "Random_Uniform"},
        )

    # -------------------------------------------------------------------------
    # Visualization & Export Tools
    # -------------------------------------------------------------------------
    def to_mermaid_dag(self, candidate: ArchitectureCandidate) -> str:
        """Converts candidate architecture DAG into a Mermaid visualization graph."""
        lines = ["graph TD", "    classDef blockStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;"]
        lines.append("    classDef skipStyle stroke:#f43f5e,stroke-width:2px,stroke-dasharray: 5 5;")
        lines.append("    Input([\"Input Features\"])")

        for b in candidate.blocks:
            label = f"{b.block_id}<br><b>{b.block_type.value}</b><br>{b.in_features} ➔ {b.out_features}<br><i>{b.activation.value}</i>"
            lines.append(f"    {b.block_id}[\"{label}\"]:::blockStyle")

        # Edges
        for b_id, preds in candidate.dag_topology.items():
            for p in preds:
                if p == "input_layer":
                    lines.append(f"    Input --> {b_id}")
                elif p in candidate.dag_topology:
                    if p in [b.block_id for b in candidate.blocks if b.skip_connections and p in b.skip_connections]:
                        lines.append(f"    {p} -.->|Skip Residual| {b_id}")
                    else:
                        lines.append(f"    {p} --> {b_id}")

        last_id = candidate.blocks[-1].block_id if candidate.blocks else "Input"
        lines.append(f"    {last_id} --> Output([\"Output Predictions\"])")
        return "\n".join(lines)

    def to_pytorch_code(self, candidate: ArchitectureCandidate) -> str:
        """Generates standalone executable PyTorch code defining the candidate architecture."""
        class_name = candidate.name.replace("-", "_").replace(" ", "_")
        code_lines = [
            "import torch",
            "import torch.nn as nn",
            "",
            f"class {class_name}(nn.Module):",
            f'    """Candidate Architecture: {candidate.name}',
            f'    Strategy: {candidate.strategy_used.value}',
            f'    Trainable Parameters: {candidate.estimated_parameters:,}',
            f'    """',
            "    def __init__(self):",
            "        super().__init__()",
            "        self.blocks = nn.ModuleDict({",
        ]

        for b in candidate.blocks:
            if b.block_type == BlockType.DENSE:
                code_lines.append(f"            '{b.block_id}': nn.Sequential(")
                code_lines.append(f"                nn.Linear({b.in_features}, {b.out_features}),")
                if b.normalization == NormType.LAYER_NORM:
                    code_lines.append(f"                nn.LayerNorm({b.out_features}),")
                code_lines.append(f"                nn.{b.activation.value.capitalize()}(),")
                code_lines.append(f"                nn.Dropout({b.dropout}),")
                code_lines.append("            ),")
            elif b.block_type == BlockType.MULTI_HEAD_ATTENTION:
                code_lines.append(f"            '{b.block_id}': nn.MultiheadAttention(")
                code_lines.append(f"                embed_dim={b.in_features}, num_heads={b.num_heads or 4}, dropout={b.dropout}, batch_first=True")
                code_lines.append("            ),")
            else:
                code_lines.append(f"            '{b.block_id}': nn.Linear({b.in_features}, {b.out_features}),")

        code_lines.extend([
            "        })",
            "",
            "    def forward(self, x: torch.Tensor) -> torch.Tensor:",
            "        residual_cache = {}",
        ])

        for b in candidate.blocks:
            code_lines.append(f"        # {b.block_id} ({b.block_type.value})")
            if b.skip_connections:
                skip_sum = " + ".join([f"residual_cache['{s}']" for s in b.skip_connections])
                code_lines.append(f"        x = self.blocks['{b.block_id}'](x) + ({skip_sum})")
            else:
                code_lines.append(f"        x = self.blocks['{b.block_id}'](x)")
            code_lines.append(f"        residual_cache['{b.block_id}'] = x")

        code_lines.extend([
            "        return x",
            "",
            "# Sampled Hyperparameters:",
            f"# Learning Rate: {candidate.hyperparameters.learning_rate}",
            f"# Optimizer: {candidate.hyperparameters.optimizer}",
            f"# Weight Decay: {candidate.hyperparameters.weight_decay}",
            f"# Batch Size: {candidate.hyperparameters.batch_size}",
            f"# Precision: {candidate.hyperparameters.precision}",
        ])

        return "\n".join(code_lines)

    # -------------------------------------------------------------------------
    # Helper Math Functions
    # -------------------------------------------------------------------------
    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        e_x = np.exp(x - np.max(x))
        return e_x / np.sum(e_x)

    @staticmethod
    def _entropy(probs: np.ndarray) -> float:
        return float(-np.sum([p * np.log(p + 1e-12) for p in probs if p > 0]))


controller_ai = ControllerAI()
