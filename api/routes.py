from fastapi import APIRouter
from handler.auth_handler import handle_get_auth
from handler.study_weekly_battle_handler import handle_get_weekly_study_records

r = APIRouter()
r.add_api_route("/auth", handle_get_auth, methods=["POST"])
r.add_api_route(
    "/study-weekly-battle",
    handle_get_weekly_study_records,
    methods=["GET"],
)


# sqliteに登録される
r.add_api_route("/weekly-record", lambda: None, methods=["POST"])

# 想定: mcp経由で学習記録を登録出来る
r.add_api_route("/register-record/mcp", lambda: None, methods=["POST"])
