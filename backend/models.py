from dataclasses import dataclass

@dataclass
class Section:
    course: str
    section: str
    days: list[str]
    start: int
    end: int
    instructor: str

@dataclass
class Preferences:
    preferred_start: int
    preferred_end: int
    gap_weight: float
    lunch_start: int
    lunch_end: int

@dataclass(frozen=True)
class Schedule:
    sections: tuple[Section, ...]
    def sort_by_start(self) -> tuple:
        return tuple(sorted(self.sections, key = lambda x: x.start))
    def total_gap_time(self) -> int:
        cum_gap_time = 0
        for current, next in zip(self.sort_by_start(),self.sort_by_start()[1:]):
            cum_gap_time += next.end - current.start
        return cum_gap_time
    def earliest_start(self) -> int:
        return min(section.start for section in self.sections)
    def latest_end(self) -> int:
        return max(section.end for section in self.sections)