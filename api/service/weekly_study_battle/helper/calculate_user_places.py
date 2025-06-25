from itertools import groupby
from typing import List

from api.service.weekly_study_battle.model import PlaceModel, TotalStudyDurationModel


def calculate_user_places(
    user_total_study_duration: List[TotalStudyDurationModel],
) -> List[PlaceModel]:
    """
    ユーザーの合計学習時間に基づいて順位を計算する。
    同じ学習時間の場合は同じ順位を割り当てる（例: 1位, 2位, 2位, 4位）。
    """
    sorted_user_durations = sorted(
        user_total_study_duration, key=lambda x: x.total_duration, reverse=True
    )

    user_places: List[PlaceModel] = []
    current_place = 1
    for _, group in groupby(sorted_user_durations, key=lambda x: x.total_duration):
        group_list = list(group)
        for duration_model in group_list:
            user_places.append(
                PlaceModel(
                    user=duration_model.user,
                    place=current_place,
                    total_duration=duration_model.total_duration,
                )
            )
        current_place += len(group_list)
    return user_places
