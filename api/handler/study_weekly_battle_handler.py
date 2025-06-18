from datetime import datetime, timedelta

import pytz
from service.study_weekly_battle import get_weekly_study_records


def handle_get_weekly_study_records(user_id: str):
    """ユーザーの学習記録を取得する"""
    jst = pytz.timezone("Asia/Tokyo")
    now = datetime.now(jst)
    # is_monday = now.weekday() == 0  # 月曜日: 0, 火曜日: 1, ..., 日曜日: 6
    # if not is_monday:
    #     raise ValueError("This endpoint can only be called on Mondays.")
    last_sunday_jst = now.replace(hour=23, minute=59, second=59) - timedelta(days=1)
    last_sunday_utc = last_sunday_jst.astimezone(pytz.utc)
    return get_weekly_study_records(user_id, last_sunday_utc)
