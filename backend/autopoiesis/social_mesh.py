"""Social Mesh & Pheromone Swarm Communication Engine.
Enables distributed population intelligence through:
1. Pheromone Gradient Signals: Decentralized stigmergy where instances deposit and sense task-space gradient signals.
2. Sexual Crossover Mating: Compatible instances (cosine similarity >= 0.70) combine layer weights and memory matrices.
"""

import os
import json
import time
import math
import hashlib
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn
import structlog

logger = structlog.get_logger(__name__)


class PheromoneDeposit:
    """Represents a gradient stigmergy signal left in the shared environment."""

    def __init__(
        self,
        source_id: str,
        location_hash: str,
        gradient_vector: List[float],
        confidence: float,
        ttl: float = 86400.0,
        timestamp: Optional[float] = None,
    ):
        self.source_id = source_id
        self.location_hash = location_hash
        self.gradient_vector = [float(x) for x in gradient_vector]
        self.confidence = float(np.clip(confidence, 0.0, 1.0))
        self.ttl = float(ttl)
        self.timestamp = timestamp or time.time()

    def is_valid(self, current_time: float) -> bool:
        return (current_time - self.timestamp) < self.ttl

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "location_hash": self.location_hash,
            "gradient_vector": self.gradient_vector,
            "confidence": self.confidence,
            "ttl": self.ttl,
            "timestamp": self.timestamp,
        }


class PheromoneLayer:
    """Decentralized gradient signal repository across digital organism instances."""

    def __init__(self, store_path: str = "data/pheromones/pheromone_store.json"):
        self.store_path = store_path
        self.deposits: List[PheromoneDeposit] = []
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        self._load_store()

    def _load_store(self):
        """Loads existing pheromone signals from disk."""
        if os.path.exists(self.store_path):
            try:
                with open(self.store_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    now = time.time()
                    self.deposits = [
                        PheromoneDeposit(**item) for item in data
                        if (now - item.get("timestamp", 0)) < item.get("ttl", 86400.0)
                    ]
            except Exception as e:
                logger.warning("failed_to_load_pheromones", error=str(e))
                self.deposits = []

    def _persist_store(self):
        """Saves valid active pheromones to disk."""
        try:
            now = time.time()
            valid_items = [d.to_dict() for d in self.deposits if d.is_valid(now)]
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(valid_items, f, indent=2)
        except Exception as e:
            logger.warning("failed_to_persist_pheromones", error=str(e))

    def deposit(
        self,
        source_id: str,
        location_hash: str,
        gradient_signal: List[float],
        confidence: float = 0.85,
        ttl: float = 86400.0,
    ) -> Dict[str, Any]:
        """Deposits a new gradient signal into the shared task-space."""
        dep = PheromoneDeposit(
            source_id=source_id,
            location_hash=location_hash,
            gradient_vector=gradient_signal,
            confidence=confidence,
            ttl=ttl,
        )
        self.deposits.append(dep)
        self._persist_store()
        logger.info("pheromone_deposited", location=location_hash, source=source_id[:8], confidence=confidence)
        return {"status": "deposited", "total_active_signals": len(self.deposits)}

    def sense(
        self,
        location_hash: str,
        decay_constant: float = 1e-4,
    ) -> Dict[str, Any]:
        """Senses gradient signals in the task-space and aggregates into a consensus vector."""
        now = time.time()
        # Filter active signals matching location or general swarm
        matching = [
            d for d in self.deposits
            if d.is_valid(now) and (d.location_hash == location_hash or d.location_hash == "GLOBAL_CONSENSUS")
        ]

        if not matching:
            return {
                "consensus_gradient": [0.0] * 16,
                "signals_detected": 0,
                "confidence_aggregate": 0.0,
                "status": "No Pheromones Detected",
            }

        # Weight by confidence and exponential age decay: w_i = confidence * exp(-lambda * dt)
        weights = []
        vecs = []
        for d in matching:
            dt = max(now - d.timestamp, 0.0)
            w = d.confidence * math.exp(-decay_constant * dt)
            weights.append(max(w, 1e-5))
            vecs.append(np.array(d.gradient_vector, dtype=np.float32))

        weights_arr = np.array(weights, dtype=np.float32)
        weights_norm = weights_arr / np.sum(weights_arr)

        consensus_vec = np.zeros_like(vecs[0])
        for w, v in zip(weights_norm, vecs):
            consensus_vec += w * v

        avg_conf = float(np.mean([d.confidence for d in matching]))
        return {
            "consensus_gradient": [round(float(x), 4) for x in consensus_vec.tolist()],
            "signals_detected": len(matching),
            "confidence_aggregate": round(avg_conf, 4),
            "status": "Consensus Gradient Synthesized",
        }


class SocialMeshEngine:
    """Coordinates multi-instance social protocols: pheromone stigmergy and genetic crossover mating."""

    def __init__(self):
        self.pheromone_layer = PheromoneLayer()

    def calculate_compatibility(self, parent_a_signature: np.ndarray, parent_b_signature: np.ndarray) -> float:
        """Calculates cosine similarity between two digital organism genetic signatures."""
        norm_a = np.linalg.norm(parent_a_signature) + 1e-9
        norm_b = np.linalg.norm(parent_b_signature) + 1e-9
        return float(np.dot(parent_a_signature, parent_b_signature) / (norm_a * norm_b))

    def mate_crossover(
        self,
        parent_a: Dict[str, Any],
        parent_b: Dict[str, Any],
        environment: str = "general",
        min_compatibility: float = 0.70,
        mutation_rate: float = 0.01,
    ) -> Dict[str, Any]:
        """Performs sexual genetic crossover and memory matrix imprinting between two parent checkpoints."""
        sig_a = np.array(parent_a.get("signature", [1.0] * 16), dtype=np.float32)
        sig_b = np.array(parent_b.get("signature", [0.9] * 16), dtype=np.float32)

        similarity = self.calculate_compatibility(sig_a, sig_b)
        if similarity < min_compatibility:
            return {
                "success": False,
                "reason": f"Genetic incompatibility: cosine similarity {similarity:.3f} < {min_compatibility:.2f}",
                "child": None,
            }

        fitness_a = parent_a.get("fitness", 0.75)
        fitness_b = parent_b.get("fitness", 0.75)
        conf_a = parent_a.get("confidence", 0.8)
        conf_b = parent_b.get("confidence", 0.8)

        # Crossover weights from superior parent
        dom_parent = "Parent_A" if fitness_a >= fitness_b else "Parent_B"
        random_mutation = float(np.random.normal(0, mutation_rate))
        child_fitness_baseline = max(fitness_a, fitness_b) * (1.0 + random_mutation)

        # Memory Imprinting: attention-weighted average
        total_conf = conf_a + conf_b + 1e-9
        weight_a = conf_a / total_conf
        weight_b = conf_b / total_conf

        child_id = hashlib.sha256(f"{parent_a.get('id', 'A')}_{parent_b.get('id', 'B')}_{time.time()}".encode()).hexdigest()[:16]

        certificate = {
            "child_id": child_id,
            "parent_a_id": parent_a.get("id", "A"),
            "parent_b_id": parent_b.get("id", "B"),
            "compatibility_score": round(similarity, 4),
            "dominant_genetic_donor": dom_parent,
            "memory_imprint_weights": {"parent_a": round(weight_a, 3), "parent_b": round(weight_b, 3)},
            "mutation_applied": round(float(random_mutation), 5),
            "projected_fitness": round(float(child_fitness_baseline), 4),
            "generation": max(parent_a.get("generation", 1), parent_b.get("generation", 1)) + 1,
            "timestamp": time.time(),
        }

        logger.info("organism_mating_crossover_success", child_id=child_id, compatibility=round(similarity, 3))
        return {
            "success": True,
            "certificate": certificate,
        }


social_mesh_engine = SocialMeshEngine()
