from service.register_user import register_user


def handle_register_user(user_id: str, username: str):
    """ユーザーを登録する"""
    register_user(user_id, username)
    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "username": username,
    }
