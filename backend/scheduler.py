# backend/scheduler.py

import itertools

def conflicts(section_a, section_b):
    days_match = any(day in section_a["days"] for day in section_b["days"])
    if days_match:
        a_start = section_a["start"]
        a_end = section_a["end"]
        b_start = section_b["start"]
        b_end = section_b["end"]
        validate_interval = a_start < b_end and b_start < a_end
        return validate_interval
    return False
def generate_schedules(courses):
    n = len(courses.keys())
    combinations = itertools.product()