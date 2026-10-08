from backend import models


def test_sections_by_day_groups_and_sorts_sections(make_section):
    late = make_section(section="002", days=["M", "W"], start=11 * 60, end=12 * 60)
    early = make_section(section="001", days=["M"], start=9 * 60, end=10 * 60)
    schedule = models.Schedule((late, early))

    grouped = schedule.sections_by_day()

    assert grouped["M"] == (early, late)
    assert grouped["W"] == (late,)


def test_total_gap_time_sums_gaps_across_days(make_section):
    monday_early = make_section(section="001", days=["M"], start=9 * 60, end=10 * 60)
    monday_late = make_section(section="002", days=["M"], start=11 * 60, end=12 * 60)
    tuesday_early = make_section(section="003", days=["T"], start=10 * 60, end=11 * 60)
    tuesday_late = make_section(section="004", days=["T"], start=11 * 60 + 30, end=12 * 60)
    schedule = models.Schedule(
        (monday_late, tuesday_late, monday_early, tuesday_early)
    )

    assert schedule.total_gap_time() == 90


def test_adjacent_sections_have_no_gap(make_section):
    first = make_section(section="001", start=9 * 60, end=10 * 60)
    second = make_section(section="002", start=10 * 60, end=11 * 60)

    assert models.Schedule((first, second)).total_gap_time() == 0


def test_earliest_start_and_latest_end(make_section):
    first = make_section(section="001", start=8 * 60 + 30, end=9 * 60 + 30)
    second = make_section(section="002", start=14 * 60, end=15 * 60 + 15)
    schedule = models.Schedule((second, first))

    assert schedule.earliest_start() == 8 * 60 + 30
    assert schedule.latest_end() == 15 * 60 + 15
