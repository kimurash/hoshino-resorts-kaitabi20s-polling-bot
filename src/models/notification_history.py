from datetime import date, datetime, timedelta

from models.notification_log import NotificationLog


class NotificationHistory:
    EXPIRED_TIME = timedelta(days=1)

    def __init__(self, logs: list[NotificationLog]) -> None:
        self.logs = logs

    def remove_expired_logs(self) -> None:
        """1日経過した通知を履歴から削除する"""

        removed_logs = []
        now = datetime.now()

        for log in self.logs:
            elapsed_time = now - log.notified_at
            if elapsed_time < self.EXPIRED_TIME:
                removed_logs.append(log)

        self.logs = removed_logs

    def is_notified(self, date: date) -> bool:
        """
        指定された通知記録が既に通知済みかどうかを確認する

        Args:
            date (date): 確認する日付

        Returns:
            bool: 通知済みかどうか
        """
        return any(date == history_log.date for history_log in self.logs)

    def append(self, log: NotificationLog) -> None:
        """
        指定された通知ログを通知済みとして記録する

        Args:
            log (NotificationLog): 通知済みとして記録する通知ログ
        """
        self.logs.append(log)

    def to_json(self) -> list[dict]:
        return [log.to_dict() for log in self.logs]
