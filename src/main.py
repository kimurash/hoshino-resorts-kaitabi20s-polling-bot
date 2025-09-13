from datetime import date, timedelta

from logger import configure_logger, get_logger
from models.plan import ReservationPlan
from notifiers.factory import NotifierFactory
from notifiers.interfaces.notifier import Notifier
from repositories.factory import RepositoryFactory
from repositories.interfaces.notification_repository import NotificationRepository
from webdriver import Kaitabi20sIzumoWebDriver


def main(notify_when_unavailable: bool):
    configure_logger()

    notifier = NotifierFactory.create_notifier()
    notification_repository = RepositoryFactory.create_notification_repository()

    try:
        webdriver = Kaitabi20sIzumoWebDriver(headless=True)

        is_candidate_plan_found = find_candidate_plan(webdriver)

        if not is_candidate_plan_found:
            if notify_when_unavailable:
                notifier.notify("予約可能なプランが見つかりませんでした")

            return

        found_available_plan = find_available_plan(webdriver, notifier, notification_repository)
        if found_available_plan:
            return

        webdriver.click_next_month_button()

        found_available_plan = find_available_plan(webdriver, notifier, notification_repository)
        if found_available_plan:
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


def find_candidate_plan(webdriver: Kaitabi20sIzumoWebDriver) -> bool:
    """
    ダイアログが表示されないプランを検索する
    """
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
            return True

    return False


def find_available_plan(
    webdriver: Kaitabi20sIzumoWebDriver,
    notifier: Notifier,
    notification_repository: NotificationRepository,
) -> bool:
    """
    現在の画面から予約可能なプランを検索する

    Args:
        webdriver: Kaitabi20sIzumoWebDriver
        notifier: Notifier
        notification_repository: 通知履歴リポジトリ

    Returns:
        bool: 予約可能なプランが見つかったかどうか
    """
    available_check_in_dates = webdriver.find_available_check_in_dates()

    if available_check_in_dates:
        yet_notified_dates = []  # 未通知の日付

        # 未通知の日付を絞り込む
        for available_date in available_check_in_dates:
            if not notification_repository.is_notified(available_date):
                yet_notified_dates.append(available_date)
                notification_repository.mark_as_notified(available_date)

        # 未通知の日付があれば通知する
        if yet_notified_dates:
            notifier.notify_available_dates(yet_notified_dates)
            notification_repository.save()

            return True

    return False


if __name__ == "__main__":
    main(notify_when_unavailable=False)
