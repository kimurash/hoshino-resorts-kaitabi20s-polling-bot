from datetime import date, timedelta

from logger import configure_logger, get_logger
from models.plan import ReservationPlan
from notifiers.notifier import Notifier
from notifiers.slack import SlackNotifier
from webdriver import Kaitabi20sIzumoWebDriver


def main(notifier: Notifier, notify_when_unavailable: bool):
    configure_logger()

    try:
        webdriver = Kaitabi20sIzumoWebDriver(headless=True)

        is_candidate_plan_found = False  # ダイアログが出ないプランが見つかったかどうか

        for i in range(1, 31):  # 今日から30日後まで調べる
            check_in_date = date.today() + timedelta(days=i)
            plan = ReservationPlan(
                check_in=check_in_date,
                stay=1,
                adults=2,
                children_7_11=0,
                children_4_6=0,
                children_0_6=0,
            )

            webdriver.visit(plan)

            if not webdriver.is_alert_dialog_displayed():
                is_candidate_plan_found = True
                break

        if not is_candidate_plan_found:
            if notify_when_unavailable:
                notifier.notify("予約可能なプランが見つかりませんでした")
            return

        available_check_in_date = webdriver.find_available_check_in_date()

        if available_check_in_date is not None:
            notifier.notify(
                f"予約可能なプランが見つかりました: {available_check_in_date.strftime('%Y/%m/%d')}"
            )
            return

        webdriver.click_next_month_button()
        available_check_in_date = webdriver.find_available_check_in_date()

        if available_check_in_date is not None:
            notifier.notify(
                f"予約可能なプランが見つかりました: {available_check_in_date.strftime('%Y/%m/%d')}"
            )
            return

        if notify_when_unavailable:
            notifier.notify("予約可能なプランが見つかりませんでした")

    except Exception as e:
        notifier.notify("予約チェック中にエラーが発生しました")

        logger = get_logger()
        logger.error("予約チェック中にエラーが発生しました")
        logger.error(e)

    finally:
        webdriver.close()


if __name__ == "__main__":
    notifier = SlackNotifier()
    main(notifier, notify_when_unavailable=False)
