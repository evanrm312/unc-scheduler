import json

with open("data/courses.json") as f:
    courses = json.load(f)

print(courses["COMP 110"][0])
    
