from datetime import datetime, timedelta
from typing import List

from api.external.studyplus.study_records import StudyRecord
from api.repository.user import get_users
from api.repository.weekly_study_battle import register_result
from api.service.weekly_study_battle.helper.generate_comment import generate_comment
from api.service.weekly_study_battle.helper.get_user_study_records import (
    get_user_study_records,
)
from api.service.weekly_study_battle.model import PlaceModel, TotalStudyDurationModel

BATTLE_MATERIAL_CODE = "2a66f47e-3ef0-47f7-a893-b31174a392a7"


def complete_weekly_study_battle(start: datetime, end: datetime, access_token: str):
    """週間学習バトルを完了させる"""
    users = get_users()
    user_total_study_duration: List[TotalStudyDurationModel] = []

    for user in users:
        weekly_study_record = get_user_study_records(
            user.studyplus_id, start, end, access_token
        )
        total_duration = sum(record.duration for record in weekly_study_record)
        user_total_study_duration.append(
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
            for duration in user_total_study_duration
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

    register_result(
        battel_name=f"週間学習バトル {end.strftime('%Y-%m-%d')}",
        start=end - timedelta(days=6, hours=23, minutes=59, seconds=59),
        end=end,
        user_places=user_places,
    )

    study_record = StudyRecord(access_token=access_token)
    comment = generate_comment(
        start=end - timedelta(days=6, hours=23, minutes=59, seconds=59),
        end=end,
        user_places=user_places,
    )
    study_record.post(BATTLE_MATERIAL_CODE, 0, comment=comment)
