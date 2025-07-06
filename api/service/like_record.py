from api.external.studyplus.timeline_events import TimelineEvents
from api.external.studyplus.timeline_feeds import TimelineFeeds


def like_followees_timeline_records(access_token: str) -> None:
    """
    フォロー中のユーザー(自分自身も含む)の学習記録にいいねをする

    Note:
        直近30件分の学習記録に対して処理を行います。
        30件以上の学習記録に対して置き換えたい場合は、untilパラメータを指定してください

    Args:
        access_token: アクセストークン
    """

    timeline_feeds = TimelineFeeds(access_token)
    timeline_event = TimelineEvents(access_token)
    res = timeline_feeds.get_followee_study_feeds(until="")
    for feed in res.feeds:
        if feed.feed_type != "study_record":
            continue
        body = feed.body_study_record
        if not body:
            continue
        event_id = body.event_id
        timeline_event.like(event_id=event_id)
