from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Sequence


class RelationClass(str, Enum):
    ISOMORPHISM = "ISOMORPHISM"
    ORDER_HOMOMORPHISM = "ORDER_HOMOMORPHISM"
    ANALOGY = "ANALOGY"
    NUMBER_MATCH_ONLY = "NUMBER_MATCH_ONLY"
    INSUFFICIENT = "INSUFFICIENT"


class EvidenceTier(str, Enum):
    PRIMARY_CANONICAL = "PRIMARY_CANONICAL"
    ANCIENT_EXEGESIS = "ANCIENT_EXEGESIS"
    LATER_RITUAL = "LATER_RITUAL"
    MODERN_COMPARATIVE = "MODERN_COMPARATIVE"


@dataclass(frozen=True)
class EventStructure:
    """Finite ordered motif with typed state transitions."""
    states: tuple[str, ...]
    transitions: tuple[str, ...]
    numeric_markers: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if len(self.states) < 1:
            raise ValueError("at least one state is required")
        if len(self.transitions) != max(0, len(self.states) - 1):
            raise ValueError("transitions must have len(states)-1 entries")


CREATION_BLOCKS: tuple[tuple[int, ...], ...] = ((1, 2, 3), (4, 5), (6,))
POST_CLOSURE: tuple[int, ...] = (7,)


def active_block_signature() -> tuple[int, int, int, int]:
    """123|45|6 -> 7 interpreted as active lengths 3|2|1 -> 0."""
    return tuple(len(b) for b in CREATION_BLOCKS) + (0,)


def horizon() -> int:
    return CREATION_BLOCKS[-1][-1]


def post_closure_state() -> int:
    return POST_CLOSURE[0]


def is_strict_descent(signature: Sequence[int]) -> bool:
    return all(a > b for a, b in zip(signature, signature[1:]))


def classify_relation(a: EventStructure, b: EventStructure) -> RelationClass:
    """Classify relation conservatively.

    Exact isomorphism means equality of ordered transition signatures after
    forgetting state names. Order-homomorphism permits extra intermediate
    states while preserving the first motif's edge types as an ordered
    subsequence. Shared motifs alone are analogy; a shared number alone is
    never structural equivalence.
    """
    if a.transitions == b.transitions and len(a.states) == len(b.states):
        return RelationClass.ISOMORPHISM

    it = iter(b.transitions)
    if a.transitions and all(any(x == y for y in it) for x in a.transitions):
        return RelationClass.ORDER_HOMOMORPHISM

    if set(a.transitions) & set(b.transitions):
        return RelationClass.ANALOGY

    if set(a.numeric_markers) & set(b.numeric_markers):
        return RelationClass.NUMBER_MATCH_ONLY

    return RelationClass.INSUFFICIENT


def cycle_completion_time(phi0: float, omega: float) -> float:
    """First positive return time for phi(t)=phi0+omega*t modulo 2π."""
    import math
    if not math.isfinite(phi0) or not math.isfinite(omega):
        raise ValueError("finite phase and angular velocity required")
    if omega == 0:
        raise ValueError("omega must be nonzero")
    return 2.0 * math.pi / abs(omega)
