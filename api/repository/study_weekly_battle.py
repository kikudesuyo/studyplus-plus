from typing import Dict, List

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


def get_user_studyplus_ids() -> List[str]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT studyplus_user_id FROM user
        """
    )
    records = cur.fetchall()
    cur.close()
    return [record[0] for record in records]


def register_winner(battel_name, start, end, user_place: Dict[str, int]):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO battle (name, start_at, end_at) VALUES (?, ?, ?)
        """,
        (battel_name, start, end),
    )
    battle_id = cur.lastrowid
    for user_id, place in user_place.items():
        cur.execute(
            """
            INSERT INTO result (user_id, battle_id, place) VALUES (?,  ?, ?)
            """,
            (user_id, battle_id, place),
        )
    conn.commit()
    cur.close()
