from datetime import datetime, timezone
from typing import List

from api.external.studyplus.timeline_feeds import BodyStudyRecord, TimelineFeeds
from api.service.weekly_study_battle.model import StudyRecordModel


def get_user_study_records(
    user_id: str, start: datetime, end: datetime, access_token: str
) -> List[StudyRecordModel]:
    """指定期間のユーザーの学習記録を取得する"""
    timeline_feeds = TimelineFeeds(access_token)

    weekly_study_records: List[StudyRecordModel] = []
    next_until = ""
    while True:
        feeds_res = timeline_feeds.get_user_study_feeds(user_id, next_until)
        records_in_page: list[BodyStudyRecord] = [
            feed.body_study_record
            for feed in feeds_res.feeds
            if feed.feed_type == "study_record" and feed.body_study_record is not None
        ]

        sorted_records = sorted(
            records_in_page,
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
                StudyRecordModel(
                    username=record.username,
                    nickname=record.nickname,
                    user_image_url=record.user_image_url or "",
                    duration=record.duration,
                    record_datetime=record.record_datetime,
                )
            )
        next_until = feeds_res.next
