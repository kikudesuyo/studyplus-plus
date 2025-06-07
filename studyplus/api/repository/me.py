from typing import Any, Dict

import requests
from utils.http_utils import ME_ENDPOINT, ApiError, get_auth_headers


class MeRepository:
    """ユーザー情報を取得するハンドラークラス"""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_me(self) -> Dict[str, Any]:
        """現在のユーザー情報を取得する"""
        headers = get_auth_headers(self.access_token)
        response = requests.get(ME_ENDPOINT, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=ME_ENDPOINT,
            )
