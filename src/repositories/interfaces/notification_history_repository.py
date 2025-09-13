from abc import ABC, abstractmethod
from pathlib import Path

from models.notification_history import NotificationHistory


class NotificationHistoryRepository(ABC):
    """通知履歴リポジトリのインターフェース"""

    @abstractmethod
    def load(self, file_path: Path) -> NotificationHistory:
        """
        通知履歴を読み出す

        Returns:
            NotificationHistory: 通知履歴
        """
        pass

    @abstractmethod
    def save(self, file_path: Path) -> None:
        """通知履歴を保存する"""
        pass
