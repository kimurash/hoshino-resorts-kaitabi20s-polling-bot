from repositories.interfaces.notification_history_repository import NotificationHistoryRepository
from repositories.json.notification_history_repository import JSONNotificationHistoryRepository


class RepositoryFactory:
    @staticmethod
    def create_notification_history_repository() -> NotificationHistoryRepository:
        return JSONNotificationHistoryRepository()
