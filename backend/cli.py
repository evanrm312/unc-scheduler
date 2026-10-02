import data, scheduler
import time

def main():
    print("Welcome to the Carolina Scheduler!")
    print("Choose from the following options:")
    print(
    """
    1) View sections for a course
    2) View all possible schedules
    3) View the best schedules based on your choices #TODO
    4) Modify/set your preferences #TODO
    5) Exit
    """
    )
    options_map = {
        "1": view_courses,
        "2": build_schedules,
        "3": ranked_schedules,
        "4": preferences,
    }
    while True:
        user_choice = input("Please select your choice >> ")
        if user_choice == "5":
            print("Exiting...")
            break
        elif user_choice not in options_map.keys():
            print("Please select from the options above.")
        else:
            options_map[user_choice]()

def build_schedules(file_name: str = "./data/courses.json"):
    # Will be changed in future, just generates all schedules for now
    print(f"Loading courses from {file_name}...")
    s = time.perf_counter()
    courses = data.load_courses(file_name)
    e = time.perf_counter()
    print(f"Loaded courses in {e-s}s")
    print("Generating all possible schedules...")
    s = time.perf_counter()
    schedule_list = scheduler.generate_schedules(courses)
    e = time.perf_counter()
    print(f"Generated {len(courses)} schedules in {e-s}s")
    while True:
        user_input = input("Press v to view all schedules or f to search: ").strip().lower()
        if user_input not in ["v", "f"]:
            print("Invalid input")
        else:
            # TODO
            


def ranked_schedules():
    pass

def preferences():
    ### short survey to get weighted values
    """
    gaps -> prioritize gaps (5) or avoid gaps if possible (1)
    start-time -> avoid classes w/ start time before this time
    day-end -> avoids classes w/ start or end times after this time
    lunch-time -> blocks classes from this time (if important)

    """
    print()

def conv_time(time_msm: int) -> str:
    hours = time_msm // 60
    minutes = time_msm % 60
    if minutes < 10:
        minutes = f"0{minutes}"
    return f"{hours}:{minutes}"

def view_courses(courses: dict = None):
    if courses is None:
        courses = data.load_courses()
    user_choice = ""
    choices = {
        str(number): course
        for number, course in enumerate(courses.keys(), start=1)
    }
    for k, v in choices.items():
        print(f"{k}: {v}")
    while True:
        user_choice = input("Enter the course you would like to view sections for or press 'q' to exit: ")
        if user_choice.lower().strip() == 'q':
            print("Exiting...")
            return
        if user_choice not in choices.keys():
            print("Please enter a course number from the list above.")
        else:
            for section in courses[choices[user_choice]]:
                print(
                    f"""
                    Section number: {section.section}
                    Days: {"".join(section.days)}
                    Start time: {conv_time(section.start)}
                    End time: {conv_time(section.end)}
                    Instructor: {section.instructor}
                    """
                )
            break

main()