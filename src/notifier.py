import os

import requests
from dotenv import load_dotenv


class LINENotifier:
    PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"

    def __init__(self):
        load_dotenv()

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
