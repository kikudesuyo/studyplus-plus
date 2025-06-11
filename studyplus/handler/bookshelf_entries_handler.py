from model.bookshelf_entries_model import BookshelfEntriesModel
from repository.bookshelf_entries import BookshelfEntriesRepository


def get_bookshelf_entries(access_token: str, username: str) -> BookshelfEntriesModel:
    """本棚エントリーを取得する関数"""
    bookshelf_entries_repo = BookshelfEntriesRepository(access_token, username)
    return bookshelf_entries_repo.get_bookshelf_entries()
