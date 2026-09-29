# backend/scheduler.py

import itertools

from backend import models

def conflicts(section_a: models.Section, section_b: models.Section) -> bool:
    days_match = any(day in section_a.days for day in section_b.days)
    if days_match:
        a_start = section_a.start
        a_end = section_a.end
        b_start = section_b.start
        b_end = section_b.end
        validate_interval = a_start < b_end and b_start < a_end
        return validate_interval
    return False

def generate_schedules(courses: dict[str, list[models.Section]]) -> list[tuple[models.Section, ...]]:
    validated_schedules = list(
        filter(
            lambda combo: all(not conflicts(a, b) for a, b in itertools.combinations(combo, 2)),
            itertools.product(*courses.values())
        )
    )
    return validated_schedules

    