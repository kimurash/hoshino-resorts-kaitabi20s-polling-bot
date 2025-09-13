import json
from pathlib import Path

from models.notification_history import NotificationHistory
from models.notification_log import NotificationLog
from repositories.interfaces.notification_history_repository import NotificationHistoryRepository


class JSONNotificationHistoryRepository(NotificationHistoryRepository):
    """JSONの通知履歴リポジトリ"""

    def __init__(self):
        pass

    def load(self, file_path: Path) -> NotificationHistory:
        """
        履歴ファイルから通知済み日付を読み出す

        Returns:
            set[date]: 通知済み日付の集合
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logs = [NotificationLog.from_dict(log) for log in data]

            return NotificationHistory(logs)

    def save(self, file_path: Path, history: NotificationHistory) -> None:
        """
        ファイルに通知履歴を保存する
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history.to_json(), f, ensure_ascii=False, indent=2)
