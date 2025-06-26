from sqlite3 import Connection
from typing import List

from api.model.user_model import UserModel


def create_user(db: Connection, user_id: str, username: str):
    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO user (studyplus_user_id, name) VALUES (?, ?)
        """,
        [user_id, username],
    )
    db.commit()
    cur.close()


def get_users(db: Connection) -> List[UserModel]:
    cur = db.cursor()
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
