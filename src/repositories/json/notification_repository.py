import json
from datetime import date
from pathlib import Path

from repositories.interfaces.notification_repository import NotificationRepository


class JSONNotificationRepository(NotificationRepository):
    """JSONの通知履歴リポジトリ"""

    def __init__(self, file_path: str):
        """
        初期化

        Args:
            file_path (str): 履歴ファイルのパス
        """
        self.file_path = Path(file_path)
        self.notified_dates = self.load()

    def load(self) -> set[date]:
        """
        履歴ファイルから通知済み日付を読み出す

        Returns:
            set[date]: 通知済み日付の集合
        """
        if not self.file_path.exists():
            return set()

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {date.fromisoformat(date_str) for date_str in data}
        except json.JSONDecodeError:
            return set()

    def is_notified(self, date: date) -> bool:
        """
        指定された日付が既に通知済みかどうかを確認する

        Args:
            date (date): 確認する日付

        Returns:
            bool: 通知済みかどうか
        """
        return date in self.notified_dates

    def mark_as_notified(self, date: date):
        """
        指定された日付を通知済みとして記録する

        Args:
            date (date): 通知済みとして記録する日付
        """
        self.notified_dates.add(date)

    def save(self):
        """
        履歴ファイルに通知済み日付を保存する
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = [d.isoformat() for d in self.notified_dates]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
