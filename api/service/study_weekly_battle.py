from datetime import datetime, timedelta, timezone
from typing import List

from external.studyplus.timeline_feeds import BodyStudyRecord, TimelineFeeds
from pydantic import BaseModel
from repository.study_weekly_battle import get_user_studyplus_ids, register_winner


class UserStudyRecord(BaseModel):
    username: str
    nickname: str
    user_image_url: str
    duration: int
    record_datetime: str


def get_weekly_study_records(user_id: str, end: datetime):
    """ユーザーの週間学習記録を取得する"""
    access_token_from_repo = "a5317c96-c5bd-4366-843f-a2068112ad95"
    timeline_feeds = TimelineFeeds(access_token_from_repo)

    start = end - timedelta(days=6, hours=23, minutes=59, seconds=59)
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


def get_weekly_total_duration(user_id: str, end: datetime) -> int:
    """ユーザーの週間学習時間を取得する"""
    weekly_study_records = get_weekly_study_records(user_id, end)
    total_duration = sum(record.duration for record in weekly_study_records)
    return total_duration


def register_weekly_study_battle(end: datetime):
    """週間学習バトルを登録する"""
    user_ids = get_user_studyplus_ids()
    user_total_study_duration = {}  # key: user_id, value: total_duration
    for user_id in user_ids:
        weekly_study_record = get_weekly_study_records(user_id, end)
        total_duration = sum(record.duration for record in weekly_study_record)
        user_total_study_duration[user_id] = total_duration
    sorted_user_durations = sorted(
        user_total_study_duration.items(), key=lambda x: x[1], reverse=True
    )

    user_place = {}
    for place, (user_id, total_duration) in enumerate(sorted_user_durations, start=1):
        user_place[user_id] = place
    register_winner(
        battel_name=f"週間学習バトル {end.strftime('%Y-%m-%d')}",
        start=end - timedelta(days=6, hours=23, minutes=59, seconds=59),
        end=end,
        user_place=user_place,
    )
