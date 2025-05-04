from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from utils.http_utils import (
    BASE_URL,
    TIMELINE_FEEDS_ENDPOINT,
    ApiError,
    get_auth_headers,
)


class LikePostReq(BaseModel):
    post_id: int


class LikePostRes(BaseModel):
    success: bool
    message: Optional[str] = None
    event_id: Optional[int] = None
    like_count: Optional[int] = None


class UserPostsRes(BaseModel):
    posts: List[Dict[str, Any]]


class TimelineFeed(BaseModel):
    feed_type: str
    body_study_record: Optional[Dict[str, Any]] = None
    feed_visibility: Optional[str] = None
    body_ads: Optional[str] = None


class TimelineResponse(BaseModel):
    current: str
    next: Optional[str] = None
    feeds: List[TimelineFeed]


class LikeHandler:
    """投稿にいいねするハンドラークラス"""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_user_posts(self, username: str, limit: int = 10) -> UserPostsRes:
        """特定のユーザーの投稿を取得する"""
        url = f"{BASE_URL}/users/{username}/study_records?limit={limit}"
        headers = get_auth_headers(self.access_token)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return UserPostsRes(posts=response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )

    def get_timeline_feeds(self, limit: int = 10) -> TimelineResponse:
        """タイムラインのフィードを取得する"""
        url = f"{TIMELINE_FEEDS_ENDPOINT}?limit={limit}"
        headers = get_auth_headers(self.access_token)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return TimelineResponse.model_validate(response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )

    def like_post(self, post_id: int) -> LikePostRes:
        """投稿にいいねする（旧API）"""
        url = f"{BASE_URL}/study_records/{post_id}/like"
        headers = get_auth_headers(self.access_token)

        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return LikePostRes(success=True)
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )

    def like_timeline_event(self, event_id: int) -> LikePostRes:
        """タイムラインイベントにいいねする"""
        url = f"{BASE_URL}/timeline_events/{event_id}/likes/like"
        headers = get_auth_headers(self.access_token)

        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return LikePostRes(
                success=True,
                event_id=data.get("event_id"),
                like_count=data.get("like_count"),
            )
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )

    def like_user_latest_posts(
        self, username: str, count: int = 5
    ) -> List[LikePostRes]:
        """特定のユーザーの最新の投稿にいいねする"""
        user_posts = self.get_user_posts(username, limit=count)

        results = []
        for post in user_posts.posts:
            post_id = post.get("id")
            if post_id:
                try:
                    result = self.like_post(post_id)
                    results.append(result)
                except ApiError as e:
                    results.append(LikePostRes(success=False, message=str(e)))

        return results

    def like_timeline_posts(self, count: int = 5) -> List[LikePostRes]:
        """タイムラインの最新の投稿にいいねする"""
        timeline = self.get_timeline_feeds(limit=count)

        results = []
        for feed in timeline.feeds:
            if feed.feed_type == "study_record" and feed.body_study_record:
                event_id = feed.body_study_record.get("event_id")
                if_you_like = feed.body_study_record.get("if_you_like", False)

                if event_id and not if_you_like:
                    try:
                        result = self.like_timeline_event(event_id)
                        results.append(result)
                    except ApiError as e:
                        results.append(LikePostRes(success=False, message=str(e)))
                elif event_id and if_you_like:
                    results.append(
                        LikePostRes(
                            success=False,
                            message=f"Event {event_id} is already liked",
                            event_id=event_id,
                        )
                    )

        return results
