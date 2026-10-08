from flask import Flask, jsonify, render_template

from backend import data, scheduler

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/schedules")
def get_schedules():
    courses = data.load_courses()
    schedules = scheduler.generate_schedules(courses)

    result = []

    for schedule in schedules:
        result.append({
            "sections": [
                {
                    "course": section.course,
                    "section": section.section,
                    "days": section.days,
                    "start": section.start,
                    "end": section.end,
                    "instructor": section.instructor
                }
                for section in schedule.sections
            ]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True)
