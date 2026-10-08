import pytest

from backend import models


@pytest.fixture
def make_section():
    def factory(
        course: str = "TEST 101",
        section: str = "001",
        days: list[str] | None = None,
        start: int = 9 * 60,
        end: int = 10 * 60,
        instructor: str = "Test Instructor",
    ) -> models.Section:
        return models.Section(
            course=course,
            section=section,
            days=["M"] if days is None else days,
            start=start,
            end=end,
            instructor=instructor,
        )

    return factory
