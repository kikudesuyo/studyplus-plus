from api.service.like_record import like_followees_timeline_records_occasionally


def handle_like_followees_records_by_bot():
    """
    フォロー中のユーザーの学習記録にいいねをするハンドラー

    Args:
        access_token: アクセストークン
    """
    access_token = "a5317c96-c5bd-4366-843f-a2068112ad95"
    like_followees_timeline_records_occasionally(access_token)
    return {
        "message": "Followees' timeline records liked successfully",
    }
