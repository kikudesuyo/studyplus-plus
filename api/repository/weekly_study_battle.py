from typing import List

from api.repository.init_db import get_db_connection
from api.service.weekly_study_battle.model import PlaceModel


def insert_result(battle_name, start, end, user_places: List[PlaceModel]):
    conn = get_db_connection()
    cur = conn.cursor()
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

    conn.commit()
    cur.close()
    conn.close()
