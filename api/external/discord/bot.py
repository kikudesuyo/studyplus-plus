import httpx

from api.utils.api_error import ApiError
from api.utils.env_utils import get_required_env_var


def send_discord_msg(msg: str) -> None:
    payload = {
        "content": msg,
        "username": "miyabi",
        "avatar_url": "https://example.com/avatar.png",
    }

    webhook_url = get_required_env_var("DISCORD_WEBHOOK_URL")
    try:
        response = httpx.post(webhook_url, json=payload)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise ApiError(
            status_code=e.response.status_code,
            message=f"[External/Discord] Failed to send message: {e.response.text}",
        )
    except httpx.RequestError as e:
        raise ApiError(
            status_code=None,
            message=f"[External/Studyplus] Communication error: {str(e)}",
        )


send_discord_msg("Hello, Discord!")
