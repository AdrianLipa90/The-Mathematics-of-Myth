import json
from pathlib import Path

import pytest

from mythmath.mayor_transform import (
    EvidenceItem,
    EvidenceKind,
    EvaluationStatus,
    Hypothesis,
    RelationGraph,
    RelationSignature,
    compare_relation_graphs,
    evaluate_hypothesis,
    has_independent_constraint,
    retained_invariants,
    specificity_margin,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "mayor_research_cases_v0_1.json"


def R(a, r, b, order=None):
    return RelationSignature(a, r, b, order)


def test_exact_normalized_relations_define_retained_invariants():
    shared = R("WATER_SOURCE", "CAUSES", "TOXIC_EFFECT", 1)
    narrative = RelationGraph(frozenset({
        shared,
        R("TOXIC_EFFECT", "DAMAGES", "CONTAINER", 2),
    }))
    independent = RelationGraph(frozenset({
        shared,
        R("GEOLOGY", "PERMITS", "TOXIN_CANDIDATE", 0),
    }))

    comparison = compare_relation_graphs(narrative, independent)
    assert comparison.shared == frozenset({shared})
    assert retained_invariants(narrative, independent) == frozenset({shared})
    assert comparison.jaccard == pytest.approx(1 / 3)


def test_sequence_is_part_of_relation_signature():
    a = RelationGraph(frozenset({R("EVENT", "PRECEDES", "EFFECT", 1)}))
    b = RelationGraph(frozenset({R("EVENT", "PRECEDES", "EFFECT", 2)}))
    assert compare_relation_graphs(a, b).shared == frozenset()
    assert compare_relation_graphs(a, b).jaccard == 0.0


def test_independent_constraint_requires_non_textual_independent_evidence():
    items = [
        EvidenceItem(
            evidence_id="N1",
            case_id="STYX",
            kind=EvidenceKind.TEXTUAL,
            source_id="ANCIENT-TEXT",
            independent_of_target_narrative=False,
        )
    ]
    assert not has_independent_constraint(items, case_id="STYX")

    items.append(
        EvidenceItem(
            evidence_id="G1",
            case_id="STYX",
            kind=EvidenceKind.GEOLOGICAL,
            source_id="GEOLOGY-STUDY",
            independent_of_target_narrative=True,
        )
    )
    assert has_independent_constraint(items, case_id="STYX")


def test_hypothesis_can_be_constrained_but_is_not_promoted_to_proof():
    relation = R("LIMESTONE_CONTEXT", "PERMITS", "TOXIN_CANDIDATE")
    hypothesis = Hypothesis(
        hypothesis_id="H1",
        case_id="STYX",
        required_narrative=frozenset(),
        required_independent=frozenset({relation}),
    )
    evidence = [
        EvidenceItem(
            evidence_id="G1",
            case_id="STYX",
            kind=EvidenceKind.GEOLOGICAL,
            source_id="GEOLOGY-STUDY",
            independent_of_target_narrative=True,
        )
    ]
    evaluation = evaluate_hypothesis(
        hypothesis,
        RelationGraph(),
        RelationGraph(frozenset({relation})),
        evidence,
    )
    assert evaluation.status is EvaluationStatus.INDEPENDENTLY_CONSTRAINED
    assert evaluation.consistent_with_constraints


def test_missing_preregistered_relation_fails_constraint():
    required = R("AGENT", "CREATED_AS", "ARTIFICIAL_BODY")
    hypothesis = Hypothesis(
        hypothesis_id="AI-H",
        case_id="AI",
        required_narrative=frozenset({required}),
        required_independent=frozenset(),
    )
    evaluation = evaluate_hypothesis(
        hypothesis,
        RelationGraph(),
        RelationGraph(),
        [],
    )
    assert evaluation.status is EvaluationStatus.CONSTRAINT_FAILURE
    assert required in evaluation.missing_narrative


def test_negative_control_specificity_margin_is_explicit():
    x = R("A", "CAUSES", "B")
    y = R("B", "LEADS_TO", "C")
    independent = RelationGraph(frozenset({x, y}))
    target = RelationGraph(frozenset({x, y}))
    control = RelationGraph(frozenset({x}))
    assert specificity_margin(target, independent, [control]) == pytest.approx(0.5)


def test_committed_research_registry_has_current_mayor_domains_and_three_styx_hypotheses():
    payload = json.loads(DATA.read_text())
    case_ids = {case["id"] for case in payload["cases"]}
    assert {
        "MYTHOPEDIA_GEOMYTHS",
        "STYX_TOXICOLOGY",
        "ANCIENT_AI",
        "AMAZONS_SCYTHIA",
        "EXTRAORDINARY_BODIES",
        "ANIMAL_SELF_MEDICATION",
    } <= case_ids

    styx = next(case for case in payload["cases"] if case["id"] == "STYX_TOXICOLOGY")
    assert len(styx["hypotheses"]) == 3
    assert "proof is elusive" in styx["caution"]


def test_every_case_points_to_committed_source_ids():
    payload = json.loads(DATA.read_text())
    source_ids = {source["id"] for source in payload["sources"]}
    for case in payload["cases"]:
        assert set(case["sources"]) <= source_ids
