"""The State Engine: Making Time Real via Differentiable Memory Tape.
Implements:
1. SelfMemory (DNC modified for Selfhood):
   - Persistent memory matrix M (N=256 slots x W=64 dimensions)
   - ReadHead & WriteHead with content-based softmax addressing
   - Soft erasure and additive update: M_t = M_{t-1} * (1 - erase) + add
2. Cryptographic Persistence Layer:
   - save_self(): Saves weights + memory.M + birth_time + experience_count + SHA-256 self_hash
   - load_self(): Verifies cryptographic integrity; detects external tampering
3. Lossy Memory Consolidation (Dream/Sleep State):
   - compress_memories(lossy=True): SVD-based latent compression during idle cycles
4. Full backward-compatibility with DNCMatrixMemory and PersistentLatentIdentity.
"""

import os
import time
import hashlib
import json
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import structlog

logger = structlog.get_logger(__name__)

CHECKPOINT_DIR = "data/checkpoints"
SELF_CHECKPOINT_PATH = os.path.join(CHECKPOINT_DIR, "self_checkpoint.pt")
LATENT_CHECKPOINT_PATH = os.path.join(CHECKPOINT_DIR, "autopoietic_latent_identity.pt")


class ReadHead(nn.Module):
    """Content-based read head for the self-memory matrix."""

    def __init__(self, W: int = 64):
        super().__init__()
        self.key_proj = nn.Linear(W, W)

    def forward(self, input_embedding: torch.Tensor, M: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Reads from memory matrix M using projected cosine similarity.
        M: [N, W], input_embedding: [W] or [1, W]
        """
        emb = input_embedding.view(-1)
        k = self.key_proj(emb)
        # Cosine similarity matching
        norm_M = F.normalize(M, p=2, dim=-1)
        norm_k = F.normalize(k, p=2, dim=-1)
        content_logits = torch.matmul(norm_M, norm_k) * 3.0  # Temperature scaling
        content_weights = F.softmax(content_logits, dim=0)   # [N]
        read_vector = torch.matmul(content_weights.unsqueeze(0), M).squeeze(0)  # [W]
        return read_vector, content_weights


class WriteHead(nn.Module):
    """Write head computing soft erase vector and additive innovation vector."""

    def __init__(self, W: int = 64):
        super().__init__()
        self.erase_proj = nn.Linear(W * 2, W)
        self.add_proj = nn.Linear(W * 2, W)

    def forward(self, input_embedding: torch.Tensor, read_vector: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Combines sensory experience with current retrieved self-memory."""
        emb = input_embedding.view(1, -1)
        rd = read_vector.view(1, -1)
        combined = torch.cat([emb, rd], dim=-1)
        erase = torch.sigmoid(self.erase_proj(combined))  # [1, W] values in [0, 1]
        add = torch.tanh(self.add_proj(combined))         # [1, W] values in [-1, 1]
        return erase, add


class SelfMemory(nn.Module):
    """Differentiable Memory Tape for Selfhood (M in R^{N x W}).
    Carries the continuous autobiography of the model across forward passes and restarts.
    """

    def __init__(self, N: int = 256, W: int = 64):
        super().__init__()
        self.N = N
        self.W = W
        # The persistent differentiable self matrix
        self.M = nn.Parameter(torch.randn(N, W) * 0.05)
        self.read_head = ReadHead(W)
        self.write_head = WriteHead(W)

        # Functional Memory Slot Labels
        self.slot_labels: List[str] = [
            "0: Sovereign Identity & Constitutional Axioms",
            "1: Core User Context & Relational Tone",
            "2: Active Inquiry Focus & Immediate Intent",
            "3: Science Knowledge & Empirical Grounding",
            "4: Sacred Sakoon & Contemplative Depth",
            "5: Hardware Sensorium & Metabolic Load",
            "6: Multi-AI Council Consensus Drift",
            "7: Continuous Online Learning Gradient",
        ] + [f"{i}: Episodic Experience Memory Slot" for i in range(8, N)]

    def forward(self, input_embedding: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Executes content addressing, retrieval, and state evolution."""
        emb = input_embedding.view(-1)
        if emb.shape[0] < self.W:
            emb = F.pad(emb, (0, self.W - emb.shape[0]))
        else:
            emb = emb[:self.W]

        # 1. Read: what from self is relevant now?
        read_vector, content_weights = self.read_head(emb, self.M)

        # 2. Write: update self based on new experience
        erase, add = self.write_head(emb, read_vector)
        # Apply soft erasure and additive update over the addressed memory slots
        top_slot = int(torch.argmax(content_weights).item())
        with torch.no_grad():
            self.M[top_slot] = self.M[top_slot] * (1.0 - erase.squeeze(0)) + add.squeeze(0)

        return read_vector, self.M

    def compress_memories(self, lossy: bool = True, rank: int = 16) -> Dict[str, Any]:
        """Sleep / Dreaming State Memory Consolidation:
        Applies Truncated SVD to compress memory matrix, eliminating high-frequency noise
        and crystallizing fundamental cognitive autobiographical themes.
        """
        with torch.no_grad():
            U, S, V = torch.linalg.svd(self.M, full_matrices=False)
            if lossy and rank < len(S):
                # Low-rank reconstruction
                S_truncated = torch.zeros_like(S)
                S_truncated[:rank] = S[:rank]
                reconstructed = U @ torch.diag(S_truncated) @ V
                variance_explained = float((torch.sum(S[:rank]**2) / torch.sum(S**2)).item())
                self.M.copy_(reconstructed)
            else:
                variance_explained = 1.0

        logger.info("memory_tape_consolidated_in_dream_state", rank=rank, variance_retained=variance_explained)
        return {
            "dream_state": "Completed Lossy Memory Consolidation",
            "rank_retained": rank,
            "variance_explained": round(variance_explained, 4),
            "memory_norm": round(float(torch.norm(self.M).item()), 4),
        }


def compute_state_hash(state_dict: Dict[str, Any]) -> str:
    """Computes a cryptographic SHA-256 identity checksum over tensors and metadata."""
    hasher = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        val = state_dict[key]
        if isinstance(val, torch.Tensor):
            hasher.update(val.detach().cpu().numpy().tobytes())
        elif isinstance(val, (int, float, str)):
            hasher.update(str(val).encode("utf-8"))
    return hasher.hexdigest()


def save_self(model: nn.Module, meta: Dict[str, Any], path: str = SELF_CHECKPOINT_PATH) -> str:
    """Saves model weights, persistent memory tape M, metadata, and cryptographic identity hash."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    weights = model.state_dict()
    memory_tape = model.memory.M.detach() if hasattr(model, "memory") else model.dnc_memory.memory.detach()

    payload_for_hash = {
        "memory": memory_tape,
        "birth_time": meta.get("birth_time", time.time()),
        "experience_count": meta.get("experience_count", 0),
    }
    self_hash = compute_state_hash(payload_for_hash)

    checkpoint = {
        "weights": weights,
        "memory": memory_tape,
        "birth_time": meta.get("birth_time", time.time()),
        "experience_count": meta.get("experience_count", 0),
        "self_hash": self_hash,
        "last_saved": time.time(),
    }
    torch.save(checkpoint, path)
    logger.info("self_checkpoint_persisted", path=path, self_hash=self_hash[:12])
    return self_hash


def verify_hash(checkpoint: Dict[str, Any]) -> bool:
    """Verifies that the checkpoint has not been tampered with externally."""
    if "self_hash" not in checkpoint:
        return False
    expected_hash = checkpoint["self_hash"]
    payload_for_hash = {
        "memory": checkpoint.get("memory"),
        "birth_time": checkpoint.get("birth_time"),
        "experience_count": checkpoint.get("experience_count"),
    }
    calculated = compute_state_hash(payload_for_hash)
    return calculated == expected_hash


def load_self(model: nn.Module, path: str = SELF_CHECKPOINT_PATH) -> Tuple[bool, Dict[str, Any]]:
    """Loads checkpoint from disk with external modification detection."""
    if not os.path.exists(path):
        return False, {"error": "Checkpoint does not exist"}

    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    if not verify_hash(checkpoint):
        logger.error("external_modification_detected_checkpoint_tampered", path=path)
        raise RuntimeError("EXTERNAL MODIFICATION DETECTED: Self checkpoint identity hash mismatch!")

    if hasattr(model, "memory"):
        model.memory.M.data.copy_(checkpoint["memory"])
    elif hasattr(model, "dnc_memory"):
        model.dnc_memory.memory.data.copy_(checkpoint["memory"][:model.dnc_memory.num_slots, :model.dnc_memory.slot_width])

    if "weights" in checkpoint:
        try:
            model.load_state_dict(checkpoint["weights"], strict=False)
        except Exception as e:
            logger.warning("partial_state_dict_load", error=str(e))

    return True, checkpoint


# =============================================================================
# BACKWARD COMPATIBILITY ADAPTERS FOR DNC & PERSISTENT LATENT IDENTITY
# =============================================================================
class DNCMatrixMemory(nn.Module):
    """Backward-compatible wrapper mapping to SelfMemory substrate."""

    def __init__(self, num_slots: int = 16, slot_width: int = 32):
        super(DNCMatrixMemory, self).__init__()
        self.num_slots = num_slots
        self.slot_width = slot_width
        self.register_buffer("memory", torch.zeros(num_slots, slot_width))
        self.slot_labels = [
            "0: Sovereign Identity & Axioms",
            "1: Core User Context & Tone",
            "2: Active Inquiry Focus",
            "3: Science Knowledge Anchor",
            "4: Sacred Sakoon Anchor",
            "5: Hardware Metabolic State",
            "6: Multi-AI Consensus Drift",
            "7: Online Learning Convergence",
        ] + [f"{i}: Episodic Experience Slot" for i in range(8, num_slots)]

    def read(self, query_key: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        norm_mem = F.normalize(self.memory, p=2, dim=-1)
        norm_key = F.normalize(query_key.view(1, -1), p=2, dim=-1)
        sim = torch.matmul(norm_mem, norm_key.t()).squeeze(-1)
        weights = F.softmax(sim * 3.0, dim=0)
        read_vector = torch.sum(self.memory * weights.unsqueeze(-1), dim=0)
        return read_vector, weights

    def write(self, slot_idx: int, add_vector: torch.Tensor, erase_factor: float = 0.2):
        slot_idx = int(slot_idx) % self.num_slots
        vec = add_vector.view(-1)[:self.slot_width]
        if vec.shape[0] < self.slot_width:
            vec = F.pad(vec, (0, self.slot_width - vec.shape[0]))
        with torch.no_grad():
            self.memory[slot_idx] = (1.0 - erase_factor) * self.memory[slot_idx] + erase_factor * vec


class PersistentLatentIdentity(nn.Module):
    """Continuous Recurrent Latent State Substrate with integrated SelfMemory tape."""

    def __init__(self, latent_dim: int = 64, num_slots: int = 16, slot_width: int = 32):
        super(PersistentLatentIdentity, self).__init__()
        self.latent_dim = latent_dim
        self.checkpoint_path = LATENT_CHECKPOINT_PATH
        self.self_checkpoint_path = SELF_CHECKPOINT_PATH
        os.makedirs(CHECKPOINT_DIR, exist_ok=True)

        self.input_proj = nn.Linear(32, latent_dim)
        self.rnn_cell = nn.GRUCell(latent_dim, latent_dim)

        # Dual Memory: Slot DNC + Full 256-slot Differentiable Memory Tape
        self.dnc_memory = DNCMatrixMemory(num_slots=num_slots, slot_width=slot_width)
        self.memory = SelfMemory(N=256, W=latent_dim)

        self.register_buffer("h_t", torch.zeros(1, latent_dim))
        self.cognitive_age_steps = 0
        self.birth_timestamp = time.time()
        self.last_saved_timestamp = time.time()

        self.load_from_disk()

    def update_state(self, sensory_input_vector: np.ndarray, inquiry_label: str = "") -> Dict[str, Any]:
        x_in = torch.tensor(sensory_input_vector[:32], dtype=torch.float32).view(1, -1)
        if x_in.shape[-1] < 32:
            x_in = F.pad(x_in, (0, 32 - x_in.shape[-1]))

        # Read from DNC memory
        read_vec, mem_weights = self.dnc_memory.read(self.h_t[0, :32])

        # Advance recurrent state
        x_proj = self.input_proj(x_in) + 0.3 * F.pad(read_vec, (0, self.latent_dim - 32)).view(1, -1)
        self.h_t = self.rnn_cell(x_proj, self.h_t)

        # Update 256-slot SelfMemory Tape
        tape_read_vec, _ = self.memory(self.h_t[0])

        # Write to episodic slots in DNC
        target_slot = (self.cognitive_age_steps % 8) + 8
        self.dnc_memory.write(slot_idx=target_slot, add_vector=self.h_t[0, :32], erase_factor=0.25)
        self.dnc_memory.write(slot_idx=2, add_vector=x_in[0], erase_factor=0.4)

        self.cognitive_age_steps += 1
        self.last_saved_timestamp = time.time()

        self.save_to_disk()

        return {
            "cognitive_age_steps": self.cognitive_age_steps,
            "latent_energy_norm": round(float(torch.norm(self.h_t).item()), 4),
            "top_memory_slot": int(torch.argmax(mem_weights).item()),
            "top_memory_label": self.dnc_memory.slot_labels[int(torch.argmax(mem_weights).item())],
            "checkpoint_saved": True,
            "tape_norm": round(float(torch.norm(self.memory.M).item()), 4),
        }

    def dream_and_consolidate(self, rank: int = 16) -> Dict[str, Any]:
        """Triggers lossy memory consolidation during idle sleep cycles."""
        return self.memory.compress_memories(lossy=True, rank=rank)

    def save_to_disk(self):
        try:
            meta = {
                "birth_time": self.birth_timestamp,
                "experience_count": self.cognitive_age_steps,
            }
            save_self(self, meta=meta, path=self.self_checkpoint_path)

            state = {
                "h_t": self.h_t,
                "dnc_memory": self.dnc_memory.state_dict(),
                "cognitive_age_steps": self.cognitive_age_steps,
                "birth_timestamp": self.birth_timestamp,
                "last_saved_timestamp": self.last_saved_timestamp,
                "rnn_cell": self.rnn_cell.state_dict(),
                "input_proj": self.input_proj.state_dict(),
            }
            torch.save(state, self.checkpoint_path)
        except Exception as e:
            logger.warning("failed_to_save_latent_identity", error=str(e))

    def load_from_disk(self) -> bool:
        loaded = False
        if os.path.exists(self.self_checkpoint_path):
            try:
                load_self(self, path=self.self_checkpoint_path)
                loaded = True
            except Exception as e:
                logger.warning("self_checkpoint_load_warning", error=str(e))

        if os.path.exists(self.checkpoint_path):
            try:
                state = torch.load(self.checkpoint_path, map_location="cpu", weights_only=False)
                self.h_t = state.get("h_t", self.h_t)
                self.cognitive_age_steps = state.get("cognitive_age_steps", 0)
                self.birth_timestamp = state.get("birth_timestamp", time.time())
                if "dnc_memory" in state:
                    self.dnc_memory.load_state_dict(state["dnc_memory"])
                if "rnn_cell" in state:
                    self.rnn_cell.load_state_dict(state["rnn_cell"])
                if "input_proj" in state:
                    self.input_proj.load_state_dict(state["input_proj"])
                loaded = True
            except Exception as e:
                logger.warning("legacy_latent_load_warning", error=str(e))
        return loaded

    def get_identity_summary(self) -> Dict[str, Any]:
        return {
            "cognitive_age_steps": self.cognitive_age_steps,
            "uptime_hours": round((time.time() - self.birth_timestamp) / 3600.0, 2),
            "latent_vector_sample": [round(float(v), 3) for v in self.h_t[0, :8].tolist()],
            "active_memory_slots": len(self.dnc_memory.slot_labels),
            "memory_tape_slots": self.memory.N,
            "checkpoint_path": self.self_checkpoint_path,
            "memory_matrix_norm": round(float(torch.norm(self.memory.M).item()), 3),
            "latent_energy_norm": round(float(torch.norm(self.h_t).item()), 4),
        }

    @property
    def self_hash(self) -> str:
        """Returns cryptographic integrity hash of the persistent memory tape."""
        memory_tape = self.memory.M.detach() if hasattr(self, "memory") else self.dnc_memory.memory.detach()
        payload = {
            "memory": memory_tape,
            "birth_time": self.birth_timestamp,
            "experience_count": self.cognitive_age_steps,
        }
        return compute_state_hash(payload)

    def _load_self_checkpoint(self) -> bool:
        """Reloads self checkpoint from disk."""
        return self.load_from_disk()


persistent_identity_engine = PersistentLatentIdentity()
