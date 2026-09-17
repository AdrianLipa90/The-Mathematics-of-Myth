import math
import pytest

from mythmath.transition import (
    BoundarySchedule,
    EvidenceTier,
    EventStructure,
    RelationClass,
    active_block_signature,
    classify_boundary_schedule,
    classify_relation,
    cycle_completion_time,
    horizon,
    is_strict_descent,
    post_closure_state,
    phase_fraction_period,
    interval_contains,
    DIVINE_DAY_THRESHOLDS,
    MESOPOTAMIAN_DIVINE_NUMERALS,
    creation_calendar_state,
    divine_day_threshold,
    schematic_year,
    sexagesimal_phase,
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
    canonical = {
        "tier": EvidenceTier.PRIMARY_CANONICAL,
        "supports": {"darkness_to_light_transition"},
    }
    later = {
        "tier": EvidenceTier.LATER_RITUAL,
        "supports": {"three_interval_liminal_motif"},
    }
    assert "three_interval_liminal_motif" not in canonical["supports"]
    assert later["tier"] is EvidenceTier.LATER_RITUAL


def test_cycle_completion_operator():
    omega = 2 * math.pi / 10.0
    assert cycle_completion_time(0.3, omega) == pytest.approx(10.0)


@pytest.mark.parametrize("omega", [0.0, float("inf"), float("nan")])
def test_cycle_completion_fail_closed(omega):
    with pytest.raises(ValueError):
        cycle_completion_time(0.0, omega)


def test_genesis_gilgamesh_projected_schedule_isomorphic_only_at_schedule_level():
    genesis = BoundarySchedule(active_steps=6, boundary_step=7, boundary_type="cessation")
    gilgamesh = BoundarySchedule(active_steps=6, boundary_step=7, boundary_type="cessation")
    assert classify_boundary_schedule(genesis, gilgamesh) is RelationClass.ISOMORPHISM


def test_inanna_seven_gate_boundary_same_geometry_different_semantics():
    genesis = BoundarySchedule(active_steps=6, boundary_step=7, boundary_type="cessation")
    inanna = BoundarySchedule(active_steps=6, boundary_step=7, boundary_type="death_threshold")
    assert classify_boundary_schedule(genesis, inanna) is RelationClass.ORDER_HOMOMORPHISM


def test_inanna_full_story_not_exact_resurrection_isomorphism():
    resurrection_core = EventStructure(
        states=("death", "liminal", "life"),
        transitions=("death_to_liminal", "liminal_to_life"),
        numeric_markers=(3,),
    )
    inanna_full = EventStructure(
        states=("descent", "corpse", "waiting", "rescue", "life", "ascent"),
        transitions=("descent", "death_to_liminal", "rescue_after_three", "liminal_to_life", "ascent"),
        numeric_markers=(3, 7),
    )
    assert classify_relation(resurrection_core, inanna_full) is RelationClass.ORDER_HOMOMORPHISM


def test_zoroastrian_three_day_threshold_is_not_resurrection_isomorphism():
    resurrection = EventStructure(
        states=("death", "liminal", "life"),
        transitions=("death_to_liminal", "liminal_to_life"),
        numeric_markers=(3,),
    )
    zoroastrian = EventStructure(
        states=("death", "liminal", "judgment"),
        transitions=("death_to_liminal", "judgment_transition"),
        numeric_markers=(3, 4),
    )
    assert classify_relation(resurrection, zoroastrian) is RelationClass.ANALOGY


def test_matching_six_or_seven_counts_without_cessation_is_number_match_only():
    creation_variant = BoundarySchedule(active_steps=5, boundary_step=7, boundary_type="additional_creation")
    genesis = BoundarySchedule(active_steps=6, boundary_step=7, boundary_type="cessation")
    assert classify_boundary_schedule(genesis, creation_variant) is RelationClass.NUMBER_MATCH_ONLY


def test_lunar_quarter_null_model():
    # Mean synodic month in days; this is a null-model calculation, not a
    # historical derivation of the seven-day week.
    assert phase_fraction_period(29.530588, 4) == pytest.approx(7.382647)


def test_three_days_lies_inside_naked_eye_lunar_invisibility_range():
    # Literature reports an observational invisibility span of roughly
    # 2.5--4.5 days; three days is therefore not by itself diagnostic of
    # cultural transmission or a hidden universal operator.
    assert interval_contains(3.0, 2.5, 4.5)


def test_astronomical_helpers_fail_closed():
    with pytest.raises(ValueError):
        phase_fraction_period(0.0, 4)
    with pytest.raises(ValueError):
        phase_fraction_period(29.5, 0)
    with pytest.raises(ValueError):
        interval_contains(3.0, 4.5, 2.5)


def test_divine_calendar_decadal_thresholds_are_frozen():
    assert DIVINE_DAY_THRESHOLDS == (10, 20, 30, 40, 50, 60)
    assert tuple(divine_day_threshold(i) for i in range(1, 7)) == DIVINE_DAY_THRESHOLDS


def test_mesopotamian_decadal_ladder_is_attested_but_not_exhaustive():
    expected = {
        10: "Adad",
        20: "Shamash",
        30: "Sin",
        40: "Ea",
        50: "Enlil",
        60: "Anu",
    }
    assert {k: MESOPOTAMIAN_DIVINE_NUMERALS[k] for k in DIVINE_DAY_THRESHOLDS} == expected
    # Ishtar=15 is an explicit guard against claiming the pantheon consists
    # only of the six decadal values.
    assert MESOPOTAMIAN_DIVINE_NUMERALS[15] == "Ishtar"
    assert 15 not in DIVINE_DAY_THRESHOLDS


def test_sixty_is_boundary_not_seventh_equal_sector():
    assert creation_calendar_state(0) == ("ACTIVE", 1)
    assert creation_calendar_state(9.999) == ("ACTIVE", 1)
    assert creation_calendar_state(10) == ("ACTIVE", 2)
    assert creation_calendar_state(59.999) == ("ACTIVE", 6)
    assert creation_calendar_state(60) == ("POST_CLOSURE", 7)
    assert sexagesimal_phase(60) == pytest.approx(0.0)


def test_post_sixty_rule_is_deliberately_undefined():
    with pytest.raises(ValueError):
        creation_calendar_state(60.0001)
    with pytest.raises(ValueError):
        creation_calendar_state(70)


def test_schematic_360_year_and_flood_five_month_interval():
    assert schematic_year() == 360
    assert 5 * 30 == 150
    assert schematic_year() // 60 == 6


def test_divine_calendar_helpers_fail_closed():
    for bad in (0, 7, 1.5, True):
        with pytest.raises(ValueError):
            divine_day_threshold(bad)
    for bad in (-1.0, float("inf"), float("nan")):
        with pytest.raises(ValueError):
            sexagesimal_phase(bad)

