from typing import Optional

from pydantic import BaseModel


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


class BookshelfEntriesModel(BaseModel):
    bookshelf_entries: BookshelfEntriesStatus
