from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# BACKEND API URL
BACKEND_URL = os.environ.get("http://localhost:5000")   # change later when deploying to EKS

@app.get("/")
def index():
    courses = requests.get(f"{BACKEND_URL}/courses").json()
    return render_template("index.html", courses=courses)

@app.post("/register")
def register():
    name = request.form["name"]
    course_id = request.form["course_id"]
    
    requests.post(f"{BACKEND_URL}/register", json={
        "student_name": name,
        "course_id": course_id
    })
    
    return render_template("success.html", student=name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
