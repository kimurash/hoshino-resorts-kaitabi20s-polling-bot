from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class NotificationLog:
    date: date
    notified_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> NotificationLog:
        return cls(
            date=date.fromisoformat(data["date"]),
            notified_at=datetime.fromisoformat(data["notified_at"]),
        )

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "notified_at": self.notified_at.isoformat(),
        }
