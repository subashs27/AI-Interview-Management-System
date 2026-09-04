from database.database import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # -------------------------
    # Candidate
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS candidate(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT UNIQUE,

        role TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # -------------------------
    # Interview
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS interview(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        candidate_id INTEGER,

        overall_score REAL,

        technical_score REAL,

        communication_score REAL,

        confidence_score REAL,

        recommendation TEXT,

        summary TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(candidate_id)
        REFERENCES candidate(id)

    )

    """)

    # -------------------------
    # Question Results
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS question_result(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        interview_id INTEGER,

        question_no INTEGER,

        topic TEXT,

        difficulty TEXT,

        question TEXT,

        answer TEXT,

        technical REAL,

        communication REAL,

        confidence REAL,

        feedback TEXT,

        FOREIGN KEY(interview_id)
        REFERENCES interview(id)

    )

    """)

    # -------------------------
    # Strengths / Weaknesses
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS strength_weakness(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        interview_id INTEGER,

        type TEXT,

        content TEXT,

        FOREIGN KEY(interview_id)
        REFERENCES interview(id)

    )

    """)

    conn.commit()

    conn.close()