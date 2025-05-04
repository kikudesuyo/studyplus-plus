from datetime import datetime, timedelta, timezone
from typing import Optional

from handler.bookshelf_entries_handler import (BookshelfEntriesHandler,
                                               BookshelfEntriesMaterial,
                                               BookshelfEntriesRes)
from handler.study_records_handler import StudyRecordRes, StudyRecordsHandler


def get_previous_day_at_2359() -> str:
    """
    Returns the previous day's date with time set to 23:59:59 in ISO format.
    Example: "2025-05-03T23:59:59.000+09:00"
    """
    now = datetime.now(timezone(timedelta(hours=9)))  # JST timezone

    previous_day = now - timedelta(days=1)

    previous_day = previous_day.replace(hour=23, minute=59, second=59, microsecond=0)

    return previous_day.isoformat()


def select_material_from_bookshelf(
    bookshelf_entries: BookshelfEntriesRes,
) -> Optional[BookshelfEntriesMaterial]:
    """
    Selects a material from bookshelf entries.
    Tries to select from in_progress first, then open, then closed.

    Args:
        bookshelf_entries: The bookshelf entries response

    Returns:
        A selected material or None if no materials are available
    """
    if (
        bookshelf_entries.bookshelf_entries.in_progress
        and len(bookshelf_entries.bookshelf_entries.in_progress) > 0
    ):
        return bookshelf_entries.bookshelf_entries.in_progress[0]

    if (
        bookshelf_entries.bookshelf_entries.open
        and len(bookshelf_entries.bookshelf_entries.open) > 0
    ):
        return bookshelf_entries.bookshelf_entries.open[0]

    if (
        bookshelf_entries.bookshelf_entries.closed
        and len(bookshelf_entries.bookshelf_entries.closed) > 0
    ):
        return bookshelf_entries.bookshelf_entries.closed[0]

    return None


def record_previous_day_study(
    study_records_handler: StudyRecordsHandler,
    material_code: str,
    duration: int = 3600,  # Default 1 hour (3600 seconds)
    comment: Optional[str] = None,
) -> StudyRecordRes:
    """
    Records a study session for the previous day at 23:59.

    Args:
        study_records_handler: The study records handler
        material_code: The material code to record for
        duration: Study duration in seconds (default: 1 hour)
        comment: Optional comment for the study record

    Returns:
        The study record response
    """
    previous_day_timestamp = get_previous_day_at_2359()

    return study_records_handler.create_study_record(
        material_code=material_code,
        duration=duration,
        record_datetime=previous_day_timestamp,
        comment=comment,
    )


def record_previous_day_study_for_material(
    access_token: str,
    username: str,
    duration: int = 3600,
    comment: Optional[str] = None,
) -> Optional[StudyRecordRes]:
    """
    Fetches bookshelf entries, selects a material, and records a study session
    for the previous day at 23:59.

    Args:
        access_token: The access token for API authentication
        username: The username for bookshelf entries
        duration: Study duration in seconds (default: 1 hour)
        comment: Optional comment for the study record

    Returns:
        The study record response or None if no materials are available
    """
    bookshelf_entries_handler = BookshelfEntriesHandler(access_token, username)
    bookshelf_entries_res = bookshelf_entries_handler.get_bookshelf_entries()

    material = select_material_from_bookshelf(bookshelf_entries_res)
    if not material:
        print("No materials available in bookshelf")
        return None

    study_records_handler = StudyRecordsHandler(access_token)
    return record_previous_day_study(
        study_records_handler=study_records_handler,
        material_code=material.material_code,
        duration=duration,
        comment=comment,
    )
