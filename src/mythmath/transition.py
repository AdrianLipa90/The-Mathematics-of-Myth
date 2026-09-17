from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence


class RelationClass(str, Enum):
    ISOMORPHISM = "ISOMORPHISM"
    ORDER_HOMOMORPHISM = "ORDER_HOMOMORPHISM"
    ANALOGY = "ANALOGY"
    NUMBER_MATCH_ONLY = "NUMBER_MATCH_ONLY"
    INSUFFICIENT = "INSUFFICIENT"


class EvidenceTier(str, Enum):
    PRIMARY_CANONICAL = "PRIMARY_CANONICAL"
    ANCIENT_EXEGESIS = "ANCIENT_EXEGESIS"
    LATE_TRADITION_TEXT = "LATE_TRADITION_TEXT"
    LATER_RITUAL = "LATER_RITUAL"
    SCHOLARLY_SYNTHESIS = "SCHOLARLY_SYNTHESIS"
    MODERN_COMPARATIVE = "MODERN_COMPARATIVE"


@dataclass(frozen=True)
class EventStructure:
    """Finite ordered motif with typed state transitions.

    `states` are labels in temporal/order sequence.
    `transitions[i]` labels the edge states[i] -> states[i+1].
    """
    states: tuple[str, ...]
    transitions: tuple[str, ...]
    numeric_markers: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if len(self.states) < 1:
            raise ValueError("at least one state is required")
        if len(self.transitions) != max(0, len(self.states) - 1):
            raise ValueError("transitions must have len(states)-1 entries")


@dataclass(frozen=True)
class BoundarySchedule:
    """Projected schedule: N active steps followed by a typed boundary step.

    This deliberately ignores the narrative semantics before the boundary.
    It is therefore suitable only for testing a projected schedule relation,
    never for declaring two complete myths equivalent.
    """
    active_steps: int
    boundary_step: int
    boundary_type: str

    def __post_init__(self) -> None:
        if self.active_steps < 1:
            raise ValueError("active_steps must be positive")
        if self.boundary_step <= self.active_steps:
            raise ValueError("boundary_step must follow active_steps")
        if not self.boundary_type.strip():
            raise ValueError("boundary_type is required")


def classify_boundary_schedule(a: BoundarySchedule, b: BoundarySchedule) -> RelationClass:
    """Classify only the abstract active->boundary schedule.

    Same count, same boundary position, and same boundary semantics gives an
    isomorphism of the *projected schedule*. Same geometry but different
    semantics is only an order-homomorphism. A matching boundary number alone
    is not structural evidence.
    """
    same_geometry = (a.active_steps, a.boundary_step) == (b.active_steps, b.boundary_step)
    if same_geometry and a.boundary_type == b.boundary_type:
        return RelationClass.ISOMORPHISM
    if same_geometry:
        return RelationClass.ORDER_HOMOMORPHISM
    if a.boundary_step == b.boundary_step:
        return RelationClass.NUMBER_MATCH_ONLY
    return RelationClass.INSUFFICIENT


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

    Exact isomorphism here means equality of ordered transition signatures
    after forgetting state names. An order-homomorphism permits b to contain
    extra intermediate states while preserving a's transition sequence as an
    ordered subsequence. Shared semantic motifs alone are only analogy.
    A shared number with no structural preservation is NUMBER_MATCH_ONLY.
    """
    if a.transitions == b.transitions and len(a.states) == len(b.states):
        return RelationClass.ISOMORPHISM

    # ordered subsequence test on edge labels
    it = iter(b.transitions)
    if a.transitions and all(any(x == y for y in it) for x in a.transitions):
        return RelationClass.ORDER_HOMOMORPHISM

    shared_transition_types = set(a.transitions) & set(b.transitions)
    if shared_transition_types:
        return RelationClass.ANALOGY

    if set(a.numeric_markers) & set(b.numeric_markers):
        return RelationClass.NUMBER_MATCH_ONLY

    return RelationClass.INSUFFICIENT


def cycle_completion_time(phi0: float, omega: float) -> float:
    """First positive return time for uniform phase phi(t)=phi0+omega*t mod 2π."""
    import math
    if not math.isfinite(phi0) or not math.isfinite(omega):
        raise ValueError("finite phase and angular velocity required")
    if omega == 0:
        raise ValueError("omega must be nonzero")
    return 2.0 * math.pi / abs(omega)
