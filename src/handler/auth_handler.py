import requests
import os
from pydantic import BaseModel, Field

class AuthReq(BaseModel):
    consumer_key: str = Field(..., alias="consumer_key")
    consumer_secret: str = Field(..., alias="consumer_secret")
    password: str = Field(..., alias="password")
    username: str = Field(..., alias="username")       

class AuthRes(BaseModel):
    access_token: str
    refresh_token: str
    username: str
    
class AuthHandler():
    def __init__(self):
        self.req = self.__new_req()
        
    def __new_req(self) -> AuthReq:
        email = os.getenv("STUDYPLUS_EMAIL")
        if not email:
            raise ValueError("STUDYPLUS_EMAIL must be set in the environment variables.")
        password = os.getenv("STUDYPLUS_PASSWORD")
        if not password:
            raise ValueError("STUDYPLUS_PASSWORD must be set in the environment variables.")
        consumer_key = os.getenv("CONSUMER_KEY")
        if not consumer_key:
            raise ValueError("CONSUMER_KEY must be set in the environment variables.")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        if not consumer_secret:
            raise ValueError(
                "CONSUMER_SECRET must be set in the environment variables."
            )
        return AuthReq(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            password=password,
            username=email,
        )
        
    def auth(self) -> AuthRes:
        url = "https://api.studyplus.jp/2/client_auth"
        payload = {
            "consumer_key": self.req.consumer_key,
            "consumer_secret": self.req.consumer_secret,
            "password": self.req.password,
            "username": self.req.username,
        }

        # リクエストヘッダーを設定
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Client-Service": "Studyplus",
            "Origin": "https://app.studyplus.jp",
            "Referer": "https://app.studyplus.jp/",
            "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"macOS"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Stpl-Client-Sp2": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

        # POSTリクエストを送信
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return AuthRes(**response.json())
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")