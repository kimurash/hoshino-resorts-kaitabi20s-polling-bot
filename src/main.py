from datetime import date, timedelta

from models.plan import ReservationPlan
from notifier import LINENotifier
from webdriver import Kaitabi20sIzumoWebDriver


def main():
    webdriver = Kaitabi20sIzumoWebDriver(headless=True)
    notifier = LINENotifier()

    is_candidate_plan_found = False  # ダイアログが出ないプランが見つかったかどうか

    for i in range(1, 31):  # 今日から30日後まで調べる
        check_in_date = date.today() + timedelta(days=i)
        plan = ReservationPlan(
            check_in=check_in_date,
            stay=1,
            adults=1,
            children_7_11=0,
            children_4_6=0,
            children_0_6=0,
        )

        webdriver.visit(plan)

        if not webdriver.is_alert_dialog_displayed():
            print(check_in_date)
            is_candidate_plan_found = True
            break

    if not is_candidate_plan_found:
        notifier.notify("予約可能なページが見つかりませんでした")
        return

    available_plan = webdriver.find_available_plan()

    if available_plan is not None:
        notifier.notify(f"予約可能なページが見つかりました: {available_plan}")
        return

    webdriver.click_next_month_button()
    available_plan = webdriver.find_available_plan()

    if available_plan is not None:
        notifier.notify(f"予約可能なページが見つかりました: {available_plan}")
        return

    notifier.notify("予約可能なページが見つかりませんでした")


if __name__ == "__main__":
    main()
