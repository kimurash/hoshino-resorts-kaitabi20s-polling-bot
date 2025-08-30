import urllib.parse
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ReservationPlan:
    check_in: date  # チェックイン日
    stay: int  # 泊数
    adults: int  # 大人
    children_7_11: int  # 7-11歳の子供
    children_4_6: int  # 4-6歳の子供
    children_0_6: int  # 0-6歳の子供

    def to_query_string(self):
        query_params = {
            "checkIn": self.check_in.strftime("%Y/%m/%d"),
            "stay": str(self.stay),
            "a": str(self.adults),
            "b": str(self.children_7_11),
            "c": str(self.children_4_6),
            "d": str(self.children_0_6),
        }
        return "&".join(
            [f"{key}={urllib.parse.quote(value)}" for key, value in query_params.items()]
        )
