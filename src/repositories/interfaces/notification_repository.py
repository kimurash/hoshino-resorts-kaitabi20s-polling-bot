from abc import ABC, abstractmethod
from datetime import date


class NotificationRepository(ABC):
    """通知履歴リポジトリのインターフェース"""

    @abstractmethod
    def load(self) -> None:
        """通知履歴を読み出す"""
        pass

    @abstractmethod
    def is_notified(self, date: date) -> bool:
        """
        指定された日付が既に通知済みかどうかを確認する

        Args:
            date (date): 確認する日付

        Returns:
            bool: 通知済みかどうか
        """
        pass

    @abstractmethod
    def mark_as_notified(self, date: date) -> None:
        """
        指定された日付を通知済みとして記録する

        Args:
            date (date): 通知済みとして記録する日付
        """
        pass

    @abstractmethod
    def save(self) -> None:
        """通知履歴を保存する"""
        pass
