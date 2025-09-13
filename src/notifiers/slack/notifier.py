import os
from datetime import date

import requests

from notifiers.interfaces.notifier import Notifier


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

    def notify_available_dates(self, available_dates: list[date]):
        """
        予約可能な日付をSlackのBlocks形式で通知する

        Args:
            available_dates (list[date]): 予約可能な日付のリスト
        """
        if not available_dates:
            return

        lines = ["予約可能なプランが見つかりました:"]
        for available_date in available_dates:
            lines.append(f"• {available_date.strftime('%Y/%m/%d')}")

        block_text = "\n".join(lines)

        requests.post(
            self.webhook_url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": block_text,
                        },
                    },
                ],
            },
        )
