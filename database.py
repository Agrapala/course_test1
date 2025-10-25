import psycopg2

# ----------------------------
# UPDATE THESE WITH YOUR VALUES
# ----------------------------
RDS_HOST = "database-2.cncm40u8c3il.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Samitha0130"

# Your bucket base path (no trailing slash)
BUCKET_URL = "https://coursesami.s3.ap-south-1.amazonaws.com"

# ----------------------------

def connect():
    return psycopg2.connect(
        host=RDS_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            image_url TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id SERIAL PRIMARY KEY,
            student_name VARCHAR(100),
            course_id INT REFERENCES courses(id)
        );
    """)

    conn.commit()
    cur.close()
    print("✅ Tables created successfully")

def insert_sample_courses(conn):
    cur = conn.cursor()

    courses = [
        ("Python Basics", "Learn Python from scratch", f"{BUCKET_URL}/python.png"),
        ("AWS Essentials", "Introduction to AWS Cloud services", f"{BUCKET_URL}/aws.png"),
        ("Java Programming", "Object-oriented development in Java", f"{BUCKET_URL}/java.png")
    ]

    cur.executemany("""
        INSERT INTO courses (title, description, image_url)
        VALUES (%s, %s, %s);
    """, courses)

    conn.commit()
    cur.close()
    print("✅ Sample courses inserted successfully")

if __name__ == "__main__":
    try:
        conn = connect()
        print("✅ Connected to RDS successfully")

        create_tables(conn)
        insert_sample_courses(conn)

        conn.close()
        print("✅ Setup complete!")

    except Exception as e:
        print("❌ Error:", e)
