from datetime import date, datetime, timedelta
from pathlib import Path

from logger import configure_logger, get_logger
from models.notification_history import NotificationHistory
from models.notification_log import NotificationLog
from models.plan import ReservationPlan
from notifiers.factory import NotifierFactory
from repositories.factory import RepositoryFactory
from webdriver import Kaitabi20sIzumoWebDriver


def main(notify_when_unavailable: bool):
    configure_logger()

    notifier = NotifierFactory.create_notifier()

    try:
        notification_repository = RepositoryFactory.create_notification_history_repository()

        parent_dir = Path(__file__).parent
        notification_history_file_path = parent_dir / "notification.json"

        notification_history = notification_repository.load(notification_history_file_path)
        notification_history.remove_expired_logs()
    except FileNotFoundError:
        notifier.notify("通知履歴が見つかりませんでした")
        return

    try:
        webdriver = Kaitabi20sIzumoWebDriver(headless=True)

        is_candidate_plan_found = find_candidate_plan(webdriver)

        if not is_candidate_plan_found:
            if notify_when_unavailable:
                notifier.notify("予約可能なプランが見つかりませんでした")

            return

        available_dates = find_available_dates(webdriver, notification_history)
        if available_dates:
            notifier.notify_available_dates(available_dates)
            return

        webdriver.click_next_month_button()

        available_dates = find_available_dates(webdriver, notification_history)
        if available_dates:
            notifier.notify_available_dates(available_dates)
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

        notification_repository.save(
            notification_history_file_path,
            notification_history,
        )


def find_candidate_plan(webdriver: Kaitabi20sIzumoWebDriver) -> bool:
    """
    ダイアログが表示されないプランを探す

    Args:
        webdriver: Kaitabi20sIzumoWebDriver

    Returns:
        bool: ダイアログが表示されないプランが見つかったかどうか
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


def find_available_dates(
    webdriver: Kaitabi20sIzumoWebDriver,
    notification_history: NotificationHistory,
) -> list[date]:
    """
    現在の画面から予約可能なプランを検索する

    Args:
        webdriver: Kaitabi20sIzumoWebDriver
        notification_history: NotificationHistory

    Returns:
        list[date]: 予約可能な日付のリスト
    """
    available_check_in_dates = webdriver.find_available_check_in_dates()

    if available_check_in_dates:
        yet_notified_dates = []  # 未通知の日付

        # 未通知の日付を絞り込む
        for available_date in available_check_in_dates:
            if not notification_history.is_notified(available_date):
                yet_notified_dates.append(available_date)

                notification_log = NotificationLog(
                    date=available_date,
                    notified_at=datetime.now(),
                )
                notification_history.append(notification_log)

        return yet_notified_dates

    return []


if __name__ == "__main__":
    main(notify_when_unavailable=False)
