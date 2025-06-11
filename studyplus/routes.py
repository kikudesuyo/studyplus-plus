from fastapi import APIRouter
from handler.auth_handler import get_auth

r = APIRouter()
r.add_api_route("/auth", get_auth, methods=["POST"])
