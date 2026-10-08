import models

def dot_product(v1: list[float], v2: list[float]) -> float:
    if len(v1) == len(v2):
        return sum(a * b for a, b in zip(v1, v2))
    else:
        raise ValueError("Vectors must have equal lengths!")

def largest_gap(
    sections: tuple[models.Section],
    start: int,
    end: int
) -> int:
    overlapping = [section for section in sections if section.start < end and section.end > start]
    if not overlapping:
        return end - start
    overlapping.sort(key = lambda section: section.start)
    current = start
    largest = 0
    for section in overlapping:
        section_start = max(section.start, start)
        section_end = min(section.end, end)

        largest = max(largest, section_start - current)
        current = max(current, section_end)

    largest = max(largest, end-current)
    return largest

def lunch_penalty(
    schedule: models.Schedule,
    start: int,
    end: int,
    length: int) -> int:

    total_penalty = 0
    for sections in schedule.sections_by_day().values():
        longest = largest_gap(sections, start, end)
        total_penalty += max(0, length - longest)
    return total_penalty
    
def create_penalty_vector(
    schedule: models.Schedule,
    preferences: models.Preferences
) -> list[float]:
    start_pen = max(0, schedule.earliest_start() - preferences.preferred_start)
    end_pen = max(0, schedule.latest_end() - preferences.preferred_end)
    gap_pen = schedule.total_gap_time()
    lunch_pen = lunch_penalty(
        schedule, 
        preferences.lunch_start, 
        preferences.lunch_end,
        preferences.lunch_length
        )
    ...
    return [start_pen, end_pen, gap_pen, lunch_pen]

def create_weight_vector(preferences: models.Preferences) -> list[float]:
    return [
        preferences.start_weight,
        preferences.end_weight,
        preferences.gap_weight,
        preferences.lunch_weight
    ]

def score_schedule(
    schedule: models.Schedule,
    preferences: models.Preferences
) -> float:
    penalties = create_penalty_vector(schedule, preferences)
    weights = create_weight_vector(preferences)

    return dot_product(penalties, weights)

def rank_schedules(
    schedules: list[models.Schedule],
    preferences: models.Preferences
) -> list[models.Schedule]:
    return sorted(
        schedules,
        key = lambda schedule: score_schedule(schedule, preferences)
    )