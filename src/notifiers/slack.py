import os

import requests

from notifiers.notifier import Notifier


class SlackNotifier(Notifier):
    def __init__(self):
        super().__init__()

        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def notify(self, message: str):
        requests.post(
            self.webhook_url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "text": message,
            },
        )
