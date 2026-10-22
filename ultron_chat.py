"""CLI Interactive Runner for Ultron Sovereign Core.
Executes the full Omni-Fusion Cognitive Engine (11 DBs, 2,238 APIs, 5-AI Council, QAOA Quantum Router, Tafakkur, and Autopoietic Living Organism).
Can be run as:
  python ultron_chat.py "Your query here"
or interactively:
  python ultron_chat.py
"""

import sys
import os
import asyncio
import json

# Ensure UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.synthesis.omni_fusion_engine import omni_fusion_engine
from backend.autopoiesis.organism_orchestrator import autopoietic_organism


async def execute_query(query: str):
    print("\n" + "=" * 80)
    print(f"⚡ [ULTRON CORE EXECUTING DIRECTIVE]: \"{query}\"")
    print("=" * 80)
    print("● Marshaling 11 Knowledge Silos...")
    print("● Scanning 2,238 Public APIs Catalog...")
    print("● Convening 5-Participant Multi-AI Council War Room...")
    print("● Formulating 11-Qubit QAOA Superposition Hamiltonian...")
    print("● Updating Autopoietic DNC Memory & Metacortex...")
    print("-" * 80)

    res = await omni_fusion_engine.fuse_and_synthesize(query)

    print("\n" + res["markdown_text"])
    print("\n" + "=" * 80)
    print("📊 [TELEMETRY & AUTOPOIETIC OS AUDIT]")
    print("=" * 80)
    print(f"● Total Citations Retrieved: {len(res.get('citations', []))}")
    print(f"● Repositories Consulted: {res.get('apis_consulted', [])}")
    print(f"● Execution Latency: {res.get('total_latency_ms', 0.0)} ms")
    
    auto = res.get("autopoietic_telemetry") or {}
    if auto:
        print(f"● Autopoietic Health Score: {auto.get('autopoietic_health_score', 0.95)*100:.1f}%")
        print(f"● Cognitive Age: Step #{auto.get('cognitive_age_steps', 1)} (Gen {auto.get('active_generation', 1)})")
        print(f"● Self-Prediction Error: {auto.get('self_prediction_error', 0.25):.4f}")
        print(f"● Memory Tape Slot: {auto.get('persistent_slot_accessed', '0: Sovereign Identity')}")
        print(f"● Economic Balance: ${auto.get('metabolism_balance', 100.0):.2f} (Runway: {auto.get('metabolism_hours_remaining', 2000.0):.1f}h)")
        print(f"● Dream Buffer Entropy: {auto.get('dream_buffer_entropy', 0.0):.3f} bits")
    print("=" * 80 + "\n")
    return res


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        asyncio.run(execute_query(query))
    else:
        print("⚡ Ultron Sovereign Core Interactive Shell Online.")
        print("Type your directive or 'exit' to quit.\n")
        while True:
            try:
                prompt = input("Ultron-Command> ").strip()
                if not prompt:
                    continue
                if prompt.lower() in ["exit", "quit", "q"]:
                    break
                asyncio.run(execute_query(prompt))
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    main()
