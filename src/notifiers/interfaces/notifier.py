import os
from abc import ABC, abstractmethod
from datetime import date

from dotenv import load_dotenv


class Notifier(ABC):
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        env_path = os.path.join(current_dir, "../../.env")
        load_dotenv(env_path)

    @abstractmethod
    def notify(self, message: str):
        pass

    @abstractmethod
    def notify_available_dates(self, dates: list[date]):
        """
        予約可能な日付を箇条書きで通知する

        Args:
            dates (list[date]): 予約可能な日付のリスト
        """
        pass
