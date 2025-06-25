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
    for user_place in user_places:
        cur.execute(
            """
            INSERT INTO result (user_id, battle_id, place) VALUES (?,  ?, ?)
            """,
            [user_place.user.id, battle_id, user_place.place],
        )
    conn.commit()
    cur.close()
    conn.close()
