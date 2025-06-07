from studyplus.api.repository.timeline_events import TimelineEventsRepository


def like(access_token: str, event_id: str) -> None:
    """
    タイムラインイベントにいいねをする関数

    Args:
        access_token: アクセストークン
        event_id: イベントID
    """
    timeline_events_repo = TimelineEventsRepository(access_token)
    timeline_events_repo.like(event_id=int(event_id))


def withdraw_like(access_token: str, event_id: str) -> None:
    """
    タイムラインイベントのいいねを取り消す関数

    Args:
        access_token: アクセストークン
        event_id: イベントID
    """
    timeline_events_repo = TimelineEventsRepository(access_token)
    timeline_events_repo.withdraw_like(event_id=int(event_id))
