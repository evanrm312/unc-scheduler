from backend.scheduler import conflicts, generate_schedules
from backend.data import load_courses
import itertools

from backend import models
from backend.scheduler import conflicts


def make_section(days, start, end):
    return models.Section(
        course="TEST 101",
        section="001",
        days=days,
        start=start,
        end=end,
        instructor="Test Instructor",
    )


def test_overlapping_same_day():
    a = make_section(["M", "W", "F"], 600, 660)
    b = make_section(["M", "W", "F"], 630, 690)

    assert conflicts(a, b) is True


def test_nonoverlapping_same_day():
    a = make_section(["M"], 600, 660)
    b = make_section(["M"], 720, 780)

    assert conflicts(a, b) is False


def test_same_time_different_days():
    a = make_section(["M", "W"], 600, 660)
    b = make_section(["T", "Th"], 600, 660)

    assert conflicts(a, b) is False


def test_touching_intervals():
    a = make_section(["M"], 600, 660)
    b = make_section(["M"], 660, 720)

    assert conflicts(a, b) is False


def test_partial_day_overlap():
    a = make_section(["M", "W", "F"], 600, 660)
    b = make_section(["W"], 630, 690)

    assert conflicts(a, b) is True

def test_full_course_tuple():
    a = load_courses()
    l = generate_schedules(a)
    assert len(l) > 0 and len(a) > 0
    for i in l:
        assert len(i) == len(a)
        c = [conflicts(a, b) for a, b in itertools.combinations(i, 2)]
        assert True not in c

