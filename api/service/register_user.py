from api.repository.study_weekly_battle import register_weekly_study_battle


def register_user(user_id: str, username: str):
    """ユーザーを登録する"""
    register_weekly_study_battle(user_id, username)
