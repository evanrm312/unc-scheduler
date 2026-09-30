import data, scheduler

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
        "5": leave
    }
    while True:
        break

def build_schedules():
    pass

def ranked_schedules():
    pass

def preferences():
    pass

def leave():
    exit()

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