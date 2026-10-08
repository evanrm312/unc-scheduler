import pytest

from backend import models, ranking


def make_preferences(**overrides) -> models.Preferences:
    values = {
        "preferred_start": 10 * 60,
        "preferred_end": 16 * 60,
        "start_weight": 1.0,
        "end_weight": 1.0,
        "gap_weight": 1.0,
        "lunch_length": 45,
        "lunch_weight": 1.0,
        "lunch_start": 12 * 60,
        "lunch_end": 14 * 60,
    }
    values.update(overrides)
    return models.Preferences(**values)


def test_dot_product():
    assert ranking.dot_product([1, 2, 3], [4, 5, 6]) == 32


def test_dot_product_rejects_different_lengths():
    with pytest.raises(ValueError):
        ranking.dot_product([1, 2], [1])


def test_largest_gap_with_no_classes(make_section):
    assert ranking.largest_gap((), 12 * 60, 14 * 60) == 120


def test_largest_gap_between_and_after_classes(make_section):
    first = make_section(start=11 * 60 + 30, end=12 * 60 + 15)
    second = make_section(start=12 * 60 + 45, end=13 * 60)

    assert ranking.largest_gap((second, first), 12 * 60, 14 * 60) == 60


def test_lunch_penalty_sums_shortages_for_each_class_day(make_section):
    monday = make_section(days=["M"], start=12 * 60, end=13 * 60)
    tuesday = make_section(days=["T"], start=12 * 60, end=13 * 60 + 30)
    schedule = models.Schedule((monday, tuesday))

    assert ranking.lunch_penalty(schedule, 12 * 60, 14 * 60, 45) == 15


def test_penalty_vector_penalizes_early_start_and_late_end(make_section):
    early = make_section(days=["M"], start=9 * 60, end=10 * 60)
    late = make_section(days=["T"], start=16 * 60, end=17 * 60)
    schedule = models.Schedule((early, late))
    preferences = make_preferences(gap_weight=0, lunch_weight=0)

    penalties = ranking.create_penalty_vector(schedule, preferences)

    assert penalties[0] == 60
    assert penalties[1] == 60


def test_schedule_inside_start_and_end_limits_has_no_time_penalty(make_section):
    section = make_section(start=10 * 60 + 30, end=15 * 60)
    schedule = models.Schedule((section,))

    penalties = ranking.create_penalty_vector(schedule, make_preferences())

    assert penalties[0] == 0
    assert penalties[1] == 0


def test_score_schedule_is_weighted_penalty_sum(make_section):
    first = make_section(days=["M"], start=9 * 60, end=10 * 60)
    second = make_section(days=["M"], start=11 * 60, end=17 * 60)
    schedule = models.Schedule((first, second))
    preferences = make_preferences(
        start_weight=2,
        end_weight=3,
        gap_weight=0.5,
        lunch_weight=0,
    )

    # 60 early * 2 + 60 late * 3 + 60 gap * 0.5
    assert ranking.score_schedule(schedule, preferences) == 330


def test_rank_schedules_places_lowest_score_first(make_section):
    early = models.Schedule(
        (make_section(section="001", start=8 * 60, end=15 * 60),)
    )
    preferred = models.Schedule(
        (make_section(section="002", start=10 * 60, end=15 * 60),)
    )
    late = models.Schedule(
        (make_section(section="003", start=10 * 60, end=17 * 60),)
    )
    preferences = make_preferences(gap_weight=0, lunch_weight=0)

    ranked = ranking.rank_schedules([late, early, preferred], preferences)

    assert ranked == [preferred, late, early]
