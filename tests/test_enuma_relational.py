import json
from pathlib import Path

import pytest

from mythmath.enuma_relational import (
    EpistemicLayer,
    Operator,
    OperatorKind,
    Relation,
    apply_operator,
    is_relational_zero,
    primordial_state,
    promote_to_physical_hypothesis,
    relational_rank,
    run_program,
    trace_is_source_complete,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "enuma_elish_relational_core_v1.json"


def _load_program() -> tuple[Operator, ...]:
    payload = json.loads(DATA.read_text())
    return tuple(
        Operator(
            operator_id=row["operator_id"],
            kind=OperatorKind(row["kind"]),
            inputs=tuple(row.get("inputs", ())),
            outputs=tuple(row.get("outputs", ())),
            source_id=row["source_id"],
            relation_kind=row.get("relation_kind", ""),
        )
        for row in payload["formal_program"]
    )


def test_primordial_state_is_relational_zero_not_empty_nothingness():
    state = primordial_state()
    assert state.entities == frozenset({"Apsu", "Tiamat"})
    assert Relation("Apsu", "MINGLED_WITH", "Tiamat") in state.relations
    assert is_relational_zero(state)


def test_first_generation_exits_relational_zero():
    state = primordial_state()
    state = apply_operator(
        state,
        Operator(
            operator_id="TEST.GEN.1",
            kind=OperatorKind.GENERATE,
            inputs=("Apsu", "Tiamat"),
            outputs=("Lahmu", "Lahamu"),
            source_id="EE-I-009-010",
        ),
    )
    assert not is_relational_zero(state)
    assert {"Lahmu", "Lahamu"} <= state.entities


def test_complete_committed_program_is_source_bound_and_grows_structure():
    final = run_program(primordial_state(), _load_program())
    assert trace_is_source_complete(final)
    assert relational_rank(final) == (9, 2, 1, 1)
    assert {"Lahmu", "Lahamu"} <= final.named
    assert ("UpperCosmicRegion", "LowerCosmicRegion") in final.boundaries
    assert "Humanity" in final.functions


def test_provenance_trace_is_append_only_and_input_state_is_unchanged():
    before = primordial_state()
    after = apply_operator(
        before,
        Operator(
            operator_id="TEST.NAME.1",
            kind=OperatorKind.NAME,
            inputs=("Apsu",),
            source_id="TEST-SOURCE",
        ),
    )
    assert before.trace == ()
    assert len(after.trace) == 1
    assert after.trace[0].source_id == "TEST-SOURCE"


def test_duplicate_operator_id_is_rejected():
    op = Operator(
        operator_id="TEST.DUP",
        kind=OperatorKind.NAME,
        inputs=("Apsu",),
        source_id="TEST-SOURCE",
    )
    state = apply_operator(primordial_state(), op)
    with pytest.raises(ValueError):
        apply_operator(state, op)


def test_naming_or_role_assignment_of_absent_entity_fails_closed():
    with pytest.raises(ValueError):
        apply_operator(
            primordial_state(),
            Operator(
                operator_id="TEST.BAD.NAME",
                kind=OperatorKind.NAME,
                inputs=("NotYetGenerated",),
                source_id="TEST-SOURCE",
            ),
        )

    with pytest.raises(ValueError):
        apply_operator(
            primordial_state(),
            Operator(
                operator_id="TEST.BAD.ROLE",
                kind=OperatorKind.ASSIGN_FUNCTION,
                inputs=("Humanity",),
                source_id="TEST-SOURCE",
            ),
        )


def test_separation_requires_two_distinct_outputs():
    with pytest.raises(ValueError):
        apply_operator(
            primordial_state(),
            Operator(
                operator_id="TEST.BAD.SPLIT",
                kind=OperatorKind.SEPARATE,
                inputs=("Tiamat",),
                outputs=("Sky", "Sky"),
                source_id="TEST-SOURCE",
            ),
        )


def test_structural_fit_cannot_self_promote_to_physics():
    with pytest.raises(ValueError):
        promote_to_physical_hypothesis(independent_empirical_evidence=False)
    assert (
        promote_to_physical_hypothesis(independent_empirical_evidence=True)
        is EpistemicLayer.PHYSICAL_HYPOTHESIS
    )


def test_legacy_143_mapping_remains_unverified_until_corpus_is_recovered():
    payload = json.loads(DATA.read_text())
    legacy = payload["legacy_143"]
    assert legacy["historical_reference_present"] is True
    assert legacy["standalone_143_statement_corpus_recovered"] is False
    assert legacy["status"] == "REFERENCE_ONLY_NOT_REVERIFIED"


def test_every_program_operator_points_to_a_committed_text_witness():
    payload = json.loads(DATA.read_text())
    witness_ids = {w["id"] for w in payload["witnesses"]}
    source_ids = {op["source_id"] for op in payload["formal_program"]}
    assert source_ids <= witness_ids
