from typing import Any, Dict

import requests
from utils.http_utils import BASE_URL, ApiError, get_auth_headers


class Me:
    """ユーザー情報を取得するハンドラークラス"""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = get_auth_headers(access_token)

    def get_me(self) -> Dict[str, Any]:
        """現在のユーザー情報を取得する"""
        endpoint = f"{BASE_URL}/me"

        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=endpoint,
            )
