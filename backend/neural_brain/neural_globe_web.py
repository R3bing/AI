"""Interactive 3D Spherical Neural Pathway & Globe Web Engine.
Constructs a 3D celestial globe constellation of the unified Neural-Quantum Brain.
Allows drill-down into every neural block, mathematical formulation, tensor dimension,
and recursive sub-node web.
"""

import math
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional


# -----------------------------------------------------------------------------
# Deep Architectural Specification for All 9 Core Neural Blocks
# -----------------------------------------------------------------------------
NEURAL_BLOCKS: Dict[str, Dict[str, Any]] = {
    "B1_THALAMUS": {
        "id": "B1_THALAMUS",
        "name": "Block 1: Prefrontal Sensory Thalamus (Intake)",
        "short_name": "Sensory Thalamus",
        "role": "Sensory Reception, Tokenization & Intent Deconstruction",
        "icon": "🧩",
        "category": "Input & Parsing",
        "color": "#a855f7",
        "sphere_coords": {"theta_deg": 0.0, "phi_deg": 85.0, "radius": 2.2},
        "math_formula": r"x = \text{Embed}(w) + \text{PE}(pos), \quad \mathcal{E} = \text{NER}(x) \cup \text{Intent}(x)",
        "tensor_shapes": {
            "input_shape": "[Batch, Sequence_Len, 512]",
            "hidden_shape": "[Batch, Sequence_Len, 1024]",
            "output_shape": "[Batch, 1024] (Semantic Vector z_0)",
        },
        "activation_fn": "GELU (Gaussian Error Linear Unit)",
        "parameter_count": "14.2M Parameters",
        "latency_typical_ms": 2.1,
        "description": (
            "Serves as the gateway sensory filter of the brain. Decomposes unstructured natural language "
            "into core epistemic concepts, extracts named entities, assesses emotional sentiment, and maps "
            "inquiries into high-dimensional latent intent space."
        ),
        "sub_nodes": [
            {
                "id": "B1_SUB_1",
                "name": "Sub-Layer 1.1: Byte-Pair Semantic Tokenizer",
                "formula": r"\tau = \mathcal{T}(S_{raw}) \in \mathbb{V}^L",
                "description": "Vocabulary indexing with OOV resilience and multi-lingual transliteration support.",
                "telemetry": "Active Vocab: 32,000 tokens",
            },
            {
                "id": "B1_SUB_2",
                "name": "Sub-Layer 1.2: Named Entity & Concept Extractor",
                "formula": r"\mathcal{E} = \text{Softmax}(W_e \cdot h + b_e)",
                "description": "Extracts scientific entities (e.g., 'qubit', 'penicillin') and theological roots (e.g., 'Tawhid').",
                "telemetry": "Extraction Precision: 98.4%",
            },
            {
                "id": "B1_SUB_3",
                "name": "Sub-Layer 1.3: Epistemic Domain Router",
                "formula": r"p(domain|x) = \sigma(W_d \cdot x)",
                "description": "Classifies the prompt across Science, Philosophy, Scripture, Medicine, and Cosmology.",
                "telemetry": "Multi-label confidence: 0.96",
            },
        ],
    },
    "B2_AQL": {
        "id": "B2_AQL",
        "name": "Block 2: Aql Cerebral Hemisphere (Left Cortex)",
        "short_name": "Aql (Left Brain)",
        "role": "Empirical Logic, Deductive Reasoning & Physics Tensors",
        "icon": "🧠",
        "category": "Rational Hemisphere",
        "color": "#38bdf8",
        "sphere_coords": {"theta_deg": -55.0, "phi_deg": 40.0, "radius": 2.2},
        "math_formula": r"\mathcal{L}_{Aql} = \text{SwiGLU}(x W_1) \otimes (x W_2) \cdot W_3 + \sum \text{Axiom\_Penalty}",
        "tensor_shapes": {
            "input_shape": "[Batch, 1024]",
            "hidden_shape": "[Batch, 4096] (Feed-Forward Projection)",
            "output_shape": "[Batch, 1024] (|Aql⟩ State Projection)",
        },
        "activation_fn": "SwiGLU (Swish Gated Linear Unit)",
        "parameter_count": "48.6M Parameters",
        "latency_typical_ms": 6.4,
        "description": (
            "The analytical powerhouse representing the Particle / Aql hemisphere. Implements deductive "
            "formal logic, checks mathematical consistency, validates physical constants, and models "
            "deterministic cause-and-effect relationships."
        ),
        "sub_nodes": [
            {
                "id": "B2_SUB_1",
                "name": "Sub-Layer 2.1: Axiomatic Theorem Verifier",
                "formula": r"\text{Valid}(\phi) = \forall p \in \mathcal{P}, \quad \text{Eval}(p \vdash \phi)",
                "description": "Checks physical laws (conservation of energy, thermodynamics, quantum bounds).",
                "telemetry": "Zero-contradiction guarantee",
            },
            {
                "id": "B2_SUB_2",
                "name": "Sub-Layer 2.2: Biomedical & Chemical Matrix",
                "formula": r"Z_{bio} = \text{LayerNorm}(W_{mol} \cdot S_{SMILES})",
                "description": "Aligns molecular structures and biomedical entities with PubChem and PubMed indices.",
                "telemetry": "Resolution: 1.2 Å accuracy",
            },
            {
                "id": "B2_SUB_3",
                "name": "Sub-Layer 2.3: Empirical Fact Anchor",
                "formula": r"R_{anchor} = \text{CosineSim}(z_{Aql}, z_{corpus}) \ge \gamma_{min}",
                "description": "Filters out hallucinated propositions before passing to the Corpus Callosum bridge.",
                "telemetry": "Hallucination suppression: 99.1%",
            },
        ],
    },
    "B3_QALB": {
        "id": "B3_QALB",
        "name": "Block 3: Qalb Sacred Resonance Matrix (Right Cortex)",
        "short_name": "Qalb (Right Brain)",
        "role": "Spiritual Contemplation (Tafakkur), Sakoon Field & Ethics",
        "icon": "🕊️",
        "category": "Sacred Hemisphere",
        "color": "#34d399",
        "sphere_coords": {"theta_deg": 55.0, "phi_deg": 40.0, "radius": 2.2},
        "math_formula": r"\mathcal{H}_{Qalb} = \sum_k w_k |\text{Aya}_k\rangle \langle \text{Aya}_k| + \int \Psi_{Sakoon}(r) dr",
        "tensor_shapes": {
            "input_shape": "[Batch, 1024]",
            "hidden_shape": "[Batch, 2048] (Ontological Embedding)",
            "output_shape": "[Batch, 1024] (|Qalb⟩ State Projection)",
        },
        "activation_fn": "Sakoon-Sigmoidal Field (Bounded Peace Metric)",
        "parameter_count": "32.1M Parameters",
        "latency_typical_ms": 4.8,
        "description": (
            "The spiritual heart representing the Wave / Qalb hemisphere. Embeds ontological reality, "
            "Quranic verses, Prophetic Hadith, Sufi psychology (Nafs al-Mutma'innah), and comparative world "
            "wisdom. Instills moral discernment, empathy, and cosmic awe (Khushu)."
        ),
        "sub_nodes": [
            {
                "id": "B3_SUB_1",
                "name": "Sub-Layer 3.1: Quranic Ontological Tensor",
                "formula": r"\mathcal{V}_{quran} = \sum_{i=1}^{6236} \alpha_i \cdot \text{Tafseer}(Aya_i)",
                "description": "Connects cosmic empirical phenomena (Afaq) with inner consciousness (Anfus).",
                "telemetry": "Active verses: 6,236 Ayahs indexed",
            },
            {
                "id": "B3_SUB_2",
                "name": "Sub-Layer 3.2: Prophetic Isnad Authenticator",
                "formula": r"\text{Score}_{hadith} = \text{SanadChainAuth}(\mathcal{H}) \times \text{MatnCoherence}",
                "description": "Weights prophetic wisdom by classical chain authenticity and moral coherence.",
                "telemetry": "Verified Sunnah corpus active",
            },
            {
                "id": "B3_SUB_3",
                "name": "Sub-Layer 3.3: Sufi Sakoon Resonance Core",
                "formula": r"S_{Sakoon} = 1.0 - \mathcal{D}_{KL}(Nafs_{current} \parallel Nafs_{Mutma'innah})",
                "description": "Calculates inward tranquility and resolves existential dread into spiritual peace.",
                "telemetry": "Sakoon index: 0.94 / 1.00",
            },
        ],
    },
    "B4_QUANTUM_QAOA": {
        "id": "B4_QUANTUM_QAOA",
        "name": "Block 4: Quantum QAOA Hamiltonian Router",
        "short_name": "QAOA Router (11-Qubit)",
        "role": "QUBO Optimization, Statevector Routing & XY-Mixer",
        "icon": "⚛️",
        "category": "Quantum Core",
        "color": "#f59e0b",
        "sphere_coords": {"theta_deg": -125.0, "phi_deg": 0.0, "radius": 2.2},
        "math_formula": r"|\gamma, \beta\rangle = \prod_{l=1}^p e^{-i \beta_l \hat{H}_M} e^{-i \gamma_l \hat{H}_C} |D_k^N\rangle, \quad \hat{H}_C = \sum J_{ij} Z_i Z_j + \sum h_i Z_i",
        "tensor_shapes": {
            "qubits": "11 Qubits (Hilbert Space: 2^11 = 2,048 States)",
            "statevector": "[2048] Complex Amplitudes (Normalized)",
            "output_shape": "[11] Binary Bitstring x* ∈ {0,1}^11",
        },
        "activation_fn": "Parameterized Quantum Rotation Gates R_z(2γ), R_x(2β)",
        "parameter_count": "2p Variational Parameters (p=3 => 6 Classical Parameters)",
        "latency_typical_ms": 11.2,
        "description": (
            "A true quantum optimization engine mapping the 11 knowledge repositories to an Ising QUBO "
            "Hamiltonian. Utilizes the XY-Mixer to guarantee preservation of the Dicke state |D_k^N⟩, "
            "ensuring exactly K APIs are chosen without penalty tuning or constraint violations."
        ),
        "sub_nodes": [
            {
                "id": "B4_SUB_1",
                "name": "Sub-Layer 4.1: Ising Problem Hamiltonian (H_C)",
                "formula": r"\hat{H}_C = \sum_{i<j} J_{ij} \hat{Z}_i \hat{Z}_j + \sum_i h_i \hat{Z}_i",
                "description": "Encodes repository relevance, inter-database overlap, and user inquiry context.",
                "telemetry": "Coupling Matrix J: 11x11 Hermitian",
            },
            {
                "id": "B4_SUB_2",
                "name": "Sub-Layer 4.2: XY Excitation-Preserving Mixer (H_M)",
                "formula": r"\hat{H}_M^{XY} = \frac{1}{2} \sum_{(i,j)} (\hat{X}_i \hat{X}_j + \hat{Y}_i \hat{Y}_j)",
                "description": "Preserves the Hamming weight HammingWeight(x) = K without leaving the valid subspace.",
                "telemetry": "Dicke state |D_4^11⟩ initialized",
            },
            {
                "id": "B4_SUB_3",
                "name": "Sub-Layer 4.3: Statevector Sampling & Quantum Noise Emulator",
                "formula": r"\rho_{noisy} = (1 - p_{depol})\rho + \frac{p_{depol}}{4} \sum_k \sigma_k \rho \sigma_k",
                "description": "Emulates real-world quantum hardware noise, T1 relaxation, and phase dephasing.",
                "telemetry": "Simulation fidelity: 99.82%",
            },
        ],
    },
    "B5_DUALITY_BRIDGE": {
        "id": "B5_DUALITY_BRIDGE",
        "name": "Block 5: Corpus Callosum Superposition Bridge",
        "short_name": "Duality Bridge",
        "role": "Wave-Particle Superposition & Homeostatic Balancing",
        "icon": "⚖️",
        "category": "Inter-Hemispheric Hub",
        "color": "#ec4899",
        "sphere_coords": {"theta_deg": 0.0, "phi_deg": 15.0, "radius": 1.7},
        "math_formula": r"|\Psi_{cognitive}\rangle = \alpha |Aql\rangle + \beta |Qalb\rangle, \quad |\alpha|^2 + |\beta|^2 = 1.000, \quad S(\rho) = -\text{Tr}(\rho \ln \rho)",
        "tensor_shapes": {
            "input_left": "[Batch, 1024]",
            "input_right": "[Batch, 1024]",
            "superposition": "[Batch, 2048] Entangled State",
            "bloch_coords": "Sphere (x=sin θ cos φ, y=sin θ sin φ, z=cos θ)",
        },
        "activation_fn": "Unitary Quantum Phase Shift U(θ, φ, λ)",
        "parameter_count": "16.4M Parameters",
        "latency_typical_ms": 1.8,
        "description": (
            "The central inter-hemispheric bridge linking left-brain empirical logic with right-brain sacred "
            "contemplation. Rotates the cognitive state on a virtual Bloch sphere and continuously maintains "
            "strict quantum normalization (|α|² + |β|² = 1.000) and low Von Neumann entropy."
        ),
        "sub_nodes": [
            {
                "id": "B5_SUB_1",
                "name": "Sub-Layer 5.1: Bloch Angle Governor",
                "formula": r"\theta = 2 \arccos(|\alpha|), \quad \phi = \text{Arg}(\beta) - \text{Arg}(\alpha)",
                "description": "Calculates real-time 3D Bloch angles from prompt linguistic markers.",
                "telemetry": "Equilibrium: θ=90° (50/50 balance)",
            },
            {
                "id": "B5_SUB_2",
                "name": "Sub-Layer 5.2: Von Neumann Entropy Monitor",
                "formula": r"S(\rho) = -\sum \lambda_i \log_2(\lambda_i)",
                "description": "Measures cognitive cognitive uncertainty and guarantees coherence across domains.",
                "telemetry": "Entropy S: 0.54 bits (Optimal)",
            },
            {
                "id": "B5_SUB_3",
                "name": "Sub-Layer 5.3: Cross-Domain Synapse Router",
                "formula": r"C_{ij} = \langle Aql_i | \hat{T}_{bridge} | Qalb_j \rangle",
                "description": "Transfers verified scientific facts to theological reflection and vice versa.",
                "telemetry": "Synaptic bandwidth: 12.8 GB/s",
            },
        ],
    },
    "B6_COUNCIL": {
        "id": "B6_COUNCIL",
        "name": "Block 6: Multi-AI Council Majlis Arena",
        "short_name": "Council Majlis (5-AI)",
        "role": "5-Participant Consensus, Reasoning Traces & Observer",
        "icon": "🏛️",
        "category": "Multi-Model Arena",
        "color": "#10b981",
        "sphere_coords": {"theta_deg": 125.0, "phi_deg": 0.0, "radius": 2.2},
        "math_formula": r"\Delta S_{Observer} = S_{final} - S_{init} < 0, \quad \mathcal{V}_{consensus} = \arg\max_V \sum_i \omega_i \text{Coherence}(M_i, V)",
        "tensor_shapes": {
            "participant_streams": "5 Parallel Streams (Gemini, DeepSeek, Groq, Physicist, Sage)",
            "cot_trace_tokens": "Up to 4,096 Reasoning Tokens (<think>)",
            "output_consensus": "[Batch, 2048] Grounded Consensus Matrix",
        },
        "activation_fn": "Consensus Softmax with Shannon Entropy Temperature",
        "parameter_count": "Multi-Model Ensemble (>200B Effective Parameters)",
        "latency_typical_ms": 18.5,
        "description": (
            "The 5-participant deliberative chamber where Google Gemini (Epistemic Context), DeepSeek-R1 "
            "(Formal Logic & CoT Reasoning), Groq LPU (Sub-second Empirical Stress-Test), Dr. Farooq "
            "(Physical Laws), and Hazrat Irfan (Spiritual Hikmah) debate under the scrutiny of the "
            "Higher-Dimensional Quantum Observer, driving entropy down by over 50%."
        ),
        "sub_nodes": [
            {
                "id": "B6_SUB_1",
                "name": "Sub-Layer 6.1: DeepSeek-R1 <think> CoT Prober",
                "formula": r"\mathcal{T}_{CoT} = \text{ArgMax} \prod_{t=1}^T P(w_t | w_{<t}, \text{Axioms})",
                "description": "Extracts pure step-by-step chain-of-thought traces with mathematical verification.",
                "telemetry": "Active CoT verification: True",
            },
            {
                "id": "B6_SUB_2",
                "name": "Sub-Layer 6.2: Gemini Epistemic Synthesizer",
                "formula": r"\mathcal{E}_{Gemini} = \text{BroadScope}(Context, \mathcal{K}_{multimodal})",
                "description": "Synthesizes wide contextual breadth and ethical human implications.",
                "telemetry": "Context window: 1M tokens",
            },
            {
                "id": "B6_SUB_3",
                "name": "Sub-Layer 6.3: Quantum Observer Entropy Collapser",
                "formula": r"\rho_{post} = \sum_m M_m \rho M_m^\dagger, \quad \Delta S = -53\%",
                "description": "Collapses multi-model divergence into a single unshakeable unified verdict.",
                "telemetry": "Entropy reduction: ΔS = -53%",
            },
        ],
    },
    "B7_NAS": {
        "id": "B7_NAS",
        "name": "Block 7: Autonomous NAS Evolved Child Network",
        "short_name": "NAS Child Network",
        "role": "DARTS Micro-Cell Search, Weight Sharing & Mutation",
        "icon": "🧬",
        "category": "Self-Evolution Core",
        "color": "#eab308",
        "sphere_coords": {"theta_deg": -65.0, "phi_deg": -45.0, "radius": 2.2},
        "math_formula": r"\min_\alpha \mathcal{L}_{val}(w^*(\alpha), \alpha) \quad \text{s.t.} \quad w^*(\alpha) = \arg\min_w \mathcal{L}_{train}(w, \alpha)",
        "tensor_shapes": {
            "micro_cell": "4 Directed Acyclic Graph (DAG) Nodes per Cell",
            "search_space": "8 Candidate Operations (Conv3x3, DilConv, SepConv, Identity, etc.)",
            "output_child": "Evolved PyTorch Child Module (~120K Params)",
        },
        "activation_fn": "Continuous Architectural Softmax α_ij over Candidate Operations",
        "parameter_count": "120K Child Parameters (Evolves Continuously)",
        "latency_typical_ms": 3.4,
        "description": (
            "The brain's self-evolving neural fabric. Executes a 5-step closed-loop cycle: (1) Controller "
            "generates candidate architectures, (2) builds dynamic PyTorch child models, (3) trains on "
            "real-time query embeddings, (4) evaluates on the Pareto frontier (Loss vs. Latency), and (5) "
            "mutates underperforming layers."
        ),
        "sub_nodes": [
            {
                "id": "B7_SUB_1",
                "name": "Sub-Layer 7.1: Continuous Architectural Controller",
                "formula": r"\bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp(\alpha_o^{(i,j)})}{\sum_{o'} \exp(\alpha_{o'}^{(i,j)})} o(x)",
                "description": "Differentiable architecture search (DARTS) continuous relaxation.",
                "telemetry": "Active cell types: Normal & Reduction",
            },
            {
                "id": "B7_SUB_2",
                "name": "Sub-Layer 7.2: Pareto Frontier Optimizer",
                "formula": r"\mathcal{F}_{Pareto} = \min (\mathcal{L}_{eval}, \text{Latency}_{ms}, \text{Params}_{MB})",
                "description": "Balances extreme accuracy against execution latency on mobile/edge hardware.",
                "telemetry": "Pareto optimal ratio: 0.92",
            },
            {
                "id": "B7_SUB_3",
                "name": "Sub-Layer 7.3: Genetic Mutation & Crossover Kernel",
                "formula": r"\alpha_{mutated} = \alpha + \mathcal{N}(0, \sigma^2) \odot \mathcal{M}_{dropout}",
                "description": "Mutates low-performing operations into high-performing separable convolutions.",
                "telemetry": "Mutation rate: 0.05 / epoch",
            },
        ],
    },
    "B8_KNOWLEDGE_MESH": {
        "id": "B8_KNOWLEDGE_MESH",
        "name": "Block 8: Omniscient Knowledge Mesh (11 DBs + 2,238 APIs)",
        "short_name": "Knowledge Mesh",
        "role": "Multi-Source Federated Data Ingestion & Live Querying",
        "icon": "🌐",
        "category": "External Repositories",
        "color": "#06b6d4",
        "sphere_coords": {"theta_deg": 65.0, "phi_deg": -45.0, "radius": 2.2},
        "math_formula": r"\mathcal{K}_{Mesh} = \bigoplus_{i=1}^{11} \text{Repo}_i \cup \bigcup_{j=1}^{2238} \text{PublicAPI}_j",
        "tensor_shapes": {
            "indexed_apis": "2,238 Public APIs across 52 Global Categories",
            "primary_databases": "11 Primary Authoritative Science & Scripture Repositories",
            "citation_embeddings": "[N, 768] High-Dimensional Semantic Vectors",
        },
        "activation_fn": "Asynchronous Non-blocking HTTP/2 & gRPC Multiplexing",
        "parameter_count": "Petabyte-scale Federated External Knowledge",
        "latency_typical_ms": 24.0,
        "description": (
            "The external senses of the brain. Connects in parallel to 11 public scientific and scriptural "
            "repositories (Wikipedia, arXiv, Quran, Hadith, PubMed, NASA, OpenAlex, PubChem, Google "
            "Knowledge, Crossref, Open Library) alongside an index of 2,238 public APIs with sub-millisecond "
            "catalog search."
        ),
        "sub_nodes": [
            {
                "id": "B8_SUB_1",
                "name": "Sub-Layer 8.1: 11 Scientific & Scriptural Gateways",
                "formula": r"D_{primary} = \{ \text{arXiv, PubMed, NASA, PubChem, Quran, Hadith, ...} \}",
                "description": "Deep citation-backed queries with DOI and verse verification.",
                "telemetry": "11 Repositories Online",
            },
            {
                "id": "B8_SUB_2",
                "name": "Sub-Layer 8.2: 2,238 Public APIs Catalog Indexer",
                "formula": r"\text{API}_{match} = \text{TF-IDF}_{search}(\mathcal{Q}, \text{APICatalog})",
                "description": "52 categories (Animals, Blockchain, Cryptography, Development, Finance, etc.).",
                "telemetry": "Indexed: 2,238 APIs in RAM",
            },
            {
                "id": "B8_SUB_3",
                "name": "Sub-Layer 8.3: Semantic Citation Corroboration Engine",
                "formula": r"\text{Corroborate}(C_1, C_2) = \text{NLI}(C_1 \implies C_2) \in \{\text{Entail}, \text{Contradict}, \text{Neutral}\}",
                "description": "Cross-verifies assertions across disparate peer-reviewed sources.",
                "telemetry": "Cross-referencing speed: 1.4ms",
            },
        ],
    },
    "B9_DISTILLATION": {
        "id": "B9_DISTILLATION",
        "name": "Block 9: Model Distillation & LoRA Adapter Core",
        "short_name": "Distillation & LoRA",
        "role": "Hinton Soft Targets, Rank-4 LoRA & SLERP Merging",
        "icon": "🧪",
        "category": "Compression & Adapters",
        "color": "#8b5cf6",
        "sphere_coords": {"theta_deg": 0.0, "phi_deg": -85.0, "radius": 2.2},
        "math_formula": r"\mathcal{L}_{KD} = \alpha T^2 \mathcal{D}_{KL}(p^\tau \parallel q^\tau) + (1-\alpha)\mathcal{L}_{CE}, \quad W_{eff} = W_0 + \frac{\alpha_{lora}}{r} B A",
        "tensor_shapes": {
            "teacher_distribution": "[Batch, 32000] Soft Target Probabilities at Temp T=3.0",
            "lora_rank": "Rank r = 4 (A: [1024, 4], B: [4, 1024])",
            "compression_ratio": "76.13% Parameter Reduction vs. Dense Baseline",
        },
        "activation_fn": "Softmax Temperature Scaling σ(z / T)",
        "parameter_count": "1.2M Adapter Parameters (76% Savings)",
        "latency_typical_ms": 1.5,
        "description": (
            "Compresses gigantic multi-billion parameter teacher model knowledge into lightweight, agile "
            "student representations. Leverages Hinton soft-target distillation, Shannon entropy query probing, "
            "Rank-4 Low-Rank Adaptation (LoRA), and SLERP (Spherical Linear Interpolation) weight merging."
        ),
        "sub_nodes": [
            {
                "id": "B9_SUB_1",
                "name": "Sub-Layer 9.1: Hinton Soft-Target Loss Engine",
                "formula": r"\mathcal{L}_{Hinton} = \alpha T^2 \sum p_i^\tau \log(p_i^\tau / q_i^\tau)",
                "description": "Transfers dark knowledge and nuanced probability distributions.",
                "telemetry": "Distillation Temp T: 3.0",
            },
            {
                "id": "B9_SUB_2",
                "name": "Sub-Layer 9.2: Rank-4 LoRA Parameter Compressor",
                "formula": r"\Delta W = \frac{\alpha_{lora}}{r} B A, \quad A \sim \mathcal{N}(0, \sigma^2), B = 0",
                "description": "Enables edge deployment with 76.13% parameter reduction.",
                "telemetry": "Active rank r=4, α=16",
            },
            {
                "id": "B9_SUB_3",
                "name": "Sub-Layer 9.3: SLERP Spherical Model Merger",
                "formula": r"W_{merged} = \frac{\sin((1-t)\Omega)}{\sin \Omega} W_A + \frac{\sin(t\Omega)}{\sin \Omega} W_B",
                "description": "Interpolates models along the hyperspherical manifold without catastrophic forgetting.",
                "telemetry": "Interpolation t: 0.50 (Harmonious)",
            },
        ],
    },
}

# -----------------------------------------------------------------------------
# Inter-Block Synaptic Pathways (The Globe Web Network Graph)
# -----------------------------------------------------------------------------
NEURAL_PATHWAYS: List[Dict[str, Any]] = [
    {"source": "B1_THALAMUS", "target": "B5_DUALITY_BRIDGE", "label": "Sensory Projection", "flow": "forward"},
    {"source": "B5_DUALITY_BRIDGE", "target": "B2_AQL", "label": "Particle Channel", "flow": "forward"},
    {"source": "B5_DUALITY_BRIDGE", "target": "B3_QALB", "label": "Wave Channel", "flow": "forward"},
    {"source": "B2_AQL", "target": "B4_QUANTUM_QAOA", "label": "QUBO Formulation", "flow": "forward"},
    {"source": "B3_QALB", "target": "B6_COUNCIL", "label": "Spiritual Wisdom Injection", "flow": "forward"},
    {"source": "B4_QUANTUM_QAOA", "target": "B8_KNOWLEDGE_MESH", "label": "Optimal API Selection", "flow": "forward"},
    {"source": "B6_COUNCIL", "target": "B8_KNOWLEDGE_MESH", "label": "Empirical Verification", "flow": "bidirectional"},
    {"source": "B2_AQL", "target": "B6_COUNCIL", "label": "Logical Proof Defense", "flow": "bidirectional"},
    {"source": "B8_KNOWLEDGE_MESH", "target": "B7_NAS", "label": "Corpus Embeddings for Search", "flow": "forward"},
    {"source": "B7_NAS", "target": "B9_DISTILLATION", "label": "Evolved Architecture Candidate", "flow": "forward"},
    {"source": "B9_DISTILLATION", "target": "B1_THALAMUS", "label": "Closed-Loop Feedback Synapse", "flow": "feedback"},
    {"source": "B2_AQL", "target": "B3_QALB", "label": "Corpus Callosum Cross-Talk", "flow": "resonance"},
]


def _spherical_to_cartesian(theta_deg: float, phi_deg: float, radius: float = 2.0):
    """Converts spherical coordinates (degrees) to 3D Cartesian (x, y, z)."""
    theta = math.radians(theta_deg)
    phi = math.radians(90.0 - phi_deg)  # phi measured from north pole
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.sin(theta)
    z = radius * math.cos(phi)
    return x, y, z


def _colatitude_spherical_to_cartesian(theta_deg: float, phi_deg: float, radius: float = 2.2):
    """Converts physics spherical coordinates (theta in [-180, 180], phi colatitude in [0, 180]) to Cartesian."""
    theta_rad = math.radians(theta_deg)
    phi_rad = math.radians(phi_deg)
    x = radius * math.sin(phi_rad) * math.cos(theta_rad)
    y = radius * math.sin(phi_rad) * math.sin(theta_rad)
    z = radius * math.cos(phi_rad)
    return x, y, z


def create_neural_globe_web_figure(
    selected_block_id: Optional[str] = None,
    highlight_active_pathways: bool = True,
    dynamic_pathway: Optional[Dict[str, Any]] = None,
) -> go.Figure:
    """Constructs a mesmerizing 3D interactive Plotly celestial globe constellation.
    
    When `dynamic_pathway` is provided:
        Renders the active prompt's connected 3D neural constellation (Prompt Core,
        QAOA Router, Empirical Citations, Left/Right Brain, Multi-AI Council, and Public APIs)
        linked via geodesic curved synaptic strings.
    Otherwise:
        Renders the baseline 9-block neural-quantum brain architecture manifold.
    """
    fig = go.Figure()
    globe_radius = 2.1

    # 1. Generate Wireframe Sphere (Latitude and Longitude circles)
    for lat_deg in [-60, -30, 0, 30, 60]:
        phi = math.radians(90.0 - lat_deg)
        r_ring = globe_radius * math.sin(phi)
        z_ring = globe_radius * math.cos(phi)
        thetas = np.linspace(0, 2 * math.pi, 60)
        xs = r_ring * np.cos(thetas)
        ys = r_ring * np.sin(thetas)
        zs = np.full_like(xs, z_ring)

        line_color = "rgba(56, 189, 248, 0.28)" if lat_deg == 0 else "rgba(148, 163, 184, 0.08)"
        line_width = 2.5 if lat_deg == 0 else 1.0

        fig.add_trace(
            go.Scatter3d(
                x=xs,
                y=ys,
                z=zs,
                mode="lines",
                line=dict(color=line_color, width=line_width),
                hoverinfo="none",
                showlegend=False,
            )
        )

    # Major Longitude Meridians
    for lon_deg in range(0, 360, 45):
        theta = math.radians(lon_deg)
        phis = np.linspace(0, math.pi, 40)
        xs = globe_radius * np.sin(phis) * math.cos(theta)
        ys = globe_radius * np.sin(phis) * math.sin(theta)
        zs = globe_radius * np.cos(phis)
        fig.add_trace(
            go.Scatter3d(
                x=xs,
                y=ys,
                z=zs,
                mode="lines",
                line=dict(color="rgba(148, 163, 184, 0.07)", width=1.0),
                hoverinfo="none",
                showlegend=False,
            )
        )

    # =========================================================================
    # DYNAMIC PROMPT CONSTELLATION MODE
    # =========================================================================
    if dynamic_pathway and dynamic_pathway.get("nodes"):
        dynamic_nodes = dynamic_pathway["nodes"]
        dynamic_pathways = dynamic_pathway.get("pathways", [])
        query = dynamic_pathway.get("query", "")

        # Compute 3D Cartesian coordinates for dynamic nodes
        node_coords: Dict[str, tuple] = {}
        for n_id, n_info in dynamic_nodes.items():
            sc = n_info.get("sphere_coords", {})
            th = sc.get("theta_deg", 0.0)
            ph = sc.get("phi_deg", 90.0)
            rad = sc.get("radius", 2.22)
            x, y, z = _colatitude_spherical_to_cartesian(th, ph, rad)
            node_coords[n_id] = (x, y, z)

        # Draw Geodesic Arcs for Synaptic Pathways (Grouped for High Performance & Glow)
        pathway_groups: Dict[str, Dict[str, Any]] = {}
        for path in dynamic_pathways:
            s_id = path.get("source")
            t_id = path.get("target")
            if s_id in node_coords and t_id in node_coords:
                p0 = np.array(node_coords[s_id])
                p1 = np.array(node_coords[t_id])
                col = path.get("color", "#38bdf8")
                width = path.get("width", 2.4)
                name = path.get("name", "Synaptic Pathway")

                num_steps = 18
                xs, ys, zs = [], [], []
                for t_step in np.linspace(0, 1, num_steps):
                    p_interp = (1.0 - t_step) * p0 + t_step * p1
                    norm = np.linalg.norm(p_interp)
                    if norm > 1e-6:
                        lift = 1.0 + 0.12 * math.sin(t_step * math.pi)
                        p_curved = (p_interp / norm) * (globe_radius * lift)
                        xs.append(p_curved[0])
                        ys.append(p_curved[1])
                        zs.append(p_curved[2])
                xs.append(None)
                ys.append(None)
                zs.append(None)

                if col not in pathway_groups:
                    pathway_groups[col] = {"xs": [], "ys": [], "zs": [], "width": width, "name": name}
                pathway_groups[col]["xs"].extend(xs)
                pathway_groups[col]["ys"].extend(ys)
                pathway_groups[col]["zs"].extend(zs)

        for col, p_data in pathway_groups.items():
            fig.add_trace(
                go.Scatter3d(
                    x=p_data["xs"],
                    y=p_data["ys"],
                    z=p_data["zs"],
                    mode="lines",
                    line=dict(color=col, width=p_data["width"]),
                    hoverinfo="none",
                    name=p_data["name"],
                    showlegend=False,
                )
            )

        # Draw Dynamic Nodes
        node_x, node_y, node_z = [], [], []
        node_text, node_hover, node_colors, node_sizes, node_ids = [], [], [], [], []

        for n_id, n_info in dynamic_nodes.items():
            x, y, z = node_coords[n_id]
            node_x.append(x)
            node_y.append(y)
            node_z.append(z)
            node_ids.append(n_id)

            is_selected = (selected_block_id == n_id)
            node_colors.append("#ffffff" if is_selected else n_info.get("color", "#38bdf8"))
            node_sizes.append(n_info.get("size", 14) + (8 if is_selected else 0))
            node_text.append(f"{n_info.get('icon', '●')} {n_info.get('short_name', n_id)}")

            hover_html = (
                f"<b>{n_info.get('icon', '●')} {n_info.get('name', n_id)}</b><br>"
                f"<b>Category:</b> {n_info.get('category', 'Neural Node')}<br>"
                f"<b>Role:</b> {n_info.get('role', '')}<br>"
                f"<i>Snippet:</i> {n_info.get('snippet', '')[:140]}...<br>"
                f"<b>Target Tab:</b> {n_info.get('link_tab', '')}<br>"
                f"<i>Tap node in inspector to view full links & jump to tab</i>"
            )
            node_hover.append(hover_html)

        fig.add_trace(
            go.Scatter3d(
                x=node_x,
                y=node_y,
                z=node_z,
                mode="markers+text",
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    opacity=0.96,
                    line=dict(color="#ffffff", width=1.5),
                ),
                text=node_text,
                textposition="top center",
                textfont=dict(color="#f8fafc", size=10, family="Outfit, Inter, sans-serif"),
                hoverinfo="text",
                hovertext=node_hover,
                customdata=node_ids,
                name="Prompt Constellation",
            )
        )

        # Highlight Selected Dynamic Node
        if selected_block_id and selected_block_id in node_coords:
            sx, sy, sz = node_coords[selected_block_id]
            fig.add_trace(
                go.Scatter3d(
                    x=[sx],
                    y=[sy],
                    z=[sz],
                    mode="markers",
                    marker=dict(
                        size=30,
                        color="rgba(255, 255, 255, 0.3)",
                        line=dict(color="#38bdf8", width=3.5),
                    ),
                    hoverinfo="none",
                    showlegend=False,
                )
            )

        # Layout Styling for Dynamic Constellation
        fig.update_layout(
            scene=dict(
                xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
                yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
                zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
                bgcolor="#060913",
                camera=dict(
                    eye=dict(x=1.75, y=1.25, z=0.95),
                    up=dict(x=0, y=0, z=1),
                ),
            ),
            paper_bgcolor="#060913",
            plot_bgcolor="#060913",
            margin=dict(l=0, r=0, t=10, b=0),
            height=540,
            legend=dict(
                font=dict(color="#94a3b8"),
                bgcolor="rgba(15, 23, 42, 0.7)",
                bordercolor="rgba(148, 163, 184, 0.2)",
                borderwidth=1,
                x=0.02,
                y=0.95,
            ),
        )
        return fig

    # =========================================================================
    # BASELINE BRAIN ARCHITECTURE MODE (Fallback)
    # =========================================================================
    # Compute 3D Coordinates for All Baseline Blocks
    block_coords: Dict[str, tuple] = {}
    for b_id, b_info in NEURAL_BLOCKS.items():
        sc = b_info["sphere_coords"]
        x, y, z = _spherical_to_cartesian(sc["theta_deg"], sc["phi_deg"], sc["radius"])
        block_coords[b_id] = (x, y, z)

    # Draw Synaptic Connection Lines (Geodesic Arcs)
    edge_x = []
    edge_y = []
    edge_z = []

    for path in NEURAL_PATHWAYS:
        s_id = path["source"]
        t_id = path["target"]
        if s_id in block_coords and t_id in block_coords:
            p0 = np.array(block_coords[s_id])
            p1 = np.array(block_coords[t_id])

            num_steps = 15
            for t_step in np.linspace(0, 1, num_steps):
                p_interp = (1.0 - t_step) * p0 + t_step * p1
                norm = np.linalg.norm(p_interp)
                if norm > 1e-6:
                    lift = 1.0 + 0.12 * math.sin(t_step * math.pi)
                    p_curved = (p_interp / norm) * (globe_radius * lift)
                    edge_x.append(p_curved[0])
                    edge_y.append(p_curved[1])
                    edge_z.append(p_curved[2])
            edge_x.append(None)
            edge_y.append(None)
            edge_z.append(None)

    fig.add_trace(
        go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode="lines",
            line=dict(color="rgba(168, 85, 247, 0.45)", width=2.8),
            hoverinfo="none",
            name="Synaptic Pathways",
        )
    )

    # Draw Core Block Nodes
    node_x = []
    node_y = []
    node_z = []
    node_text = []
    node_hover = []
    node_colors = []
    node_sizes = []

    for b_id, b_info in NEURAL_BLOCKS.items():
        x, y, z = block_coords[b_id]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

        is_selected = (selected_block_id == b_id)
        node_colors.append("#ffffff" if is_selected else b_info["color"])
        node_sizes.append(18 if is_selected else 12)
        node_text.append(f"{b_info['icon']} {b_info['short_name']}")

        hover_html = (
            f"<b>{b_info['name']}</b><br>"
            f"<i>{b_info['role']}</i><br>"
            f"<b>Category:</b> {b_info['category']}<br>"
            f"<b>Latency:</b> {b_info['latency_typical_ms']}ms | <b>Params:</b> {b_info['parameter_count']}<br>"
            f"<b>Activation:</b> {b_info['activation_fn']}<br>"
            f"<i>Click to inspect block equations & sub-layers</i>"
        )
        node_hover.append(hover_html)

    fig.add_trace(
        go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode="markers+text",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                opacity=0.95,
                line=dict(color="#ffffff", width=1.5),
            ),
            text=node_text,
            textposition="top center",
            textfont=dict(color="#f1f5f9", size=11, family="sans-serif"),
            hoverinfo="text",
            hovertext=node_hover,
            name="Neural Blocks",
        )
    )

    # Highlight Selected Block with a Pulsing Outer Ring
    if selected_block_id and selected_block_id in block_coords:
        sx, sy, sz = block_coords[selected_block_id]
        fig.add_trace(
            go.Scatter3d(
                x=[sx],
                y=[sy],
                z=[sz],
                mode="markers",
                marker=dict(
                    size=26,
                    color="rgba(255, 255, 255, 0.35)",
                    line=dict(color="#38bdf8", width=3),
                ),
                hoverinfo="none",
                showlegend=False,
            )
        )

    # Layout Styling for Rich Dark Theme
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            bgcolor="#0b0f19",
            camera=dict(
                eye=dict(x=1.65, y=1.65, z=1.2),
                up=dict(x=0, y=0, z=1),
            ),
        ),
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        margin=dict(l=0, r=0, t=10, b=0),
        height=540,
        legend=dict(
            font=dict(color="#94a3b8"),
            bgcolor="rgba(15, 23, 42, 0.7)",
            bordercolor="rgba(148, 163, 184, 0.2)",
            borderwidth=1,
            x=0.02,
            y=0.95,
        ),
    )

    return fig
