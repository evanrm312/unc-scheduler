import json
from backend import models

def load_courses():
    with open("data/courses.json") as f:
        courses = json.load(f)
    sectioned_courses = dict()
    for course_name, sections in courses.items():
        sectioned_courses[course_name] = []
        for section in sections:
            sectioned_courses[course_name].append(
                models.Section(
                    course=course_name,
                    section=section["section"],
                    days=section["days"],
                    start=section["start"],
                    end=section["end"],
                    instructor=section["instructor"],
                )
            )

    return sectioned_courses