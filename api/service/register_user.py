from api.repository.init_db import get_db
from api.repository.user import create_user


def register_user(user_id: str, username: str):
    """ユーザーを登録する"""
    with get_db() as db:
        create_user(db, user_id, username)
