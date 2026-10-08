import time
from dataclasses import fields

from . import data
from ..tests import scheduler
from . import models
from . import ranking


COURSES_FILE = "./data/courses.json"


def main() -> None:
    courses = data.load_courses(COURSES_FILE)
    user_preferences = None

    options_map = {
        "1": lambda: view_courses(courses),
        "2": lambda: build_schedules(courses),
        "3": lambda: view_ranked_schedules(courses, user_preferences),
        "4": lambda: None,
    }

    print("Welcome to the Carolina Scheduler!")

    while True:
        print(
            """
1) View sections for a course
2) View all possible schedules
3) View the best schedules based on your preferences
4) Modify/set your preferences
5) Exit
"""
        )

        user_choice = input("Please select your choice >> ").strip()

        if user_choice == "5":
            print("Exiting...")
            break

        if user_choice == "4":
            user_preferences = get_preferences()
            continue

        if user_choice not in options_map:
            print("Please select from the options above.")
            continue

        options_map[user_choice]()


def build_schedules(
    courses: dict[str, list[models.Section]],
) -> list[models.Schedule]:

    print("Generating all possible schedules...")

    start = time.perf_counter()
    schedule_list = scheduler.generate_schedules(courses)
    end = time.perf_counter()

    print(
        f"Generated {len(schedule_list)} schedules "
        f"in {end - start:.4f}s"
    )

    while True:
        user_input = input(
            "Press 'v' to view schedules or 'q' to return: "
        ).strip().lower()

        if user_input == "q":
            return schedule_list

        if user_input == "v":
            print_schedules(schedule_list)
            return schedule_list

        print("Invalid input.")


def view_ranked_schedules(
    courses: dict[str, list[models.Section]],
    preferences: models.Preferences | None,
) -> None:

    if preferences is None:
        print("Please set your preferences first.")
        return

    print("Generating schedules...")

    schedules = scheduler.generate_schedules(courses)

    ranked = ranking.rank_schedules(
        schedules,
        preferences
    )

    try:
        count = int(
            input(
                f"How many schedules would you like to view "
                f"(1-{len(ranked)})? "
            )
        )
    except ValueError:
        print("Please enter a number.")
        return

    count = max(1, min(count, len(ranked)))

    print_schedules(ranked[:count])


def get_preferences() -> models.Preferences:
    print(
        """
Enter your scheduling preferences.
Times should be entered in HH:MM format using 24-hour time.
Weights determine how important each preference is.
Use values from 0 to 5.
"""
    )

    preferred_start = ask_time(
        "Preferred earliest start time: "
    )

    preferred_end = ask_time(
        "Preferred latest end time: "
    )

    lunch_start = ask_time(
        "Earliest acceptable lunch time: "
    )

    lunch_end = ask_time(
        "Latest acceptable lunch time: "
    )

    start_weight = ask_weight(
        "Importance of avoiding early classes (0-5): "
    )

    end_weight = ask_weight(
        "Importance of avoiding late classes (0-5): "
    )

    gap_weight = ask_weight(
        "Importance of avoiding gaps (0-5): "
    )

    lunch_weight = ask_weight(
        "Importance of having a lunch break (0-5): "
    )

    while True:
        try:
            lunch_length = int(input(
                "How long should your lunch break be (in minutes): "
            ))
            break
        except ValueError:
            print("Please enter the time as a number!")


    preferences = models.Preferences(
        preferred_start=preferred_start,
        preferred_end=preferred_end,
        start_weight=start_weight,
        end_weight=end_weight,
        gap_weight=gap_weight,
        lunch_length=lunch_length,
        lunch_start=lunch_start,
        lunch_end=lunch_end,
        lunch_weight=lunch_weight,
    )

    print("Preferences updated.")

    return preferences


def ask_time(prompt: str) -> int:
    while True:
        value = input(prompt).strip()

        try:
            hours, minutes = map(int, value.split(":"))

            if not 0 <= hours <= 23:
                raise ValueError

            if not 0 <= minutes <= 59:
                raise ValueError

            return hours * 60 + minutes

        except ValueError:
            print("Enter time in HH:MM format.")


def ask_weight(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))

            if 0 <= value <= 5:
                return value

            print("Enter a value between 0 and 5.")

        except ValueError:
            print("Enter a numeric value.")


def print_schedules(
    schedules: list[models.Schedule],
) -> None:

    for index, schedule in enumerate(
        schedules,
        start=1
    ):
        print(f"\nSchedule {index}")
        print("-" * 40)

        for day, sections in schedule.sections_by_day().items():
            print(day)

            for section in sections:
                print(
                    f"  {conv_time(section.start)}-"
                    f"{conv_time(section.end)} "
                    f"{section.course} "
                    f"Section {section.section}"
                )

        print(
            f"Total gap time: "
            f"{schedule.total_gap_time()} minutes"
        )


def print_section(section: models.Section) -> None:
    for field in fields(section):
        print(
            f"{field.name}: "
            f"{getattr(section, field.name)}"
        )


def conv_time(time_msm: int) -> str:
    hours = time_msm // 60
    minutes = time_msm % 60

    return f"{hours:02d}:{minutes:02d}"


def view_courses(
    courses: dict[str, list[models.Section]],
) -> None:

    choices = {
        str(number): course
        for number, course in enumerate(
            courses.keys(),
            start=1
        )
    }

    for number, course in choices.items():
        print(f"{number}: {course}")

    while True:
        user_choice = input(
            "Enter a course number or press 'q' to exit: "
        ).strip()

        if user_choice.lower() == "q":
            return

        if user_choice not in choices:
            print(
                "Please enter a course number "
                "from the list above."
            )
            continue

        selected_course = choices[user_choice]

        for section in courses[selected_course]:
            print(
                f"""
Section number: {section.section}
Days: {"".join(section.days)}
Start time: {conv_time(section.start)}
End time: {conv_time(section.end)}
Instructor: {section.instructor}
"""
            )

        return


if __name__ == "__main__":
    main()