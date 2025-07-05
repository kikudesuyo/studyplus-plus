from api.service.replace_midnight_record import replace_midnight_record_time


def handle_replace_midnight_record_time():
    """
    深夜の勉強記録の時間を置き換える。

    - **access_token**: ユーザーのアクセストークン
    """
    access_token = "a5317c96-c5bd-4366-843f-a2068112ad95"
    user_id = "1156ae8afada4777aeb18e78c2ce752d"
    replace_midnight_record_time(access_token, user_id)
    return {
        "message": "Midnight records replaced successfully",
    }
