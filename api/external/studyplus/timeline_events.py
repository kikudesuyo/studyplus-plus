import httpx

from api.external.studyplus.request_header import BASE_URL, get_auth_headers
from api.utils.api_error import ApiError


class TimelineEvents:
    def __init__(self, access_token):
        self.headers = get_auth_headers(access_token)

    def like(self, event_id: int) -> None:
        """イベントにいいねをする"""
        endpoint = f"{BASE_URL}/timeline_events/{event_id}/likes/like"
        try:
            response = httpx.post(endpoint, headers=self.headers)
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

    def withdraw_like(self, event_id: int) -> None:
        """イベントのいいねを取り消す"""
        endpoint = f"{BASE_URL}/timeline_events/{event_id}/likes/withdraw_like"
        try:
            response = httpx.post(endpoint, headers=self.headers)
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
