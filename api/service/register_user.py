from api.repository.user import create_user


def register_user(user_id: str, username: str):
    """ユーザーを登録する"""
    create_user(user_id, username)
