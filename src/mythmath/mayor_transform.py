"""Mayor Formalism v0.1.

A conservative mathematical layer for Adrienne Mayor's research method:
compare structured features in narrative traditions with independently sourced
material, scientific, historical, or iconographic evidence.

The module deliberately does not assume that myths are literal records, that
cultural transmission destroys information, or that structural overlap proves
causal descent. It extracts testable relation invariants and exposes null
comparisons.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class EvidenceKind(str, Enum):
    NARRATIVE = "NARRATIVE"
    TEXTUAL = "TEXTUAL"
    GEOLOGICAL = "GEOLOGICAL"
    TOXICOLOGICAL = "TOXICOLOGICAL"
    ARCHAEOLOGICAL = "ARCHAEOLOGICAL"
    ICONOGRAPHIC = "ICONOGRAPHIC"
    HISTORICAL = "HISTORICAL"
    ZOOLOGICAL = "ZOOLOGICAL"
    MATERIAL = "MATERIAL"
    MODERN_SCIENCE = "MODERN_SCIENCE"


class EvaluationStatus(str, Enum):
    CONSTRAINT_FAILURE = "CONSTRAINT_FAILURE"
    NARRATIVE_ONLY = "NARRATIVE_ONLY"
    INDEPENDENTLY_CONSTRAINED = "INDEPENDENTLY_CONSTRAINED"


@dataclass(frozen=True, order=True)
class RelationSignature:
    """A name-independent typed relation.

    Roles should be normalized before comparison (for example WATER_SOURCE,
    TOXIC_EFFECT, or CONTAINER_MATERIAL).  Optional order encodes sequence
    without requiring identical proper nouns.
    """

    source_role: str
    relation: str
    target_role: str
    order: int | None = None

    def __post_init__(self) -> None:
        if not self.source_role.strip():
            raise ValueError("source_role is required")
        if not self.relation.strip():
            raise ValueError("relation is required")
        if not self.target_role.strip():
            raise ValueError("target_role is required")
        if self.order is not None and self.order < 0:
            raise ValueError("order must be non-negative")


@dataclass(frozen=True)
class RelationGraph:
    relations: frozenset[RelationSignature] = frozenset()


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    case_id: str
    kind: EvidenceKind
    source_id: str
    independent_of_target_narrative: bool
    note: str = ""

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id is required")
        if not self.case_id.strip():
            raise ValueError("case_id is required")
        if not self.source_id.strip():
            raise ValueError("source_id is required")


@dataclass(frozen=True)
class GraphComparison:
    shared: frozenset[RelationSignature]
    narrative_only: frozenset[RelationSignature]
    independent_only: frozenset[RelationSignature]
    precision: float
    recall: float
    jaccard: float


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    case_id: str
    required_narrative: frozenset[RelationSignature]
    required_independent: frozenset[RelationSignature]

    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip():
            raise ValueError("hypothesis_id is required")
        if not self.case_id.strip():
            raise ValueError("case_id is required")


@dataclass(frozen=True)
class HypothesisEvaluation:
    hypothesis_id: str
    status: EvaluationStatus
    missing_narrative: frozenset[RelationSignature]
    missing_independent: frozenset[RelationSignature]

    @property
    def consistent_with_constraints(self) -> bool:
        return not self.missing_narrative and not self.missing_independent


def compare_relation_graphs(
    narrative: RelationGraph,
    independent: RelationGraph,
) -> GraphComparison:
    """Compare exact normalized relation signatures.

    No hidden relabeling or edge deletion is performed.  More sophisticated
    graph matching must be explicit in a later version.
    """

    a = narrative.relations
    b = independent.relations
    shared = a & b
    narrative_only = a - b
    independent_only = b - a

    precision = len(shared) / len(a) if a else (1.0 if not b else 0.0)
    recall = len(shared) / len(b) if b else (1.0 if not a else 0.0)
    union = a | b
    jaccard = len(shared) / len(union) if union else 1.0

    return GraphComparison(
        shared=frozenset(shared),
        narrative_only=frozenset(narrative_only),
        independent_only=frozenset(independent_only),
        precision=precision,
        recall=recall,
        jaccard=jaccard,
    )


def retained_invariants(
    narrative: RelationGraph,
    independent: RelationGraph,
) -> frozenset[RelationSignature]:
    """Return relations independently recoverable in both representations."""

    return compare_relation_graphs(narrative, independent).shared


def has_independent_constraint(
    evidence: Iterable[EvidenceItem],
    *,
    case_id: str,
) -> bool:
    """Require at least one non-narrative item independent of target narrative."""

    return any(
        item.case_id == case_id
        and item.independent_of_target_narrative
        and item.kind not in {EvidenceKind.NARRATIVE, EvidenceKind.TEXTUAL}
        for item in evidence
    )


def evaluate_hypothesis(
    hypothesis: Hypothesis,
    narrative: RelationGraph,
    independent: RelationGraph,
    evidence: Iterable[EvidenceItem],
) -> HypothesisEvaluation:
    """Evaluate constraints without promoting consistency to proof.

    A candidate can be INDEPENDENTLY_CONSTRAINED only if all preregistered
    relations are present and the case has at least one independent
    non-textual evidence item.
    """

    missing_narrative = hypothesis.required_narrative - narrative.relations
    missing_independent = hypothesis.required_independent - independent.relations

    if missing_narrative or missing_independent:
        status = EvaluationStatus.CONSTRAINT_FAILURE
    elif has_independent_constraint(evidence, case_id=hypothesis.case_id):
        status = EvaluationStatus.INDEPENDENTLY_CONSTRAINED
    else:
        status = EvaluationStatus.NARRATIVE_ONLY

    return HypothesisEvaluation(
        hypothesis_id=hypothesis.hypothesis_id,
        status=status,
        missing_narrative=frozenset(missing_narrative),
        missing_independent=frozenset(missing_independent),
    )


def specificity_margin(
    target: RelationGraph,
    independent: RelationGraph,
    negative_controls: Iterable[RelationGraph],
) -> float:
    """Target Jaccard minus the strongest preregistered negative control.

    Positive values indicate specificity relative to the supplied controls;
    they do not by themselves establish historical causation.
    """

    target_score = compare_relation_graphs(target, independent).jaccard
    control_scores = [
        compare_relation_graphs(control, independent).jaccard
        for control in negative_controls
    ]
    strongest_control = max(control_scores, default=0.0)
    return target_score - strongest_control
