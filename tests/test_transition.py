import math
import pytest

from mythmath.transition import (
    EvidenceTier,
    EventStructure,
    RelationClass,
    active_block_signature,
    classify_relation,
    cycle_completion_time,
    horizon,
    is_strict_descent,
    post_closure_state,
)


def test_123_45_6_to_7_signature():
    assert active_block_signature() == (3, 2, 1, 0)
    assert is_strict_descent(active_block_signature())
    assert horizon() == 6
    assert post_closure_state() == 7


def test_six_is_triangular_sum_of_active_block_sizes():
    assert sum(active_block_signature()[:-1]) == 6
    assert 1 + 2 + 3 == 6


def test_exact_isomorphism_requires_transition_structure_not_same_number():
    resurrection = EventStructure(
        states=("death", "liminal", "life"),
        transitions=("enter_liminal", "emerge"),
        numeric_markers=(3,),
    )
    same_graph_different_labels = EventStructure(
        states=("darkness", "hidden", "light"),
        transitions=("enter_liminal", "emerge"),
        numeric_markers=(3,),
    )
    assert classify_relation(resurrection, same_graph_different_labels) is RelationClass.ISOMORPHISM


def test_number_three_alone_is_not_isomorphism():
    a = EventStructure(states=("a", "b"), transitions=("die",), numeric_markers=(3,))
    b = EventStructure(states=("x", "y"), transitions=("harvest",), numeric_markers=(3,))
    assert classify_relation(a, b) is RelationClass.NUMBER_MATCH_ONLY


def test_amaterasu_guard_canonical_story_cannot_inherit_late_three_day_datum():
    canonical = {"tier": EvidenceTier.PRIMARY_CANONICAL, "supports": {"darkness_to_light_transition"}}
    later = {"tier": EvidenceTier.LATER_RITUAL, "supports": {"three_interval_liminal_motif"}}
    assert "three_interval_liminal_motif" not in canonical["supports"]
    assert later["tier"] is EvidenceTier.LATER_RITUAL


def test_cycle_completion_operator():
    omega = 2 * math.pi / 10.0
    assert cycle_completion_time(0.3, omega) == pytest.approx(10.0)


@pytest.mark.parametrize("omega", [0.0, float("inf"), float("nan")])
def test_cycle_completion_fail_closed(omega):
    with pytest.raises(ValueError):
        cycle_completion_time(0.0, omega)
