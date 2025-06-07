import requests
from pydantic import BaseModel, ConfigDict, Field
from utils.env_utils import get_required_env_var
from utils.http_utils import AUTH_ENDPOINT, ApiError, get_common_headers

from studyplus.api.model.auth_model import AuthModel


class AuthRepositoryReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    consumer_key: str = Field(..., alias="consumer_key")
    consumer_secret: str = Field(..., alias="consumer_secret")
    password: str = Field(..., alias="password")
    email: str = Field(..., alias="username")


class AuthRepository:
    """認証を処理するハンドラークラス"""

    def __init__(self):
        self.req = self.__new_req()

    def __new_req(self) -> AuthRepositoryReq:
        """環境変数から認証リクエストオブジェクトを作成する"""
        return AuthRepositoryReq(
            consumer_key=get_required_env_var("CONSUMER_KEY"),
            consumer_secret=get_required_env_var("CONSUMER_SECRET"),
            password=get_required_env_var("DEV_STUDYPLUS_PASSWORD"),
            email=get_required_env_var("DEV_STUDYPLUS_EMAIL"),  # pyright: ignore
        )

    def auth(self) -> AuthModel:
        """認証を実行し、アクセストークンを取得する"""
        payload = {
            "consumer_key": self.req.consumer_key,
            "consumer_secret": self.req.consumer_secret,
            "password": self.req.password,
            "username": self.req.email,
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
