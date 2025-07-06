from api.service.auth import auth
from api.service.repwrite_midnight_record import repwrite_midnight_record_time
from api.utils.env_utils import get_required_env_var


def handle_repwrite_midnight_record_time():
    """
    深夜の勉強記録の時間を書き換える
    TODO: アクセストークンの取得方法をDB経由で行うように変更する

    - **access_token**: ユーザーのアクセストークン
    """
    consumer_key = get_required_env_var("CONSUMER_KEY")
    consumer_secret = get_required_env_var("CONSUMER_SECRET")
    password = get_required_env_var("DEV_STUDYPLUS_PASSWORD")
    email = get_required_env_var("DEV_STUDYPLUS_EMAIL")
    res = auth(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        email=email,
        pasword=password,
    )
    access_token = res.access_token
    user_id = res.studyplus_user_id
    repwrite_midnight_record_time(access_token, user_id)
    return {
        "message": "Midnight records replaced successfully",
    }
