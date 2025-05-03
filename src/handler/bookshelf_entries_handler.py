from typing import Optional

import requests
from pydantic import BaseModel, ConfigDict, Field


class BookshelfEntriesReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    username: str = Field(..., alias="username")
    incrude_categories: bool = Field(..., alias="include_categories")
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
    def __init__(self, access_token, username):
        self.access_token = access_token
        self.username = username
        self.req = self.__new_req()

    def __new_req(self) -> BookshelfEntriesReq:
        return BookshelfEntriesReq(
            username=self.username,
            include_categories=True,
            include_drill=True,
        )

    def get_bookshelf_entries(self) -> BookshelfEntriesRes:
        url = f"https://api.studyplus.jp/2/bookshelf_entries?username={self.username}&include_categories=true&include_drill=true"
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"OAuth {self.access_token}",
            "client-service": "Studyplus",
            "content-type": "application/json; charset=utf-8",
            "origin": "https://app.studyplus.jp",
            "priority": "u=1, i",
            "referer": "https://app.studyplus.jp/",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "stpl-client-sp2": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BookshelfEntriesRes(**response.json())
        else:
            raise Exception(
                f"Failed to fetch bookshelf entries: {response.status_code} - {response.text}"
            )
