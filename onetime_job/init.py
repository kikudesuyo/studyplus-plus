import sqlite3

dbname = "studyplus-plus.db"
conn = sqlite3.connect(dbname)


cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        studyplus_user_id INTEGER NOT NULL UNIQUE,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)
cur.execute(
    """    
    CREATE TABLE IF NOT EXISTS winner  (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES user(id),
        win_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)

cur.executemany(
    """
    INSERT INTO user (studyplus_user_id, name) VALUES (?, ?)
    """,
    [(1, "naoki"), (2, "雅"), (3, "vin")],
)
cur.executemany(
    """
    INSERT INTO winner (user_id) VALUES (?)
    """,
    [(1,), (2,), (3,)],
)


conn.commit()
conn.close()
