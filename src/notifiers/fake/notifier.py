from datetime import date

from notifiers.interfaces.notifier import Notifier


class FakeNotifier(Notifier):
    def notify(self, message: str):
        print(message)

    def notify_available_dates(self, available_dates: list[date]):
        print(available_dates)
