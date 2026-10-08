# backend/scheduler.py

import itertools

from . import models, data

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

def generate_schedules(courses: dict[str, list[models.Section]]) -> list[models.Schedule]:
    validated_schedules = list(
        filter(
            lambda combo: all(not conflicts(a, b) for a, b in itertools.combinations(combo, 2)),
            itertools.product(*courses.values())
        )
    )
    validated_sched_objects = []
    for schedule in validated_schedules:
        validated_sched_objects.append(models.Schedule(schedule))
    return validated_sched_objects

def search_schedules(schedule_list: list[models.Schedule], *search_params: models.Section, match_all: bool = True) -> list[int]:
    # returns the index(es) of any matching schedules
    matcher = all if match_all else any
    found_indexes = []
    for index, schedule in enumerate(schedule_list):
        if matcher(param in schedule.sections for param in search_params):
            found_indexes.append(index)
    return found_indexes
    