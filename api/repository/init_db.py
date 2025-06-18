import sqlite3


def get_db_connection():
    """Returns a database connection."""
    DB_NAME = "studyplus-plus.db"
    uri = f"file:{DB_NAME}?mode=rwc"
    return sqlite3.connect(uri, uri=True)
