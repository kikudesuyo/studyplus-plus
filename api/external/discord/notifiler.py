from api.external.discord.bot import send_discord_msg
from api.utils.error_reporter import Notifier


class DiscordNotifier(Notifier):
    def notify(self, message: str) -> None:
        send_discord_msg(message)
