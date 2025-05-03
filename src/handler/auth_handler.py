import requests
from pydantic import BaseModel, ConfigDict, Field

from utils.env_utils import get_required_env_var
from utils.http_utils import AUTH_ENDPOINT, get_common_headers, ApiError


class AuthReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    consumer_key: str = Field(..., alias="consumer_key")
    consumer_secret: str = Field(..., alias="consumer_secret")
    password: str = Field(..., alias="password")
    email: str = Field(..., alias="username")


class AuthRes(BaseModel):
    access_token: str
    refresh_token: str
    username: str


class AuthHandler:
    """認証を処理するハンドラークラス"""
    
    def __init__(self):
        self.req = self.__new_req()

    def __new_req(self) -> AuthReq:
        """環境変数から認証リクエストオブジェクトを作成する"""
        email = get_required_env_var("STUDYPLUS_EMAIL")
        password = get_required_env_var("STUDYPLUS_PASSWORD") 
        consumer_key = get_required_env_var("CONSUMER_KEY")
        consumer_secret = get_required_env_var("CONSUMER_SECRET")
        
        return AuthReq(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            password=password,
            email=email,  # pyright: ignore
        )

    def auth(self) -> AuthRes:
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
            return AuthRes(**response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=AUTH_ENDPOINT
            )
