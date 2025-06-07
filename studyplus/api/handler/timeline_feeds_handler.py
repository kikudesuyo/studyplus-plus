from studyplus.api.repository.timeline_feeds import (
    FolloweeModel,
    TimelineFeedsRepository,
)


def get_followee_timeline_feeds(access_token: str, until) -> FolloweeModel:
    """
    フォロー中のユーザーのタイムラインフィードを取得する関数

    Args:
        access_token: アクセストークン
        until: str
        フォーマット:
            "1748323851_2297584462" のような形式。
            最初の教材記録のID_最後の教材記録のID

    Returns:
        FolloweeRepositoryRes: フォロー中のユーザーのタイムラインフィード
    """
    timeline_feeds_repo = TimelineFeedsRepository(
        access_token,
    )
    return timeline_feeds_repo.get_followee_study_records(until)
