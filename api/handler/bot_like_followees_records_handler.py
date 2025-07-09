from api.service.auth import auth
from api.service.like_record import like_followees_timeline_records_occasionally
from api.utils.env_utils import get_required_env_var


def handle_like_followees_records_by_bot():
    """
    フォロー中のユーザーの学習記録にいいねをするハンドラー

    """
    consumer_key = get_required_env_var("CONSUMER_KEY")
    consumer_secret = get_required_env_var("CONSUMER_SECRET")
    password = get_required_env_var("STUDYPLUS_PASSWORD")
    email = get_required_env_var("STUDYPLUS_EMAIL")
    res = auth(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        email=email,
        pasword=password,
    )
    access_token = res.access_token
    like_followees_timeline_records_occasionally(access_token)
    return {
        "message": "Followees' timeline records liked successfully",
    }
