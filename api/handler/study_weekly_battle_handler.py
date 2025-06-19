from datetime import datetime, timedelta

import pytz

from api.service.study_weekly_battle import (
    get_weekly_study_records,
    register_weekly_study_battle,
)


def handle_get_weekly_study_records():
    """現在の週間学習バトルの進捗を取得する"""
    now = datetime.now().astimezone(pytz.utc)
    days_to_monday = now.weekday()  # 月曜日: 0, 火曜日: 1, ..., 日曜日: 6
    recent_monday_utc = now - timedelta(days=days_to_monday)
    start_utc = recent_monday_utc.replace(
        hour=4, minute=0, second=0, microsecond=0
    ) - timedelta(hours=9)

    return get_weekly_study_records(start_utc, now)


def handle_register_weekly_study_battle():
    """週間学習バトルを終了させる"""
    jst = pytz.timezone("Asia/Tokyo")
    now = datetime.now(jst)
    is_monday = now.weekday() == 0  # 月曜日: 0, 火曜日: 1, ..., 日曜日: 6
    if not is_monday:
        raise ValueError("This endpoint can only be called on Mondays.")

    # 1週間前の月曜日の朝4時(JST)を計算
    days_since_monday = (now.weekday() + 7) % 7  # 0=月, 6=日
    last_monday_jst = (now - timedelta(days=days_since_monday + 7)).replace(
        hour=4, minute=0, second=0, microsecond=0
    )
    end_utc = last_monday_jst.astimezone(pytz.utc)
    start_utc = end_utc - timedelta(days=6, hours=23, minutes=59, seconds=59)
    register_weekly_study_battle(start_utc, end_utc)
    return {
        "message": "Weekly study battle registered successfully",
        "end_date": last_monday_jst.strftime("%Y-%m-%d %H:%M:%S"),
    }
