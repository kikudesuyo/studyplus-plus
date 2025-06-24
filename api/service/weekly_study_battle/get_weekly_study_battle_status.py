from datetime import datetime, timedelta, timezone
from typing import List

from api.repository.user import get_users
from api.service.weekly_study_battle.helper import get_user_study_records
from api.service.weekly_study_battle.helper.calculate_user_places import (
    calculate_user_places,
)
from api.service.weekly_study_battle.helper.generate_comment import generate_comment
from api.service.weekly_study_battle.helper.get_user_study_records import (
    get_user_study_records,
)
from api.service.weekly_study_battle.model import PlaceModel, TotalStudyDurationModel


def get_weekly_study_battle_status(
    start_utc: datetime, end_utc: datetime, access_token: str
) -> str:
    """ユーザーの週間学習時間を取得する"""
    users = get_users()
    user_total_study_durations: List[TotalStudyDurationModel] = []
    for user in users:
        weekly_study_record = get_user_study_records(
            user.studyplus_id, start_utc, end_utc, access_token
        )
        total_duration = sum(record.duration for record in weekly_study_record)
        user_total_study_durations.append(
            TotalStudyDurationModel(
                user=user,
                total_duration=total_duration,
            )
        )

    user_places: List[PlaceModel] = calculate_user_places(user_total_study_durations)

    start_jst = start_utc.astimezone(timezone(timedelta(hours=9)))
    end_jst = end_utc.astimezone(timezone(timedelta(hours=9)))
    comment = generate_comment(
        start=start_jst,
        end=end_jst,
        user_places=user_places,
    )
    return comment
