from fastapi import APIRouter

from api.handler.auth_handler import handle_get_auth
from api.handler.register_user_handler import handle_register_user
from api.handler.study_weekly_battle_handler import (
    handle_get_weekly_study_records,
    handle_register_weekly_study_battle,
)

r = APIRouter()


r.add_api_route(
    "/auth",
    handle_get_auth,
    methods=["POST"],
)
r.add_api_route(
    "/register-user",
    handle_register_user,
    methods=["GET"],
)

r.add_api_route(
    "/weekly-study-battle",
    handle_get_weekly_study_records,
    methods=["GET"],
)
r.add_api_route(
    "/weekly-study-battle",
    handle_register_weekly_study_battle,
    methods=["POST"],
)


# 想定: mcp経由で学習記録を登録出来る
r.add_api_route("/register-record/mcp", lambda: None, methods=["POST"])
