import pytest

from backend import models, scheduler


@pytest.mark.parametrize(
    ("days_a", "start_a", "end_a", "days_b", "start_b", "end_b", "expected"),
    [
        (["M"], 600, 660, ["M"], 630, 690, True),
        (["M"], 600, 660, ["M"], 660, 720, False),
        (["M", "W"], 600, 660, ["T", "Th"], 600, 660, False),
        (["M", "W", "F"], 600, 660, ["W"], 630, 690, True),
    ],
)
def test_conflicts(
    make_section,
    days_a,
    start_a,
    end_a,
    days_b,
    start_b,
    end_b,
    expected,
):
    a = make_section(days=days_a, start=start_a, end=end_a)
    b = make_section(days=days_b, start=start_b, end=end_b)

    assert scheduler.conflicts(a, b) is expected


def test_generate_schedules_rejects_only_conflicting_combinations(make_section):
    a1 = make_section(course="A", section="001", days=["M"], start=540, end=600)
    a2 = make_section(course="A", section="002", days=["T"], start=540, end=600)
    b1 = make_section(course="B", section="001", days=["M"], start=570, end=630)
    b2 = make_section(course="B", section="002", days=["W"], start=570, end=630)

    schedules = scheduler.generate_schedules({"A": [a1, a2], "B": [b1, b2]})
    section_pairs = [schedule.sections for schedule in schedules]

    assert len(schedules) == 3
    assert all(isinstance(schedule, models.Schedule) for schedule in schedules)
    assert (a1, b1) not in section_pairs
    assert len(section_pairs) == 3
    assert (a1, b2) in section_pairs
    assert (a2, b1) in section_pairs
    assert (a2, b2) in section_pairs


def test_search_schedules_match_all(make_section):
    a = make_section(course="A", section="001")
    b = make_section(course="B", section="001")
    c = make_section(course="C", section="001")
    schedules = [
        models.Schedule((a, b)),
        models.Schedule((a, c)),
        models.Schedule((b, c)),
    ]

    assert scheduler.search_schedules(schedules, a, b) == [0]


def test_search_schedules_match_any(make_section):
    a = make_section(course="A", section="001")
    b = make_section(course="B", section="001")
    c = make_section(course="C", section="001")
    d = make_section(course="D", section="001")
    schedules = [
        models.Schedule((a, b)),
        models.Schedule((a, c)),
        models.Schedule((c, d)),
    ]

    assert scheduler.search_schedules(schedules, b, d, match_all=False) == [0, 2]
