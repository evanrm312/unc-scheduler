from dataclasses import dataclass

@dataclass
class Section:
    course: str
    section: str
    days: list[str]
    start: int
    end: int
    instructor: str
