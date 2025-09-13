import re
import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from models.plan import ReservationPlan


class Kaitabi20sIzumoWebDriver:
    BASE_URL = (
        "https://hoshinoresorts.com/JA/hotels/0000000132/plans/0000000053"  # 界 出雲の予約ページ
    )

    PAGE_LOAD_TIMEOUT = 30
    IMPLICITLY_WAIT = 30
    VISIT_MAX_RETRY = 3

    FEW_REMAINING_SYMBOL = "▲"  # 残りわずか
    FULL_SYMBOL = "×"  # 満席
    CLOSED_SYMBOL = "ー"  # 閉館

    def __init__(self, headless: bool = True):
        self.driver = self.create_driver(headless)

    def create_driver(self, headless: bool = True):
        """
        Chrome の WebDriver を作成する

        Args:
            headless (bool, optional): ヘッドレスモードかどうか. Default は True.

        Returns:
            webdriver.Chrome: Chrome の WebDriver
        """
        options = Options()

        if headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")

        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        )

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(self.IMPLICITLY_WAIT)

        return driver

    def visit(self, plan: ReservationPlan):
        """
        指定されたプランのページにアクセスする

        Args:
            plan (ReservationPlan): 予約プラン
        """
        url = f"{self.BASE_URL}?{plan.to_query_string()}"

        for attempt in range(self.VISIT_MAX_RETRY):
            try:
                if attempt == 0:
                    self.driver.get(url)
                else:
                    self.driver.refresh()

                time.sleep(2)
                break

            except Exception as e:
                if self.VISIT_MAX_RETRY - 1 <= attempt:
                    raise e

                time.sleep(2 ** (attempt + 1))

    def is_alert_dialog_displayed(self):
        """
        アラートダイアログが表示されているかどうかを返す

        Returns:
            bool: アラートダイアログが表示されているかどうか
        """
        alert_dialog = self.driver.find_elements(By.CSS_SELECTOR, ".v-stack-dialog__content")
        return len(alert_dialog) > 0

    def find_available_check_in_date(self) -> date | None:
        """
        予約可能なチェックイン日を返す

        Returns:
            date | None: 予約可能なチェックイン日. 見つからない場合は None を返す.
        """
        available_check_in_date = None

        calendar_blocks = self.driver.find_elements(By.CSS_SELECTOR, ".c-calendar")

        for calendar_block in calendar_blocks:
            try:
                header_text = calendar_block.find_element(By.CSS_SELECTOR, ".header").text
                match = re.search(r"(\d{4})年.*?(\d{1,2})月", header_text)

                if not match:
                    continue

                year, month = int(match.group(1)), int(match.group(2))

                calendar_cells = calendar_block.find_elements(
                    By.CSS_SELECTOR,
                    ".content > div:not([class='full']):not([class='null-card']):not([class='weekdays-cell'])",
                )

                for calendar_cell in calendar_cells:
                    try:
                        is_available = self.is_calendar_cell_available(calendar_cell)

                        if not is_available:
                            continue

                        day = int(calendar_cell.find_element(By.CSS_SELECTOR, ".date").text.strip())
                        available_check_in_date = date(year, month, day)
                        break

                    except NoSuchElementException:
                        continue

            except NoSuchElementException:
                continue

        return available_check_in_date

    def is_calendar_cell_available(self, calendar_cell: WebElement) -> bool:
        """
        カレンダーのセルが予約可能かどうかを返す

        Args:
            calendar_cell (WebElement): カレンダーのセル要素

        Returns:
            bool: 予約可能かどうか
        """
        # 空きありの場合をチェック
        try:
            # fmt: off
            circle_element = calendar_cell.find_element(By.CSS_SELECTOR, ".circle")  # FIXME: クラス名は予想
            # fmt: on
            if circle_element:
                return True
        except NoSuchElementException:
            pass

        # 残りわずかの場合をチェック
        try:
            triangle_element = calendar_cell.find_element(By.CSS_SELECTOR, ".triangle")
            if triangle_element:
                return True
        except NoSuchElementException:
            pass

        return True

    def click_next_month_button(self):
        """
        次の月へ進むボタンをクリックする
        """
        selectors = [
            "button.calendar-set__pagination--next",
            "button.calendar-set__pagination",
        ]

        next_button = None
        for selector in selectors:
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                break
            except NoSuchElementException:
                continue

        if next_button is None:
            return False

        if not next_button.is_displayed():
            return False

        next_button.click()
        time.sleep(2)

        return True

    def close(self):
        """
        WebDriver を閉じる
        """
        self.driver.quit()
