import sqlite3

DB_NAME = "leaderboard.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            name TEXT,
            job_role TEXT,
            skill_score REAL,
            semantic_score REAL,
            final_score REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_score(name, job_role, skill_score, semantic_score, final_score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leaderboard VALUES (?, ?, ?, ?, ?)
    """, (name, job_role, skill_score, semantic_score, final_score))

    conn.commit()
    conn.close()


def get_leaderboard(job_role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, final_score FROM leaderboard
        WHERE job_role=?
        ORDER BY final_score DESC
    """, (job_role,))

    rows = cursor.fetchall()
    conn.close()
    return rows
