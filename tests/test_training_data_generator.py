"""Unit tests for Training Data Generator and Dataset Distillation."""

import json
import pytest
from backend.synthesis.training_data_generator import TrainingDataGenerator
from backend.nas.trainer import DatasetFactory


def test_create_paired_training_sample(tmp_path):
    storage_file = str(tmp_path / "test_corpus.jsonl")
    generator = TrainingDataGenerator(storage_path=storage_file)

    query = "How does quantum entanglement relate to spiritual harmony?"
    grounded = "Quantum entanglement demonstrates non-local correlation across distant states."
    raw_ai = "Quantum entanglement is a physics concept where particles interact."
    citations = [
        {"source_name": "arXiv", "title": "Bell Non-Locality Review"},
        {"source_name": "OpenAlex", "title": "Quantum Foundations"},
    ]

    sample = generator.create_paired_sample(
        query=query,
        grounded_synthesis=grounded,
        citations=citations,
        raw_ai_completion=raw_ai,
    )

    assert sample["query"] == query
    assert sample["grounded_synthesis"] == grounded
    assert "sft_alpaca" in sample
    assert sample["sft_alpaca"]["instruction"] == query
    assert sample["sft_alpaca"]["output"] == grounded

    # DPO pair verification
    assert "dpo_pair" in sample
    assert sample["dpo_pair"]["chosen"] == grounded
    assert sample["dpo_pair"]["rejected"] == raw_ai

    # ShareGPT verification
    assert "sharegpt" in sample
    assert len(sample["sharegpt"]["conversations"]) == 2

    # JSONL Export verification
    sft_export = generator.export_as_jsonl("sft")
    assert len(sft_export.split("\n")) == 1
    loaded_sft = json.loads(sft_export)
    assert loaded_sft["instruction"] == query

    dpo_export = generator.export_as_jsonl("dpo")
    loaded_dpo = json.loads(dpo_export)
    assert loaded_dpo["chosen"] == grounded


def test_dataset_factory_from_training_bank(tmp_path):
    storage_file = str(tmp_path / "test_bank.jsonl")
    generator = TrainingDataGenerator(storage_path=storage_file)

    for i in range(5):
        generator.create_paired_sample(
            query=f"Query {i} about quantum physics and philosophy",
            grounded_synthesis=f"Grounded response {i}",
            citations=[{"source_name": "arXiv", "title": f"Paper {i}"}],
        )

    # Monkeypatch generator into factory test
    from backend.synthesis import training_data_generator
    orig_gen = training_data_generator.training_data_generator
    training_data_generator.training_data_generator = generator

    try:
        train_loader, val_loader = DatasetFactory.get_dataset_from_training_bank(
            input_dim=32,
            num_classes=4,
        )
        assert len(train_loader) > 0
        batch_x, batch_y = next(iter(train_loader))
        assert batch_x.shape[1] == 32
    finally:
        training_data_generator.training_data_generator = orig_gen
