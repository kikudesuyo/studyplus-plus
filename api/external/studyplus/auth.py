import httpx
from pydantic import BaseModel, ConfigDict, Field

from api.external.studyplus.http_utils import BASE_URL, ApiError, get_common_headers


class AuthReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    consumer_key: str = Field(..., alias="consumer_key")
    consumer_secret: str = Field(..., alias="consumer_secret")
    password: str = Field(..., alias="password")
    username: str = Field(..., alias="username")


class AuthRes(BaseModel):
    access_token: str = Field(..., alias="access_token")
    refresh_token: str = Field(..., alias="refresh_token")
    username: str = Field(..., alias="username")


class Auth:
    """認証を処理するハンドラークラス"""

    def __init__(self):
        self.headers = get_common_headers()

    def auth(self, req_param: AuthReq) -> AuthRes:
        """認証を実行し、アクセストークンを取得する"""
        endpoint = f"{BASE_URL}/client_auth"
        payload = {
            "consumer_key": req_param.consumer_key,
            "consumer_secret": req_param.consumer_secret,
            "password": req_param.password,
            "username": req_param.username,
        }
        try:
            response = httpx.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=0,
                message=str(e),
                endpoint=endpoint,
            )
        return AuthRes(**response.json())
