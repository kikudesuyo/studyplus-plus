from typing import Any, Dict, Optional


class ApiError(Exception):
    """APIリクエストのエラーを表す例外クラス"""

    def __init__(
        self,
        message: str,
        endpoint: Optional[str] = None,
        status_code: Optional[int] = None,
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
