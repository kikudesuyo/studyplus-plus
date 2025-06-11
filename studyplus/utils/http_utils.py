from typing import Any, Dict, Optional

BASE_URL = "https://api.studyplus.jp/2"


def get_common_headers() -> Dict[str, str]:
    """APIリクエスト用の共通ヘッダーを返す"""
    return {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ja",
        "Client-Service": "Studyplus",
        "Origin": "https://app.studyplus.jp",
        "Referer": "https://app.studyplus.jp/",
        "Sec-CH-UA": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Stpl-Client-Sp2": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }


def get_auth_headers(access_token: str) -> Dict[str, str]:
    """認証済みリクエスト用のヘッダーを返す"""
    headers = get_common_headers()
    headers["Authorization"] = f"OAuth {access_token}"
    return headers


class ApiError(Exception):
    """APIリクエストのエラーを表す例外クラス"""

    def __init__(
        self,
        status_code: int,
        message: str,
        endpoint: str,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.endpoint = endpoint
        self.query = query
        self.body = body

    def __str__(self) -> str:
        return (
            f"API Error: {self.status_code} {self.message}\n"
            f"Endpoint: {self.endpoint}\n"
            f"Query: {self.query}\n"
            f"Body: {self.body}"
        )
