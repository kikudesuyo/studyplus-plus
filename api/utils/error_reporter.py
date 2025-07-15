import traceback

from fastapi import Request

from api.external.discord.bot import send_discord_msg


class ErrorReporter:
    @staticmethod
    def report_exception(request: Request, exc: Exception):
        tb = "".join(traceback.format_exception(None, exc, exc.__traceback__))
        message = (
            f"🚨 ***Error Reported from API🚨***\n"
            f"URL: `{request.url}`\n"
            f"Method: `{request.method}`\n"
            f"エラー: `{str(exc)}`\n"
            f"Traceback:\n```{tb[:1500]}```"
        )
        send_discord_msg(message)
