from fastapi import APIRouter
from handler.auth_handler import get_auth
from handler.timeline_feeds_handler import get_followee_timeline_feeds

r = APIRouter()
r.add_api_route("/auth", get_auth, methods=["POST"])
r.add_api_route(
    "/timeline_feeds/followee", get_followee_timeline_feeds, methods=["GET"]
)
