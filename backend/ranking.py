from math import sqrt
import json
import models

def dot_product(v1: list[float], v2: list[float]) -> float:
    if len(v1) == len(v2):
        return sum(a * b for a, b in zip(v1, v2))
    else:
        raise ValueError("Vectors must have equal lengths!")

def lunch_penalty(
    schedule: models.Schedule,
    start: int,
    end: int,
    length: int) -> int:
    

def create_penalty_vector(
    schedule: models.Schedule,
    preferences: models.Preferences
) -> list[float]:
    start_pen = abs(schedule.earliest_start() - preferences.preferred_start)
    end_pen = abs(schedule.latest_end() - preferences.preferred_end)
    gap_pen = schedule.total_gap_time()
    lunch_penalty = lunch_penalty(
        schedule, 
        preferences.lunch_start, 
        preferences.lunch_end,
        preferences.lunch_length
        )
    ...
    return [start_pen, end_pen, gap_pen]

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

def ranked_schedules(
    schedules: list[models.Schedule],
    preferences: models.Preferences
) -> list[models.Schedule]:
    return sorted(
        schedules,
        key = lambda schedule: score_schedule(schedule, preferences)
    )