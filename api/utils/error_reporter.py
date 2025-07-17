import traceback
from typing import Protocol

from fastapi import Request


class Notifier(Protocol):
    def notify(self, message: str) -> None: ...


class ErrorReporter:

    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def report_exception(self, request: Request, exc: Exception):
        tb = "".join(traceback.format_exception(None, exc, exc.__traceback__))
        message = (
            f"🚨 ***Error Reported from API🚨***\n"
            f"URL: `{request.url}`\n"
            f"Method: `{request.method}`\n"
            f"エラー: `{str(exc)}`\n"
            f"Traceback:\n```{tb[:1500]}```"
        )
        self.notifier.notify(message)
