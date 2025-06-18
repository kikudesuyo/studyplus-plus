from repository.init_db import get_db_connection


def register_weekly_study_battle(user_id: str, username: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO user (studyplus_user_id, name) VALUES (?, ?)
        """,
        (user_id, username),
    )
    conn.commit()
    cur.close()


def get_weekly_study_records():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM user
        """
    )
    records = cur.fetchall()
    cur.close()
    return records
