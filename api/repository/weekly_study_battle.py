from sqlite3 import Connection
from typing import List

from api.service.weekly_study_battle.model import PlaceModel


def insert_result(
    db: Connection, battle_name, start, end, user_places: List[PlaceModel]
):
    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO battle (name, start_at, end_at) VALUES (?, ?, ?)
        """,
        [battle_name, start, end],
    )
    battle_id = cur.lastrowid

    result_data = [
        (user_place.user.id, battle_id, user_place.place) for user_place in user_places
    ]
    cur.executemany(
        """INSERT INTO result (user_id, battle_id, place) VALUES (?, ?, ?)""",
        result_data,
    )

    db.commit()
    cur.close()
    db.close()
