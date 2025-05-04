from typing import Optional
from urllib.parse import urlencode

import requests
from pydantic import BaseModel, ConfigDict, Field

from utils.http_utils import BOOKSHELF_ENTRIES_ENDPOINT, ApiError, get_auth_headers


class BookshelfEntriesReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    username: str = Field(..., alias="username")
    include_categories: bool = Field(..., alias="include_categories")
    include_drill: bool = Field(..., alias="include_drill")


class BookshelfEntriesMaterial(BaseModel):
    material_code: str
    user_category_id: Optional[int] = None
    category_name: str
    material_title: str
    material_image_url: Optional[str] = None


class BookshelfEntriesStatus(BaseModel):
    open: Optional[list[BookshelfEntriesMaterial]] = None
    in_progress: Optional[list[BookshelfEntriesMaterial]] = None
    closed: Optional[list[BookshelfEntriesMaterial]] = None


class BookshelfEntriesRes(BaseModel):
    bookshelf_entries: BookshelfEntriesStatus


class BookshelfEntriesHandler:
    """本棚エントリーを取得するハンドラークラス"""

    def __init__(self, access_token: str, username: str):
        self.access_token = access_token
        self.username = username
        self.req = self.__new_req()

    def __new_req(self) -> BookshelfEntriesReq:
        """リクエストオブジェクトを作成する"""
        return BookshelfEntriesReq(
            username=self.username,
            include_categories=True,
            include_drill=True,
        )

    def get_bookshelf_entries(self) -> BookshelfEntriesRes:
        """本棚エントリーを取得する"""
        params = {
            "username": self.username,
            "include_categories": "true",
            "include_drill": "true",
        }
        url = f"{BOOKSHELF_ENTRIES_ENDPOINT}?{urlencode(params)}"

        headers = get_auth_headers(self.access_token)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BookshelfEntriesRes(**response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=BOOKSHELF_ENTRIES_ENDPOINT,
            )
