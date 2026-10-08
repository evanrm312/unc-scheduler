from dataclasses import dataclass

@dataclass(frozen=True)
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
    start_weight: float
    end_weight: float
    gap_weight: float
    lunch_length: int
    lunch_weight: float
    lunch_start: int
    lunch_end: int

@dataclass(frozen=True)
class Schedule:
    sections: tuple[Section, ...]
    def sections_by_day(self) -> dict[str, tuple[Section, ...]]:
        grouped = {}

        for section in self.sections:
            for day in section.days:
                grouped.setdefault(day, []).append(section)

        return {
            day: tuple(sorted(sections, key=lambda section: section.start))
            for day, sections in grouped.items()
        }
    def total_gap_time(self) -> int:
        total = 0

        for daily_sections in self.sections_by_day().values():
            for current, following in zip(
                daily_sections,
                daily_sections[1:]
            ):
                total += following.start - current.end

        return total
    
    def earliest_start(self) -> int:
        return min(section.start for section in self.sections)

    def latest_end(self) -> int:
        return max(section.end for section in self.sections)


        
