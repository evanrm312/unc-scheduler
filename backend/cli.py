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
    """
    )
    while True:
        pass

def conv_time(time_msm: int):

def print_schedules(schedules: dict = None):
    if schedules is None:
        schedules = scheduler.generate_schedules(data.load_courses())
    course_number = 1
    for course, sections in schedules.items():
        print(f"{course_number}: {course}")
        course_number += 1
    user_choice = ""
    while True:
        try:
            user_choice = input("Enter the course you would like to view sections for or press 'q' to exit")
            if user_choice.lower() == 'q':
                print("Exiting...")
                break
            user_choice = int(user_choice)
            if not (0 < user_choice < len(schedules.keys())):
                print("Please enter a valid choice")
            else:
                break
        except TypeError:
            print("Please enter a number or press 'q' to exit")



print_schedules()