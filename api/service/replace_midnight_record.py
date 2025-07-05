from datetime import datetime, timedelta

import pytz

from api.external.studyplus.study_records import StudyRecord
from api.external.studyplus.timeline_feeds import TimelineFeeds


def replace_midnight_record_time(access_token: str, user_id: str) -> None:
    """
    深夜(00:00~03:59)の勉強記録の時間を前日の23:59に置き換える

    Note:
        直近30件分の学習記録に対して処理を行います。
        30件以上の学習記録に対して置き換えたい場合は、untilパラメータを指定してください

    Args:
        access_token: アクセストークン
        user_id: ユーザーID

    """
    timeline_feed = TimelineFeeds(access_token)
    res = timeline_feed.get_user_study_feeds(until="", user_id=user_id)
    for feed in res.feeds:
        if feed.feed_type != "study_record":
            continue
        body = feed.body_study_record
        if not body:
            continue
        record_datetime = body.record_datetime
        dt = datetime.strptime(record_datetime, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=pytz.utc
        )
        jst_dt = dt.astimezone(pytz.timezone("Asia/Tokyo"))

        if 4 <= jst_dt.hour < 24:
            continue
        previous_midnight_jst = jst_dt.replace(
            hour=23, minute=59, second=0, microsecond=0
        ) - timedelta(days=1)

        updated_record_datetime = previous_midnight_jst.astimezone(pytz.utc).isoformat()
        study_record = StudyRecord(access_token)
        study_record.put(
            record_id=body.record_id,
            material_code=body.material_code,
            duration=body.duration,
            comment=body.record_comment,
            record_datetime=updated_record_datetime,
        )
