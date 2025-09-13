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

        dates_text = []
        for available_date in available_dates:
            dates_text.append(f"• {available_date.strftime('%Y/%m/%d')}")

        block_text = "\n".join(dates_text)

        requests.post(
            self.webhook_url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "text": "予約可能なプランが見つかりました:",
                "blocks": block_text,
            },
        )
