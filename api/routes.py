from fastapi import APIRouter

from api.handler.auth_handler import handle_get_auth
from api.handler.like_followees_timeline_records_handler import (
    handle_like_followees_record_handler,
)
from api.handler.replace_midnight_record_handler import (
    handle_replace_midnight_record_time,
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
    handle_replace_midnight_record_time,
    methods=["PUT"],
)

r.add_api_route(
    "/timeline/followees/records/like",
    handle_like_followees_record_handler,
    methods=["POST"],
)


# 想定: mcp経由で学習記録を登録出来る
r.add_api_route("/register-record/mcp", lambda: None, methods=["POST"])
