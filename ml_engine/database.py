import sqlite3

DB_NAME = "leaderboard.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # New table structure (with resume_file column)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            name TEXT,
            job_role TEXT,
            skill_score REAL,
            semantic_score REAL,
            final_score REAL,
            resume_file TEXT
        )
    """)

    conn.commit()
    conn.close()


# Insert candidate score
def insert_score(name, job_role, skill_score, semantic_score, final_score, resume_file):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leaderboard VALUES (?, ?, ?, ?, ?, ?)
    """, (name, job_role, skill_score, semantic_score, final_score, resume_file))

    conn.commit()
    conn.close()


# Get leaderboard for selected role
def get_leaderboard(job_role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, final_score
        FROM leaderboard
        WHERE job_role=?
        ORDER BY final_score DESC
    """, (job_role,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# Role-wise analytics
def get_role_analytics():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT job_role, COUNT(*), AVG(final_score)
        FROM leaderboard
        GROUP BY job_role
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


# Top 5 resumes per role
def get_top_resumes(job_role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, resume_file, final_score
        FROM leaderboard
        WHERE job_role=?
        ORDER BY final_score DESC
        LIMIT 5
    """, (job_role,))

    rows = cursor.fetchall()
    conn.close()
    return rows
