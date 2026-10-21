"""Neural Architecture Search (NAS) & Controller AI Module.
Contains the Controller AI Meta-Designer, Search Space definitions,
and Architecture Sampling strategies.
"""

from backend.nas.models import (
    BlockType,
    ActivationType,
    NormType,
    SearchStrategy,
    BlockSpec,
    Hyperparameters,
    ArchitectureCandidate,
    ArchitectureProposalRequest,
)
from backend.nas.search_space import search_space, SearchSpace
from backend.nas.controller import controller_ai, ControllerAI

__all__ = [
    "BlockType",
    "ActivationType",
    "NormType",
    "SearchStrategy",
    "BlockSpec",
    "Hyperparameters",
    "ArchitectureCandidate",
    "ArchitectureProposalRequest",
    "search_space",
    "SearchSpace",
    "controller_ai",
    "ControllerAI",
]
