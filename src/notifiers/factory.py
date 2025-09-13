from notifiers.interfaces.notifier import Notifier
from notifiers.slack.notifier import SlackNotifier


class NotifierFactory:
    @staticmethod
    def create_notifier() -> Notifier:
        return SlackNotifier()
