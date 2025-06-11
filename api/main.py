import logging
import os
import sqlite3

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_db():
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


def add_user():
    dbname = "studyplus-plus.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO user (studyplus_user_id, name) VALUES (?, ?)
        """,
        (4, "新しいユーザー"),
    )
    conn.commit()
    conn.close()
    logging.info("User added successfully.")
    print("User added successfully.")


def read_db():
    logging.info(f"Current directory: {os.getcwd()}")
    logging.info(f"Directory contents: {os.listdir(os.getcwd())}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir(os.getcwd())}")

    dbname = "studyplus-plus.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM user").fetchall()
    logging.info(f"Fetched data: {data}")
    print(f"Fetched data: {data}")
    return {"message": "Hello World", "data": data}


r = APIRouter()
r.add_api_route("/read", read_db, methods=["GET"])
r.add_api_route("/create", create_db, methods=["POST"])
r.add_api_route("/add_user", add_user, methods=["POST"])


app.include_router(r)
