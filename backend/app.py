from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# ----------------------------
# UPDATE THESE WITH YOUR DB DETAILS
# ----------------------------
conn = psycopg2.connect(
    host="database-2.cncm40u8c3il.ap-south-1.rds.amazonaws.com",
    database="postgres",
    user="postgres",
    password="Samitha0130"
)
# ----------------------------

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

@app.post("/register")
def register():
    data = request.json
    name = data["student_name"]
    course_id = data["course_id"]

    cur = conn.cursor()
    cur.execute("INSERT INTO registrations (student_name, course_id) VALUES (%s, %s)",
                (name, course_id))
    conn.commit()
    cur.close()

    return jsonify({"message": "✅ Registration successful"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
