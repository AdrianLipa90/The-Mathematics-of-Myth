"""Executable relational-state formalism for Enuma Elish.

This module formalizes narrative structure. It does not identify mythic entities
with physical fields, particles, hardware, or cosmological observables.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EpistemicLayer(str, Enum):
    TEXT = "TEXT"
    FORMALIZATION = "FORMALIZATION"
    PHYSICAL_HYPOTHESIS = "PHYSICAL_HYPOTHESIS"


class OperatorKind(str, Enum):
    RELATE = "RELATE"
    GENERATE = "GENERATE"
    NAME = "NAME"
    ASSIGN_DESTINY = "ASSIGN_DESTINY"
    SEPARATE = "SEPARATE"
    ASSIGN_FUNCTION = "ASSIGN_FUNCTION"


@dataclass(frozen=True, order=True)
class Relation:
    source: str
    kind: str
    target: str


@dataclass(frozen=True)
class TraceRecord:
    operator_id: str
    kind: OperatorKind
    source_id: str


@dataclass(frozen=True)
class RelationalState:
    """Finite state of the extracted narrative relation system.

    `named` records explicit naming acts in the narrative, not merely the fact
    that a modern transcription uses a label for an entity.
    """

    entities: frozenset[str] = frozenset()
    relations: frozenset[Relation] = frozenset()
    named: frozenset[str] = frozenset()
    destinies: frozenset[str] = frozenset()
    functions: frozenset[str] = frozenset()
    boundaries: frozenset[tuple[str, str]] = frozenset()
    trace: tuple[TraceRecord, ...] = ()


@dataclass(frozen=True)
class Operator:
    operator_id: str
    kind: OperatorKind
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    source_id: str = ""
    relation_kind: str = ""

    def __post_init__(self) -> None:
        if not self.operator_id.strip():
            raise ValueError("operator_id is required")
        if not self.source_id.strip():
            raise ValueError("source_id is required")


PRIMORDIAL_CARRIERS = frozenset({"Apsu", "Tiamat"})


def primordial_state() -> RelationalState:
    """TEXT-derived initial witness from Enuma Elish I.1-8.

    Apsu and Tiamat are represented as primordial carriers already in relation.
    Their labels are transcription handles; `named` remains empty because the
    opening explicitly contrasts this state with later naming acts.
    """

    return RelationalState(
        entities=PRIMORDIAL_CARRIERS,
        relations=frozenset({Relation("Apsu", "MINGLED_WITH", "Tiamat")}),
    )


def is_relational_zero(
    state: RelationalState,
    primordial_carriers: frozenset[str] = PRIMORDIAL_CARRIERS,
) -> bool:
    """Return whether a state realizes the scoped relational-zero condition.

    Relational zero is NOT an empty set and NOT a physical vacuum. It is the
    pre-differentiated state in which only the admitted primordial carriers
    exist, while no generated entities, explicit naming acts, destinies,
    functions, or separation boundaries have yet been introduced.

    Primitive relations among the primordial carriers are allowed. This makes
    the zero a relational boundary condition rather than "nothing".
    """

    if not state.entities.issubset(primordial_carriers):
        return False
    if state.named or state.destinies or state.functions or state.boundaries:
        return False
    return all(
        rel.source in primordial_carriers and rel.target in primordial_carriers
        for rel in state.relations
    )


def relational_rank(
    state: RelationalState,
    primordial_carriers: frozenset[str] = PRIMORDIAL_CARRIERS,
) -> tuple[int, int, int, int]:
    """A representation-level growth signature, not a physical observable."""

    generated = len(state.entities - primordial_carriers)
    identities = len(state.named)
    boundaries = len(state.boundaries)
    roles = len(state.destinies | state.functions)
    return generated, identities, boundaries, roles


def _require_entities(state: RelationalState, entities: tuple[str, ...]) -> None:
    missing = set(entities) - set(state.entities)
    if missing:
        raise ValueError(f"operator references absent entities: {sorted(missing)}")


def apply_operator(state: RelationalState, op: Operator) -> RelationalState:
    """Apply one source-bound operator and append an immutable provenance trace."""

    if op.operator_id in {record.operator_id for record in state.trace}:
        raise ValueError(f"duplicate operator id: {op.operator_id}")

    entities = set(state.entities)
    relations = set(state.relations)
    named = set(state.named)
    destinies = set(state.destinies)
    functions = set(state.functions)
    boundaries = set(state.boundaries)

    if op.kind is OperatorKind.RELATE:
        if len(op.inputs) != 2 or op.outputs:
            raise ValueError("RELATE requires exactly two inputs and no outputs")
        if not op.relation_kind.strip():
            raise ValueError("RELATE requires relation_kind")
        _require_entities(state, op.inputs)
        relations.add(Relation(op.inputs[0], op.relation_kind, op.inputs[1]))

    elif op.kind is OperatorKind.GENERATE:
        if not op.outputs:
            raise ValueError("GENERATE requires at least one output")
        _require_entities(state, op.inputs)
        for output in op.outputs:
            if not output.strip():
                raise ValueError("empty output entity")
            entities.add(output)
            for source in op.inputs:
                relations.add(Relation(source, "GENERATES", output))

    elif op.kind is OperatorKind.NAME:
        if len(op.inputs) != 1 or op.outputs:
            raise ValueError("NAME requires one input and no outputs")
        _require_entities(state, op.inputs)
        named.add(op.inputs[0])

    elif op.kind is OperatorKind.ASSIGN_DESTINY:
        if len(op.inputs) != 1 or op.outputs:
            raise ValueError("ASSIGN_DESTINY requires one input and no outputs")
        _require_entities(state, op.inputs)
        destinies.add(op.inputs[0])

    elif op.kind is OperatorKind.SEPARATE:
        if len(op.inputs) != 1 or len(op.outputs) != 2:
            raise ValueError("SEPARATE requires one input and two outputs")
        _require_entities(state, op.inputs)
        left, right = op.outputs
        if not left.strip() or not right.strip() or left == right:
            raise ValueError("SEPARATE requires two distinct non-empty outputs")
        entities.update(op.outputs)
        boundaries.add((left, right))
        relations.add(Relation(op.inputs[0], "SEPARATES_INTO", left))
        relations.add(Relation(op.inputs[0], "SEPARATES_INTO", right))

    elif op.kind is OperatorKind.ASSIGN_FUNCTION:
        if len(op.inputs) != 1 or op.outputs:
            raise ValueError("ASSIGN_FUNCTION requires one input and no outputs")
        _require_entities(state, op.inputs)
        functions.add(op.inputs[0])

    else:  # pragma: no cover - defensive against future enum expansion
        raise ValueError(f"unsupported operator kind: {op.kind}")

    trace = state.trace + (TraceRecord(op.operator_id, op.kind, op.source_id),)
    return RelationalState(
        entities=frozenset(entities),
        relations=frozenset(relations),
        named=frozenset(named),
        destinies=frozenset(destinies),
        functions=frozenset(functions),
        boundaries=frozenset(boundaries),
        trace=trace,
    )


def run_program(initial: RelationalState, operators: tuple[Operator, ...]) -> RelationalState:
    state = initial
    for op in operators:
        state = apply_operator(state, op)
    return state


def trace_is_source_complete(state: RelationalState) -> bool:
    return all(record.source_id.strip() for record in state.trace)


def promote_to_physical_hypothesis(*, independent_empirical_evidence: bool) -> EpistemicLayer:
    """Mechanical epistemic gate.

    Structural resemblance, narrative order, or a successful executable model
    never counts as independent physical evidence.
    """

    if not independent_empirical_evidence:
        raise ValueError(
            "PHYSICAL_HYPOTHESIS promotion requires independent empirical evidence"
        )
    return EpistemicLayer.PHYSICAL_HYPOTHESIS


# --- Geometric rotation layer -------------------------------------------------

def normalize_angle(theta: float) -> float:
    """Normalize a finite angle to the half-open interval [-pi, pi).

    The helper is purely geometric. It does not assign a physical meaning to
    the angle or identify ANU/KI labels with measured objects.
    """

    import math

    if not math.isfinite(theta):
        raise ValueError("theta must be finite")
    return (theta + math.pi) % (2.0 * math.pi) - math.pi


def relative_rotation(theta_left: float, theta_right: float) -> float:
    """Return the rotation of the right frame relative to the left frame.

    A common rigid rotation cancels:
        relative_rotation(L + alpha, R + alpha) == relative_rotation(L, R)

    This is the formal content of treating K_L and K_R as two projections
    around one reference axis rather than as two unrelated absolute angles.
    """

    return normalize_angle(theta_right - theta_left)


def winding_from_rotation_path(
    relative_phase: tuple[float, ...],
    *,
    tolerance: float = 1e-9,
) -> int:
    """Compute integer winding induced by a closed relative-rotation path.

    The input is a sequence of relative angles sampled along a closed loop.
    Consecutive increments are taken on the principal branch. The path must
    close modulo 2*pi and the accumulated rotation must be integer-quantized
    within the supplied tolerance.

    Thus winding is derived from accumulated geometric rotation; it is not
    introduced as an independent primitive.
    """

    import math

    if len(relative_phase) < 2:
        raise ValueError("at least two phase samples are required")
    if tolerance <= 0 or not math.isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    if not all(math.isfinite(theta) for theta in relative_phase):
        raise ValueError("all phase samples must be finite")

    if abs(normalize_angle(relative_phase[-1] - relative_phase[0])) > tolerance:
        raise ValueError("relative-rotation path must close modulo 2*pi")

    total_rotation = 0.0
    for left, right in zip(relative_phase, relative_phase[1:]):
        total_rotation += normalize_angle(right - left)

    turns = round(total_rotation / (2.0 * math.pi))
    if abs(total_rotation - turns * 2.0 * math.pi) > tolerance:
        raise ValueError("closed path does not resolve to integer winding")
    return int(turns)


def moire_superperiod_ratio(relative_angle: float) -> float:
    """Return L_moire / a for two identical 2D lattices rotated by theta.

    For identical lattice constants and pure relative rotation,

        L_moire / a = 1 / (2 |sin(theta/2)|).

    This is a generic geometric control demonstrating how a small relative
    rotation can generate a much larger emergent spatial scale. It is not
    textual evidence for Enuma Elish and not a claim about a specific material.
    """

    import math

    theta = abs(normalize_angle(relative_angle))
    if theta == 0.0:
        raise ValueError("zero relative rotation has infinite moire superperiod")
    return 1.0 / (2.0 * abs(math.sin(theta / 2.0)))
