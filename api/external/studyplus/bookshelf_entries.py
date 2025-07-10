from typing import Optional

import httpx
from pydantic import BaseModel, ConfigDict, Field

from api.external.studyplus.http_utils import BASE_URL, ApiError, get_auth_headers


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


class BookshelfEntriesReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    username: str = Field(..., alias="username")
    include_categories: bool = Field(..., alias="include_categories")
    include_drill: bool = Field(..., alias="include_drill")


class BookshelfEntries:
    """本棚エントリーを取得するハンドラークラス"""

    def __init__(self, access_token: str, username: str):
        self.access_token = access_token
        self.username = username
        self.req = self.__new_req()
        self.headers = get_auth_headers(access_token)

    def __new_req(self) -> BookshelfEntriesReq:
        """リクエストオブジェクトを作成する"""
        return BookshelfEntriesReq(
            username=self.username,
            include_categories=True,
            include_drill=True,
        )

    def get_bookshelf_entries(self) -> BookshelfEntriesRes:
        """本棚エントリーを取得する"""
        endpoint = f"{BASE_URL}/bookshelf_entries"
        param = self.req.model_dump(by_alias=True)

        try:
            response = httpx.get(endpoint, headers=self.headers, params=param)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
                query=param,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=None,
                message=f"[External/Studyplus] Communication error: {str(e)}",
                endpoint=endpoint,
                query=param,
            )
        return BookshelfEntriesRes(**response.json())
