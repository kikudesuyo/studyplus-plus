from typing import List

from model.user_model import UserModel, UserPlaceModel
from repository.init_db import get_db_connection


def register_weekly_study_battle(user_id: str, username: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO user (studyplus_user_id, name) VALUES (?, ?)
        """,
        [user_id, username],
    )
    conn.commit()
    cur.close()


def get_users() -> List[UserModel]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT studyplus_user_id, name FROM user
        """
    )
    records = cur.fetchall()
    cur.close()
    return [UserModel(studyplus_id=record[0], name=record[1]) for record in records]


def register_result(battel_name, start, end, user_places: List[UserPlaceModel]):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO battle (name, start_at, end_at) VALUES (?, ?, ?)
        """,
        [battel_name, start, end],
    )
    battle_id = cur.lastrowid
    for user_place in user_places:
        cur.execute(
            """
            SELECT id FROM user WHERE studyplus_user_id = ?
            """,
            [user_place.user.studyplus_id],
        )
        user_row = cur.fetchone()
        if not user_row:
            raise Exception("ユーザーが登録されていません")
        user_id = user_row[0]
        cur.execute(
            """
            INSERT INTO result (user_id, battle_id, place) VALUES (?,  ?, ?)
            """,
            [user_id, battle_id, user_place.place],
        )
    conn.commit()
    cur.close()
