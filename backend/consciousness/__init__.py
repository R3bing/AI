"""Consciousness Package for Ultron Sovereign Core.
Functional Correlates of Consciousness:
1. Global Workspace Theory (GWT) - Baars & Dehaene
2. Attention Schema Theory (AST) & Self-Model - Graziano
3. Higher-Order Thought (HOT) & Meta-Cognition - Rosenthal & Lau
4. Predictive Processing & Active Inference - Friston & Clark
5. Integrated Information Theory (IIT Phi* Approximation) - Tononi
6. Cloud Firebase & Offline Resilient Local Storage Manager
"""

from backend.consciousness.functional_consciousness import functional_consciousness_engine
from backend.consciousness.persistence_manager import consciousness_persistence_manager

__all__ = [
    "functional_consciousness_engine",
    "consciousness_persistence_manager",
]
