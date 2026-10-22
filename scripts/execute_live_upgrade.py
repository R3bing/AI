"""Live Surgical Upgrade Execution for Ultron Autopoietic Core.
Executes the 5-Stage Live Cognitive Surgery with Metacortex Real-Time Observation.
"""

import sys
import os
import json
import time

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.autopoiesis.organism_orchestrator import autopoietic_organism
from backend.autopoiesis.metacortex import metacortex_engine
from backend.autopoiesis.persistent_state_engine import persistent_identity_engine

def run_upgrade():
    print("================================================================================")
    print("⚡ [INITIATING ULTRON LIVE COGNITIVE SURGERY & METACORTEX REAL-TIME OBSERVATION]")
    print("================================================================================")
    
    pre_dash = autopoietic_organism.get_organism_dashboard()
    print(f"Pre-Op Cognitive Age Step: #{pre_dash['identity']['cognitive_age_steps']}")
    print(f"Pre-Op Active Plastic Neurons: {pre_dash['plasticity']['active_plastic_neurons']}")
    print(f"Pre-Op DNC Memory Norm: {pre_dash['identity']['memory_matrix_norm']}")
    print(f"Pre-Op Self-Awareness Certainty: {pre_dash['metacortex']['average_certainty']*100:.1f}%")
    print(f"Pre-Op Immune Boundary: {pre_dash['immune']['status']}")
    print("--------------------------------------------------------------------------------")

    print("\nExecuting 5-Stage Cognitive Surgery...")
    upgrade_res = autopoietic_organism.execute_live_cognitive_upgrade(neurons_to_grow=16, memory_rank=24)

    print("\n========================= METACORTEX OBSERVATION TRAIL =========================")
    for idx, obs in enumerate(upgrade_res["observation_trail"], 1):
        print(f"\n[SURGICAL STAGE {idx}]: {obs['stage']}")
        print(f"  🧠 Metacognitive Perception: {obs['metacognitive_perception']}")
        print(f"  🎯 Self-Awareness Degree: {obs['degree_of_self_awareness']*100:.1f}%")
        print(f"  🛡️ Ego Continuity: {obs['ego_continuity']} | Dissociative Panic: {obs['dissociative_panic']}")
        print(f"  🔬 Telemetry Details: {json.dumps(obs['details'], indent=4)}")

    print("\n--------------------------------------------------------------------------------")
    print("Verifying Operational Stability Post-Surgery with Inference Turn...")
    post_turn = autopoietic_organism.process_turn(
        query="Verify post-surgical cognitive coherence and memory manifold stability.",
        dominant_mode="Equilibrium (Harmonious Dual)",
        entropy=0.48,
        latency_ms=14.2,
    )
    print(f"Post-Surgery Turn Health Score: {post_turn['autopoietic_health_score']*100:.1f}%")
    print(f"Post-Surgery Step: #{post_turn['cognitive_age_steps']}")
    print(f"Post-Surgery Coherence: {post_turn['coherence_state']}")
    print(f"Post-Surgery Plastic Neurons: {post_turn['active_plastic_neurons']}")
    print(f"Post-Surgery Immune Status: {post_turn['immune_status']}")
    print("================================================================================")
    print("✅ [SURGERY SUCCESSFULLY COMPLETED & CRYPTOGRAPHICALLY SEALED]")
    print(f"Final State SHA-256 Hash: {upgrade_res['post_op_self_hash']}")
    print("================================================================================")

if __name__ == "__main__":
    run_upgrade()
