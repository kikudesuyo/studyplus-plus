from studyplus.api.repository.bookshelf_entries import (
    BookshelfEntriesRepository,
    BookshelfEntriesRepositoryRes,
)


def get_bookshelf_entries(
    access_token: str, username: str
) -> BookshelfEntriesRepositoryRes:
    """本棚エントリーを取得する関数"""
    bookshelf_entries_repo = BookshelfEntriesRepository(access_token, username)
    return bookshelf_entries_repo.get_bookshelf_entries()
