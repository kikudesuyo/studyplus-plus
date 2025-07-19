from fastapi import APIRouter

from api.handler.auth_handler import handle_get_auth
from api.handler.bot_like_followees_records_handler import (
    handle_like_followees_records_by_bot,
)
from api.handler.like_followees_records_handler import handle_like_followees_records
from api.handler.rewrite_midnight_record_handler import (
    handle_rewrite_midnight_record_time,
)
from api.handler.user_handler import handle_register_user
from api.handler.weekly_study_battle_handler import (
    handle_complete_weekly_study_battle,
    handle_get_weekly_study_battle_status,
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
    handle_get_weekly_study_battle_status,
    methods=["GET"],
)
r.add_api_route(
    "/weekly-study-battle",
    handle_complete_weekly_study_battle,
    methods=["POST"],
)

r.add_api_route(
    "/study-record/midnight",
    handle_rewrite_midnight_record_time,
    methods=["PUT"],
)


r.add_api_route(
    "/followees/records/like",
    handle_like_followees_records,
    methods=["POST"],
)

r.add_api_route(
    "/followees/records/like/bot",
    handle_like_followees_records_by_bot,
    methods=["POST"],
)

# 想定: mcp経由で学習記録を登録出来る
r.add_api_route("/register-record/mcp", lambda: None, methods=["POST"])
