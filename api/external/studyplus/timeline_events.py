import requests

from api.external.studyplus.http_utils import BASE_URL, ApiError, get_auth_headers


class TimelineEvents:
    def __init__(self, access_token):
        self.headers = get_auth_headers(access_token)

    def like(self, event_id: int) -> None:
        """イベントにいいねをする"""
        endpoint = f"{BASE_URL}/timeline_events/{event_id}/like"
        response = requests.post(endpoint, headers=self.headers)
        if response.status_code != 200:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=endpoint,
            )

    def withdraw_like(self, event_id: int) -> None:
        """イベントのいいねを取り消す"""
        endpoint = f"{BASE_URL}/timeline_events/{event_id}/withdraw_like"
        response = requests.post(endpoint, headers=self.headers)
        if response.status_code != 200:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=endpoint,
            )
