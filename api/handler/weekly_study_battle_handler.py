from datetime import datetime, timedelta

import pytz

from api.service.weekly_study_battle.complete_weekly_study_battle import (
    complete_weekly_study_battle,
)
from api.service.weekly_study_battle.get_weekly_study_battle_status import (
    get_weekly_study_battle_status,
)


def handle_get_weekly_study_battle_status():
    """現在の週間学習バトルの進捗を取得する"""
    access_token_from_repo = "a5317c96-c5bd-4366-843f-a2068112ad95"

    now = datetime.now().astimezone(pytz.utc)
    days_to_monday = now.weekday()  # 月曜日: 0, 火曜日: 1, ..., 日曜日: 6
    recent_monday_utc = now - timedelta(days=days_to_monday)
    start_utc = recent_monday_utc.replace(
        hour=4, minute=0, second=0, microsecond=0
    ) - timedelta(hours=9)

    return get_weekly_study_battle_status(start_utc, now, access_token_from_repo)


def handle_complete_weekly_study_battle():
    """週間学習バトルを完了する
    日本時間で月曜日の4:00~23:59の間にのみ呼び出せる
    """
    access_token_from_repo = "a5317c96-c5bd-4366-843f-a2068112ad95"

    jst = pytz.timezone("Asia/Tokyo")
    now = datetime.now(jst)
    is_monday = now.weekday() == 0
    if not is_monday:
        raise ValueError("This endpoint can only be called on Mondays.")

    monday_4am_jst = now.replace(hour=4, minute=0, second=0, microsecond=0)
    if now < monday_4am_jst:
        raise ValueError("This endpoint can only be called after 4 AM JST on Monday.")

    end_utc = monday_4am_jst.astimezone(pytz.utc)
    start_utc = end_utc - timedelta(days=6, hours=23, minutes=59, seconds=59)
    complete_weekly_study_battle(start_utc, end_utc, access_token_from_repo)
    return {
        "message": "Weekly study battle registered successfully",
        "end_datetime": end_utc.isoformat(),
    }
