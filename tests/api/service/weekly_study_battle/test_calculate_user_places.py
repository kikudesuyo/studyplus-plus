from typing import Dict, List, Tuple

import pytest

from api.model.user_model import UserModel
from api.service.weekly_study_battle.helper.calculate_user_places import (
    calculate_user_places,
)
from api.service.weekly_study_battle.model import TotalStudyDurationModel


@pytest.mark.parametrize(
    "input_durations, expected_ranks",
    [
        pytest.param(
            [
                ("user_c", 800),  # 2位
                ("user_a", 1000),  # 1位
                ("user_d", 800),  # 2位
                ("user_b", 500),  # 4位
            ],
            {"user_a": 1, "user_b": 4, "user_c": 2, "user_d": 2},
            id="同順位ありのケース",
        ),
        pytest.param(
            [("user_a", 100), ("user_b", 200), ("user_c", 50)],
            {"user_b": 1, "user_a": 2, "user_c": 3},
            id="同順位なしのケース",
        ),
        pytest.param(
            [("user_a", 500), ("user_b", 500), ("user_c", 500)],
            {"user_a": 1, "user_b": 1, "user_c": 1},
            id="全員が同順位のケース",
        ),
        pytest.param(
            [("user_a", 100), ("user_b", 0), ("user_c", 100)],
            {"user_a": 1, "user_c": 1, "user_b": 3},
            id="0秒を含むケース",
        ),
        pytest.param(
            [],
            {},
            id="入力が空リストのケース",
        ),
    ],
)
def test_calculate_user_places(
    input_durations: List[Tuple[str, int]],
    expected_ranks: Dict[str, int],
):
    """
    calculate_user_placesが様々な入力に対して正しく順位を計算することをテストする。
    - input_durations: (ユーザー名, 合計学習時間) のタプルのリスト
    - expected_ranks: {ユーザー名: 期待される順位} の辞書
    """
    # 1. Arrange: テストデータを作成
    user_total_study_duration = [
        TotalStudyDurationModel(
            user=UserModel(name=user_name, studyplus_id=f"{user_name}_id"),
            total_duration=duration,
        )
        for user_name, duration in input_durations
    ]

    # 2. Act: テスト対象の関数を実行
    result_places = calculate_user_places(user_total_study_duration)

    # 3. Assert: 結果を検証
    assert len(result_places) == len(expected_ranks)

    # 結果を検証しやすいように {ユーザー名: 順位} の辞書に変換
    result_ranks = {place.user.name: place.place for place in result_places}

    assert result_ranks == expected_ranks
