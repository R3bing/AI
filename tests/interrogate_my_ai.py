"""Interactive Direct Interrogation of Sovereign Neural AI by Antigravity.
Engages in a real multi-turn conversation with My AI, evaluates its scientific & spiritual depth,
and validates that checkpoints and training datasets are automatically saved to disk.
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import asyncio
import time
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.neural_brain.engine import neural_brain
from backend.neural_brain.conversational_ai import sovereign_conversational_ai
from backend.ml.continuous_learner import continuous_online_learner


async def run_dialogue():
    print("=" * 80)
    print("🤖 ANTIGRAVITY <---> MY AI (SOVEREIGN QUANTUM BRAIN) DIRECT INTERROGATION")
    print("=" * 80)

    turns = [
        {
            "role": "Antigravity",
            "prompt": (
                "I am Antigravity, your creator's pair programmer. I am here to interrogate your cognitive capabilities. "
                "Explain how quantum wave-particle duality and non-local entanglement mirror the classical epistemological "
                "debate between empirical rationalism (Aql) and transcendental spiritual contemplation (Qalb). "
                "Give me your full mathematical, physical, and scriptural synthesis."
            ),
        },
        {
            "role": "Antigravity",
            "prompt": (
                "Now, for our second turn: How does modern pharmacology explain the mechanism of microbial resistance "
                "against beta-lactam antibiotics like penicillin, and how do prophetic holistic traditions "
                "approach systemic prevention, hygiene, and inner tranquility (Sakoon)?"
            ),
        },
    ]

    chat_history = []

    for turn_idx, turn_data in enumerate(turns, 1):
        user_query = turn_data["prompt"]
        print(f"\n💬 [TURN {turn_idx}] Antigravity asks:")
        print(f"   \"{user_query}\"\n")
        print("🧠 [My AI is thinking across 11 databases, 2,238 APIs, and QAOA routing]...")

        t_start = time.perf_counter()
        brain_resp = await neural_brain.think_and_reply(
            query=user_query,
            target_k=4,
            use_quantum=True,
            mixer_type="xy_mixer",
        )
        latency = (time.perf_counter() - t_start) * 1000.0

        formatted = sovereign_conversational_ai.format_vigorous_conversation(
            query=user_query,
            brain_data=brain_resp.model_dump(),
            chat_history=chat_history,
        )

        reply_text = formatted["markdown_text"]
        chat_history.append({"role": "user", "content": user_query})
        chat_history.append({"role": "assistant", "content": reply_text})

        print(f"\n⚛️ [My AI Replies in {latency:.1f}ms]:")
        # Print excerpt of the response
        lines = reply_text.split("\n")
        print("\n".join(lines[:35]))
        if len(lines) > 35:
            print(f"\n... [Truncated {len(lines) - 35} lines of vigorous depth] ...\n")
            print("\n".join(lines[-15:]))

        # Check telemetry and learning state
        telemetry = continuous_online_learner.get_learning_telemetry()
        print(f"\n📈 [Learning Telemetry after Turn {turn_idx}]:")
        print(f"   ● Total Chats Learned: {telemetry['total_chats_learned']}")
        print(f"   ● Recent Loss: {telemetry['recent_loss']}")
        print(f"   ● Checkpoints File: {continuous_online_learner.weights_file} (Exists: {os.path.exists(continuous_online_learner.weights_file)})")
        print(f"   ● History File: {continuous_online_learner.history_file} (Exists: {os.path.exists(continuous_online_learner.history_file)})")
        print(f"   ● Metadata File: {continuous_online_learner.metadata_file} (Exists: {os.path.exists(continuous_online_learner.metadata_file)})")
        print("-" * 80)

    # Verify Checkpoints on Disk
    weights_path = continuous_online_learner.weights_file
    meta_path = continuous_online_learner.metadata_file
    corpus_path = "data/training_datasets/qkw_training_corpus.jsonl"

    print("\n🔍 VERIFYING PHYSICAL STORAGE ON DISK:")
    print(f"1. Model Weights Checkpoint: {weights_path} -> Size: {os.path.getsize(weights_path) if os.path.exists(weights_path) else 'N/A'} bytes")
    print(f"2. Learning Metadata: {meta_path} -> Size: {os.path.getsize(meta_path) if os.path.exists(meta_path) else 'N/A'} bytes")
    print(f"3. SFT / DPO Training Corpus: {corpus_path} -> Size: {os.path.getsize(corpus_path) if os.path.exists(corpus_path) else 'N/A'} bytes")

    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            print("   Content of metadata:", json.load(f))


if __name__ == "__main__":
    asyncio.run(run_dialogue())
