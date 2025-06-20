from datetime import datetime, timedelta, timezone
from typing import List

from pydantic import BaseModel

from api.external.gemini.client import generate_content_with_gemini
from api.external.studyplus.study_records import StudyRecord
from api.external.studyplus.timeline_feeds import BodyStudyRecord, TimelineFeeds
from api.model.user_model import UserModel, UserPlaceModel
from api.repository.study_weekly_battle import get_users, register_result

access_token_from_repo = "a5317c96-c5bd-4366-843f-a2068112ad95"
battle_material_code = "2a66f47e-3ef0-47f7-a893-b31174a392a7"


class UserStudyRecord(BaseModel):
    username: str
    nickname: str
    user_image_url: str
    duration: int
    record_datetime: str


def get_user_weekly_study_records(user_id: str, start: datetime, end: datetime):
    """ユーザーの週間学習記録を取得する"""
    timeline_feeds = TimelineFeeds(access_token_from_repo)

    weekly_study_records: List[UserStudyRecord] = []
    next_until = ""
    while True:
        feeds_res = timeline_feeds.get_user_study_feeds(user_id, next_until)
        study_records: list[BodyStudyRecord] = [
            feed.body_study_record
            for feed in feeds_res.feeds
            if feed.feed_type == "study_record" and feed.body_study_record is not None
        ]

        sorted_records = sorted(
            study_records,
            key=lambda record: datetime.strptime(
                record.record_datetime, "%Y-%m-%dT%H:%M:%SZ"
            ),
            reverse=True,
        )
        for record in sorted_records:
            record_datetime = datetime.strptime(
                record.record_datetime, "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)
            if record_datetime > end:
                continue
            if record_datetime < start:
                return weekly_study_records
            weekly_study_records.append(
                UserStudyRecord(
                    username=record.username,
                    nickname=record.nickname,
                    user_image_url=record.user_image_url or "",
                    duration=record.duration,
                    record_datetime=record.record_datetime,
                )
            )
        next_until = feeds_res.next


def get_weekly_study_records(start_utc: datetime, end_utc: datetime):
    """ユーザーの週間学習時間を取得する"""
    users = get_users()
    user_total_study_duration: List[UserTotalStudyDuration] = []
    for user in users:
        weekly_study_record = get_user_weekly_study_records(
            user.studyplus_id, start_utc, end_utc
        )
        total_duration = sum(record.duration for record in weekly_study_record)
        user_total_study_duration.append(
            UserTotalStudyDuration(
                user=user,
                total_duration=total_duration,
            )
        )

    sorted_user_durations = sorted(
        [
            UserTotalStudyDuration(
                user=duration.user,
                total_duration=duration.total_duration,
            )
            for duration in user_total_study_duration
        ],
        key=lambda x: x.total_duration,
        reverse=True,
    )

    user_places: List[UserPlaceModel] = []
    for place, duration in enumerate(sorted_user_durations, start=1):
        user_places.append(
            UserPlaceModel(
                user=duration.user,
                place=place,
                total_duration=duration.total_duration,
            )
        )

    start_jst = start_utc.astimezone(timezone(timedelta(hours=9)))
    end_jst = end_utc.astimezone(timezone(timedelta(hours=9)))
    comment = generate_weekly_battle_comment(
        start=start_jst,
        end=end_jst,
        user_places=user_places,
    )
    return comment


class UserTotalStudyDuration(BaseModel):
    user: UserModel
    total_duration: int


def register_weekly_study_battle(start: datetime, end: datetime):
    """週間学習バトルを登録する"""
    users = get_users()
    user_total_study_duration: List[UserTotalStudyDuration] = []

    for user in users:
        weekly_study_record = get_user_weekly_study_records(
            user.studyplus_id, start, end
        )
        total_duration = sum(record.duration for record in weekly_study_record)
        user_total_study_duration.append(
            UserTotalStudyDuration(
                user=user,
                total_duration=total_duration,
            )
        )

    sorted_user_durations = sorted(
        [
            UserTotalStudyDuration(
                user=duration.user,
                total_duration=duration.total_duration,
            )
            for duration in user_total_study_duration
        ],
        key=lambda x: x.total_duration,
        reverse=True,
    )

    user_places: List[UserPlaceModel] = []
    for place, duration in enumerate(sorted_user_durations, start=1):
        user_places.append(
            UserPlaceModel(
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

    study_record = StudyRecord(access_token=access_token_from_repo)
    comment = generate_weekly_battle_comment(
        start=end - timedelta(days=6, hours=23, minutes=59, seconds=59),
        end=end,
        user_places=user_places,
    )
    study_record.post(battle_material_code, 0, comment=comment)


def generate_study_battle_summary_by_gemini(user_places: List[UserPlaceModel]) -> str:
    prompt = f"""
    あなたは勉強時間バトルの結果を要約し、感情的でポジティブなトーンでコメントを生成してください。
    出力は「はい、わかりました」や「以下が結果です」などの前置きや説明を一切含めず、直接コメント本文のみを出力してください。
    
    ユーザー名:miyavin 
    一人称は「miyavin」を使用してください。
    使用する場合は、いずれかの一人称を選び、統一してください。

    勉強時間バトルの結果は、ユーザー名、順位、勉強時間を含むデータです。
    以下のデータは、1週間の勉強時間のランキングです。
    データ:
    {user_places}
    ユーザー名、順位、勉強時間をもとに、以下の条件に従ってコメントを生成してください。
    条件:
    1. コメントは日本語で書いてください。
    2. 結果を基に要約してください。
    3. 勝者を中心に、他のユーザーの努力も称える内容にしてください。
    4. コメントは感情的で、ポジティブなトーンで書いてください。
    5. あなたが勉強をするわけではないので「見習って、私も頑張る」といった表現は使用しないでください。あくまでも他者を称える内容にしてください。
    6. 他者に比べて圧倒的に勉強時間が優れている場合は、その点を強調して褒め称えてください。
    7. 他者に比べて圧倒的に勉強時間が劣っている場合は、少しだけ煽るような内容にしてください。ユーモアのある煽りをするとより良いです。    
    8. 最後に次回の勉強時間バトルへの期待感を表現してください。
    7. 各ユーザーのコメントは1~2文程度にしてください。
    8. 前置きや説明文は一切書かず、コメント本文のみを出力してください。
    """
    return generate_content_with_gemini(
        prompt=prompt,
    )


def generate_weekly_battle_comment(
    start: datetime,
    end: datetime,
    user_places: List[UserPlaceModel],
) -> str:
    """週間学習バトルの結果をコメントとして生成する"""
    sorted_user_places = sorted(user_places, key=lambda x: x.place)
    place_comments = []
    for place in sorted_user_places:
        hours = place.total_duration // 3600
        minutes = (place.total_duration % 3600) // 60
        place_comments.append(
            f"{place.place}位: {place.user.name}さん : {hours}時間{minutes}分"
        )
    place_comment = "\n".join(place_comments)

    return (
        f"📣勉強時間バトル {start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')} の結果です📣\n\n"
        + f"{place_comment}\n\n"
        + f"勝者は {sorted_user_places[0].user.name} さんです！おめでとうございます🎉\n"
        + f"miyavinからのコメントです:\n"
        + generate_study_battle_summary_by_gemini(sorted_user_places)
        + f"次回も頑張りましょう！🔥\n"
        + f"See you next week ;D"
    )
