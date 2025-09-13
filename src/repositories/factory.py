from repositories.interfaces.notification_repository import NotificationRepository
from repositories.json.notification_repository import JSONNotificationRepository


class RepositoryFactory:
    @staticmethod
    def create_notification_repository() -> NotificationRepository:
        return JSONNotificationRepository("notification.json")
