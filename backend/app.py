from flask import Flask, request, jsonify
import psycopg2, os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Use environment variables instead of hard-coded values
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

# ----------------------------

# Get all courses
@app.get("/courses")
def get_courses():
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, image_url FROM courses;")
    rows = cur.fetchall()
    cur.close()

    result = [
        {"id": r[0], "title": r[1], "description": r[2], "image_url": r[3]}
        for r in rows
    ]
    return jsonify(result)


# Register a student for a course
@app.post("/register")
def register():
    data = request.json
    name = data.get("student_name")
    course_id = data.get("course_id")

    if not name or not course_id:
        return jsonify({"error": "Missing student_name or course_id"}), 400

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registrations (student_name, course_id) VALUES (%s, %s)",
        (name, course_id)
    )
    conn.commit()
    cur.close()

    return jsonify({"message": "✅ Registration successful"})


# Get all registrations
@app.get("/registrations")
def get_registrations():
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, r.student_name, c.title
        FROM registrations r
        JOIN courses c ON r.course_id = c.id;
    """)
    rows = cur.fetchall()
    cur.close()

    result = [
        {"id": r[0], "student_name": r[1], "course_title": r[2]}
        for r in rows
    ]
    return jsonify(result)


# Get registrations for a specific course
@app.get("/courses/<int:course_id>/registrations")
def course_registrations(course_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT student_name
        FROM registrations
        WHERE course_id = %s;
    """, (course_id,))
    rows = cur.fetchall()
    cur.close()

    result = [r[0] for r in rows]
    return jsonify({"course_id": course_id, "students": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
