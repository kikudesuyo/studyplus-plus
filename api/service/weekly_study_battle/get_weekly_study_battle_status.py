from datetime import datetime, timedelta, timezone
from typing import List

from api.repository.user import get_users
from api.service.weekly_study_battle.helper.generate_comment import generate_comment
from api.service.weekly_study_battle.helper.get_user_study_records import (
    get_user_study_records,
)
from api.service.weekly_study_battle.model import PlaceModel, TotalStudyDurationModel

access_token_from_repo = "a5317c96-c5bd-4366-843f-a2068112ad95"


def get_weekly_study_battle_status(start_utc: datetime, end_utc: datetime) -> str:
    """ユーザーの週間学習時間を取得する"""
    users = get_users()
    user_total_study_durations: List[TotalStudyDurationModel] = []
    for user in users:
        weekly_study_record = get_user_study_records(
            user.studyplus_id, start_utc, end_utc, access_token_from_repo
        )
        total_duration = sum(record.duration for record in weekly_study_record)
        user_total_study_durations.append(
            TotalStudyDurationModel(
                user=user,
                total_duration=total_duration,
            )
        )

    sorted_user_durations = sorted(
        [
            TotalStudyDurationModel(
                user=duration.user,
                total_duration=duration.total_duration,
            )
            for duration in user_total_study_durations
        ],
        key=lambda x: x.total_duration,
        reverse=True,
    )

    user_places: List[PlaceModel] = []
    for place, duration in enumerate(sorted_user_durations, start=1):
        user_places.append(
            PlaceModel(
                user=duration.user,
                place=place,
                total_duration=duration.total_duration,
            )
        )

    start_jst = start_utc.astimezone(timezone(timedelta(hours=9)))
    end_jst = end_utc.astimezone(timezone(timedelta(hours=9)))
    comment = generate_comment(
        start=start_jst,
        end=end_jst,
        user_places=user_places,
    )
    return comment
