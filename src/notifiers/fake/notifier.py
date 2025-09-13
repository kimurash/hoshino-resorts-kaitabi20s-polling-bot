from datetime import date


class FakeNotifier:
    def notify(self, message: str):
        print(message)

    def notify_available_dates(self, available_dates: list[date]):
        print(available_dates)
