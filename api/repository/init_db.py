import sqlite3
from contextlib import contextmanager
from sqlite3 import Connection

from api.utils.env_utils import get_required_env_var

db_name = get_required_env_var("DB_PATH")


def init_db():
    uri = f"file:{db_name}?mode=rwc"
    conn = sqlite3.connect(uri, uri=True)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studyplus_user_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS battle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        """    
        CREATE TABLE IF NOT EXISTS result   (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES user(id),
            battle_id INTEGER NOT NULL REFERENCES battle(id),
            place INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        "INSERT OR IGNORE INTO user (studyplus_user_id, name) VALUES ('1262ce7472e611e8a7090a4fa595880a', 'いく');"
    )
    cur.execute(
        "INSERT OR IGNORE INTO user (studyplus_user_id, name) VALUES ('af7f95ae365641f8a2be64b841f2978a', 'もち');"
    )
    cur.execute(
        "INSERT OR IGNORE INTO user (studyplus_user_id, name) VALUES ('914a9b5c61e34c2fbc05315f56a768c4', 'きく');"
    )
    conn.commit()
    conn.close()


@contextmanager
def get_db():
    """Returns a database connection."""
    try:
        uri = f"file:{db_name}?mode=rw"
        print(f"Connecting to database at {uri}")
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError:
        init_db()
        print("Database not found, initializing a new database.")
        uri = f"file:{db_name}?mode=rw"
        conn = sqlite3.connect(uri, uri=True)

    try:
        yield conn
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Database connection closed.")
