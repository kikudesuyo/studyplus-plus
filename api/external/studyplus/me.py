from typing import Any, Dict

import httpx

from api.external.studyplus.request_header import BASE_URL, get_auth_headers
from api.utils.api_error import ApiError


class Me:
    """ユーザー情報を取得するハンドラークラス"""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = get_auth_headers(access_token)

    def get_me(self) -> Dict[str, Any]:
        """現在のユーザー情報を取得する"""
        endpoint = f"{BASE_URL}/me"

        try:
            response = httpx.get(endpoint, headers=self.headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=None,
                message=f"[External/Studyplus] Communication error: {str(e)}",
                endpoint=endpoint,
            )
        return response.json()
