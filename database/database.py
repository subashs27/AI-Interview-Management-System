import sqlite3
import json

DATABASE_NAME = "knowledge.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_knowledge():

    connection = sqlite3.connect("knowledge.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT topic FROM knowledge")

    rows = cursor.fetchall()

    connection.close()

    knowledge = []

    for row in rows:

        item = get_knowledge(row["topic"])

        if item:

            knowledge.append(item)

    return knowledge

def create_database():
    """
    Creates the SQLite database and all required tables.
    Runs only once when the application starts.
    """

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    # -----------------------------
    # Table 1 : Knowledge
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        role TEXT NOT NULL,

        category TEXT NOT NULL,

        topic TEXT UNIQUE NOT NULL,

        definition TEXT,

        concepts TEXT,

        ideal_answer TEXT,

        rubric TEXT,

        common_mistakes TEXT

    )
    """)

    # -----------------------------
    # Table 2 : Questions
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        knowledge_id INTEGER,

        difficulty TEXT,

        question TEXT,

        FOREIGN KEY(knowledge_id)
        REFERENCES knowledge(id)

    )
    """)

    # -----------------------------
    # Table 3 : Interview Results
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_results(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT UNIQUE NOT NULL,

        candidate_name TEXT,

        role TEXT,

        technical_score REAL,

        voice_score REAL,

        overall_score REAL,

        weak_concepts TEXT,

        recommendation TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)
                   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_answers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        interview_id INTEGER,

        topic TEXT,

        difficulty TEXT,

        question TEXT,

        answer TEXT,

        technical_score REAL,

        communication_score REAL,

        confidence_score REAL,

        performance TEXT,

        feedback TEXT,

        followup INTEGER,

        FOREIGN KEY(interview_id)
        REFERENCES interview_results(id)

    )
    """)
    

    connection.commit()
    connection.close()

    print("✅ Database Created Successfully")


if __name__ == "__main__":
    create_database()

import json


def insert_knowledge(topic_info, knowledge_data):

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO knowledge
        (
            role,
            category,
            topic,
            definition,
            concepts,
            ideal_answer,
            rubric,
            common_mistakes
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            topic_info["role"],
            topic_info["category"],
            topic_info["topic"],
            knowledge_data["definition"],
            json.dumps(knowledge_data["concepts"]),
            knowledge_data["ideal_answer"],
            json.dumps(knowledge_data["rubric"]),
            json.dumps(knowledge_data["common_mistakes"])
        )

    )

    connection.commit()

    connection.close()

    print("✅ Knowledge Saved")

def get_knowledge(search_term):

    connection = sqlite3.connect("knowledge.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM knowledge
        WHERE
            LOWER(topic) LIKE ?
            OR LOWER(category) LIKE ?
            OR LOWER(role) LIKE ?
        """,
        (
            f"%{search_term.lower()}%",
            f"%{search_term.lower()}%",
            f"%{search_term.lower()}%"
        )
    )

    row = cursor.fetchone()

    if row is None:

        connection.close()

        return None

    cursor.execute(
        """
        SELECT difficulty,question
        FROM questions
        WHERE knowledge_id=?
        """,
        (row["id"],)
    )

    question_rows = cursor.fetchall()

    questions=[]

    for question in question_rows:

        questions.append({

            "difficulty":question["difficulty"],

            "question":question["question"]

        })

    connection.close()

    return {

        "id":row["id"],

        "role":row["role"],

        "category":row["category"],

        "topic":row["topic"],

        "definition":row["definition"],

        "concepts":json.loads(row["concepts"]),

        "ideal_answer":row["ideal_answer"],

        "rubric":json.loads(row["rubric"]),

        "common_mistakes":json.loads(row["common_mistakes"]),

        "questions":questions

    }

def insert_questions(knowledge_id, questions):

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    for question in questions:

        cursor.execute(
            """
            INSERT INTO questions
            (
                knowledge_id,
                difficulty,
                question
            )

            VALUES (?, ?, ?)
            """,
            (
                knowledge_id,
                question["difficulty"],
                question["question"]
            )
        )

    connection.commit()
    connection.close()

    print("✅ Questions Saved Successfully")

import random

def get_questions(knowledge_id, difficulty):

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT question

        FROM questions

        WHERE knowledge_id = ?

        AND difficulty = ?
        """,

        (
            knowledge_id,
            difficulty
        )
    )

    rows = cursor.fetchall()

    connection.close()

    if not rows:
        return None

    questions = [row[0] for row in rows]

    return random.choice(questions)

def insert_interview_result(result):

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interview_results
        (
            email,
            candidate_name,
            role,
            technical_score,
            communication_score,
            confidence_score,
            overall_score,
            total_questions,
            interview_duration,
            weak_concepts,
            recommendation,
            evaluations
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            result["email"],
            result["candidate_name"],
            result["role"],
            result["technical_score"],
            result["communication_score"],
            result["confidence_score"],
            result["overall_score"],
            result["total_questions"],
            result["interview_duration"],
            json.dumps(result["weak_concepts"]),
            result["recommendation"],
            json.dumps(result["evaluations"])
        )
    )

    interview_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("✅ Interview Result Saved")

    return interview_id

def insert_interview_answers(interview_id, state):

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    for question, answer, evaluation in zip(

        state.question_history,

        state.answer_history,

        state.evaluation_history

    ):

        cursor.execute(
            """
            INSERT INTO interview_answers
            (
                interview_id,
                topic,
                difficulty,
                question,
                answer,
                technical_score,
                communication_score,
                confidence_score,
                performance,
                feedback,
                followup
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (

                interview_id,

                question["topic"],

                question["difficulty"],

                question["question"],

                answer,

                evaluation["technical_score"],

                evaluation["communication_score"],

                evaluation["confidence_score"],

                evaluation["performance"],

                evaluation["feedback"],

                int(evaluation["followup_required"])

            )

        )

    connection.commit()

    connection.close()

    print("✅ Interview Answers Saved")

def get_interview_history():

    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM interview_results
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append({

            "email": row[1],

            "candidate_name": row[2],

            "role": row[3],

            "technical_score": row[4],

            "voice_score": row[5],

            "overall_score": row[6],

            "weak_concepts": json.loads(row[7]),

            "recommendation": row[8],

            "created_at": row[9]

        })

    return history

def interview_exists(email):

    connection = sqlite3.connect("knowledge.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id

        FROM interview_results

        WHERE email = ?
        """,

        (email,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None