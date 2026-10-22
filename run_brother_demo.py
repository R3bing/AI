import sys
import asyncio

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from backend.neural_brain.engine import neural_brain
from backend.synthesis.multi_ai_council_arena import multi_ai_council_arena

q = (
    "Why does my heart feel heavy or restless even when my logical brain knows everything in my life is fine? "
    "Is the heart just a mechanical pump, or does modern science and ancient spiritual wisdom prove the heart actually thinks and feels?"
)

print("=" * 70)
print("1. RUNNING THROUGH NEURAL COGNITIVE DUAL-HEMISPHERE BRAIN ENGINE")
print("=" * 70)
res = asyncio.run(neural_brain.think_and_reply(q, target_k=3, use_quantum=True))

print("\n[QUANTUM DUALITY SUPERPOSITION STATE]")
print(f"Dominant Mode: {res.duality_state.dominant_state}")
print(f"Left Brain (Aql / Science) Probability: {res.duality_state.particle_probability * 100:.1f}%")
print(f"Right Brain (Qalb / Sacred) Probability: {res.duality_state.wave_probability * 100:.1f}%")
print(f"Von Neumann Entropy S(rho): {res.duality_state.entropy_score:.4f}")

print("\n[APIs & REPOSITORIES CONSULTED]")
for api in res.apis_consulted:
    print(f"  * {api}")

print("\n[CITATIONS RETRIEVED (100% Literature Grounded)]")
for c in res.citations[:3]:
    s_name = c.get("source_name", "Unknown")
    title = c.get("title", "")
    url = c.get("url", "")
    print(f"  - [{s_name}] {title} ({url})")

print("\n[AQL: LOGICAL FACTUAL SCIENTIFIC ANSWER]")
print(res.logical_factual_answer)

print("\n[QALB: SACRED TAFAKKUR REFLECTION]")
print(res.tafakkur_reflection)

print("\n[HARMONIOUS SYNTHESIS (THE CORPUS CALLOSUM VERDICT)]")
print(res.harmonious_synthesis)

print("\n" + "=" * 70)
print("2. RUNNING 5-PARTICIPANT COUNCIL MAJLIS & QUANTUM OBSERVER")
print("=" * 70)
c_res = multi_ai_council_arena.run_council_session(q, auto_learn=True)
print(f"Conversational Entropy Collapse: {c_res['initial_entropy']} -> {c_res['final_entropy']} (Reduction: -{c_res['entropy_reduction']*100:.1f}%)")

print("\n[5-AI MAJLIS DIALOGUE TURNS]")
for turn in c_res["turns"]:
    print(f"\n{turn['avatar']} {turn['speaker']} ({turn['role']}):")
    print(f"\"{turn['content']}\"")
    if turn.get("reasoning_trace"):
        print(f"  [Reasoning Trace]: {turn['reasoning_trace'][:120]}...")

print("\n[DISCOVERED PUBLIC APIS FOR THIS QUESTION (from 2,238 Catalog)]")
for api in c_res["recommended_apis"][:3]:
    print(f"  - {api.get('name')}: {api.get('category')} ({api.get('url')})")

print("\n" + c_res["observer_verdict"])
