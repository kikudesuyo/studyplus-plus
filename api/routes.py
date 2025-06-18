from fastapi import APIRouter
from handler.auth_handler import get_auth

r = APIRouter()
r.add_api_route("/auth", get_auth, methods=["POST"])

# sqliteに登録される
r.add_api_route("/weekly-record", lambda: None, methods=["POST"])

# 想定: mcp経由で学習記録を登録出来る
r.add_api_route("/register-record/mcp", lambda: None, methods=["POST"])
