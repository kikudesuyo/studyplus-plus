from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel

from utils.http_utils import BASE_URL, ApiError, get_auth_headers


class LikePostReq(BaseModel):
    post_id: int


class LikePostRes(BaseModel):
    success: bool
    message: Optional[str] = None


class UserPostsRes(BaseModel):
    posts: List[Dict[str, Any]]


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

    def like_post(self, post_id: int) -> LikePostRes:
        """投稿にいいねする"""
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
