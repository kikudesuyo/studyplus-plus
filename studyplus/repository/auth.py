import requests
from model.auth_model import AuthModel
from pydantic import BaseModel, ConfigDict, Field
from utils.http_utils import AUTH_ENDPOINT, ApiError, get_common_headers


class AuthRepositoryReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    consumer_key: str = Field(..., alias="consumer_key")
    consumer_secret: str = Field(..., alias="consumer_secret")
    password: str = Field(..., alias="password")
    username: str = Field(..., alias="username")


class AuthRepository:
    """認証を処理するハンドラークラス"""

    def auth(self, req_param: AuthRepositoryReq) -> AuthModel:
        """認証を実行し、アクセストークンを取得する"""
        payload = {
            "consumer_key": req_param.consumer_key,
            "consumer_secret": req_param.consumer_secret,
            "password": req_param.password,
            "username": req_param.username,
        }

        headers = get_common_headers()

        response = requests.post(AUTH_ENDPOINT, json=payload, headers=headers)
        if response.status_code == 200:
            return AuthModel(**response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=AUTH_ENDPOINT,
            )
