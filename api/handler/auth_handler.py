from fastapi import HTTPException, status
from model.auth_model import AuthModel
from pydantic import BaseModel, EmailStr, Field
from service.auth import auth
from utils.env_utils import get_required_env_var


class AuthHandlerReq(BaseModel):
    """認証リクエストのボディ"""

    email: EmailStr = Field(
        ..., description="ユーザーのメールアドレス", examples=["user@example.com"]
    )
    password: str = Field(
        ..., description="ユーザーのパスワード", examples=["securepassword123"]
    )


def get_auth(credentials: AuthHandlerReq) -> AuthModel:
    """
    ユーザー認証を行い、アクセストークンを取得します。

    - **email**: ユーザーのメールアドレス
    - **password**: ユーザーのパスワード
    """
    try:
        consumer_key = get_required_env_var("CONSUMER_KEY")
        consumer_secret = get_required_env_var("CONSUMER_SECRET")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: Missing API credentials.",
        )
    return auth(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        email=credentials.email,
        pasword=credentials.password,
    )
