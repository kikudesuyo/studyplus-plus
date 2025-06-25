from typing import List

from api.model.user_model import UserModel
from api.repository.init_db import get_db_connection


def create_user(user_id: str, username: str):
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
        SELECT id, studyplus_user_id, name FROM user
        """
    )
    records = cur.fetchall()
    cur.close()
    return [
        UserModel(id=record[0], studyplus_id=record[1], name=record[2])
        for record in records
    ]
