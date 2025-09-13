import os
from datetime import date

import requests

from notifiers.interfaces.notifier import Notifier


class LINENotifier(Notifier):
    PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"

    def __init__(self):
        super().__init__()

        self.user_id = os.getenv("LINE_USER_ID")
        self.channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    def notify(self, message: str):
        response = requests.post(
            self.PUSH_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.channel_access_token}",
            },
            json={
                "to": self.user_id,
                "messages": [{"type": "text", "text": message}],
            },
        )

        response.raise_for_status()

    def notify_available_dates(self, available_dates: list[date]):
        raise NotImplementedError
