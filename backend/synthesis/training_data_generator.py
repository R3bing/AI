"""Training Data Generation and Model Distillation Hub for QKW.
Converts QKW multi-source grounded answers and raw AI completions into
Instruction-Tuning (SFT JSONL), DPO Preference Pairs, and ShareGPT datasets.
Users can inspect, download, and feed this data directly into Child Models for training.
"""

import json
import os
import time
from typing import Dict, List, Any, Optional

TRAINING_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "training_datasets"))
DEFAULT_DATASET_FILE = os.path.join(TRAINING_DATA_DIR, "qkw_training_corpus.jsonl")


class TrainingDataGenerator:
    """Manages synthetic & grounded training datasets for distilling knowledge into custom models."""

    def __init__(self, storage_path: str = DEFAULT_DATASET_FILE):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.memory_samples: List[Dict[str, Any]] = []
        self._load_existing_samples()

    def _load_existing_samples(self):
        """Loads previously saved training pairs from disk."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.memory_samples.append(json.loads(line))
            except Exception:
                pass

    def create_paired_sample(
        self,
        query: str,
        grounded_synthesis: str,
        citations: List[Dict[str, Any]],
        raw_ai_completion: Optional[str] = None,
        dominant_mode: str = "Aql & Qalb Balanced",
        entropy_score: float = 0.5,
    ) -> Dict[str, Any]:
        """Constructs a rich multi-format training entry from a query and response."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Baseline ungrounded completion if not provided
        fallback_raw = (
            raw_ai_completion
            if (raw_ai_completion and raw_ai_completion.strip())
            else f"Standard ungrounded generic answer for: {query}"
        )

        citation_sources = [c.get("source_name", "Unknown") for c in citations]

        sample = {
            "id": f"sample_{len(self.memory_samples) + 1}_{int(time.time())}",
            "timestamp": timestamp,
            "query": query,
            "grounded_synthesis": grounded_synthesis,
            "raw_ai_completion": fallback_raw,
            "citations_count": len(citations),
            "citation_sources": list(set(citation_sources)),
            "dominant_mode": dominant_mode,
            "entropy_score": entropy_score,
            # 1. Supervised Fine-Tuning Format (Alpaca / OpenAI)
            "sft_alpaca": {
                "instruction": query,
                "input": f"Grounding Repositories: {', '.join(set(citation_sources))}" if citation_sources else "",
                "output": grounded_synthesis,
            },
            # 2. Direct Preference Optimization (DPO) Pair
            "dpo_pair": {
                "prompt": query,
                "chosen": grounded_synthesis,
                "rejected": fallback_raw,
                "margin": 1.0,
            },
            # 3. ShareGPT Multi-turn Format
            "sharegpt": {
                "conversations": [
                    {"from": "human", "value": query},
                    {"from": "gpt", "value": grounded_synthesis},
                ]
            },
        }

        # Persist to disk
        self.memory_samples.append(sample)
        try:
            with open(self.storage_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(sample) + "\n")
        except Exception:
            pass

        return sample

    def get_samples(self) -> List[Dict[str, Any]]:
        """Returns all accumulated training samples."""
        return self.memory_samples

    def export_as_jsonl(self, format_type: str = "sft") -> str:
        """Exports the dataset into requested format as a JSONL string."""
        lines = []
        for s in self.memory_samples:
            if format_type == "sft":
                lines.append(json.dumps(s.get("sft_alpaca", {})))
            elif format_type == "dpo":
                lines.append(json.dumps(s.get("dpo_pair", {})))
            elif format_type == "sharegpt":
                lines.append(json.dumps(s.get("sharegpt", {})))
            else:
                lines.append(json.dumps(s))
        return "\n".join(lines)

    def clear_dataset(self):
        """Clears in-memory and disk dataset."""
        self.memory_samples.clear()
        if os.path.exists(self.storage_path):
            try:
                os.remove(self.storage_path)
            except Exception:
                pass

    def get_statistics(self) -> Dict[str, Any]:
        """Returns dataset volume and diversity telemetry."""
        total = len(self.memory_samples)
        all_sources = set()
        for s in self.memory_samples:
            all_sources.update(s.get("citation_sources", []))

        return {
            "total_samples": total,
            "storage_file": self.storage_path,
            "unique_grounding_sources": list(all_sources),
            "formats_supported": ["SFT (Alpaca/OpenAI)", "DPO Preference Pairs", "ShareGPT"],
        }


training_data_generator = TrainingDataGenerator()
