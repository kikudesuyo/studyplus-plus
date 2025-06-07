import requests
from utils.http_utils import (
    ApiError,
    get_auth_headers,
    like_endpoint,
    withdraw_like_endpoint,
)


class TimelineEventsRepository:
    def __init__(self, access_token):
        self.headers = get_auth_headers(access_token)

    def like(self, event_id: int) -> None:
        """イベントにいいねをする"""
        url = like_endpoint(event_id)
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )

    def withdraw_like(self, event_id: int) -> None:
        """イベントのいいねを取り消す"""
        url = withdraw_like_endpoint(event_id)
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )
