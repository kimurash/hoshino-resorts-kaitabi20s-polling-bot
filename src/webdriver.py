import re
import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from models.plan import ReservationPlan


class Kaitabi20sIzumoWebDriver:
    # 界 出雲の予約ページ
    BASE_URL = "https://hoshinoresorts.com/JA/hotels/0000000132/plans/0000000053"

    FULL_SYMBOL = "×"
    CLOSED_SYMBOL = "ー"

    def __init__(self, headless: bool = False):
        self.driver = self.create_driver(headless)

    def create_driver(self, headless: bool = False):
        """
        Chrome の WebDriver を作成する

        Args:
            headless (bool, optional): ヘッドレスモードかどうか. Default は False.

        Returns:
            webdriver.Chrome: Chrome の WebDriver
        """
        options = Options()

        if headless:
            options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        return driver

    def visit(self, plan: ReservationPlan):
        """
        指定されたプランのページにアクセスする

        Args:
            plan (ReservationPlan): 予約プラン
        """
        url = f"{self.BASE_URL}?{plan.to_query_string()}"
        self.driver.get(url)

        time.sleep(2)

    def is_alert_dialog_displayed(self):
        """
        アラートダイアログが表示されているかどうかを返す

        Returns:
            bool: アラートダイアログが表示されているかどうか
        """
        alert_dialog = self.driver.find_elements(By.CSS_SELECTOR, ".v-stack-dialog__content")
        return len(alert_dialog) > 0

    def find_available_plan(self) -> date | None:
        """
        予約可能なプランを返す

        Returns:
            date | None: 予約可能なプラン. 予約可能なプランが見つからない場合は None を返す.
        """
        available_plan = None

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
                    ".content > div:not([class*='full']):not([class='null-card'])",
                )

                for calendar_cell in calendar_cells:
                    try:
                        is_available = self.is_calendar_cell_available(calendar_cell)

                        if not is_available:
                            continue

                        day = int(calendar_cell.find_element(By.CSS_SELECTOR, ".date").text.strip())
                        available_plan = date(year, month, day)
                        break

                    except NoSuchElementException:
                        continue

            except NoSuchElementException:
                continue

        return available_plan

    def is_calendar_cell_available(self, calendar_cell: WebElement) -> bool:
        """
        カレンダーのセルが予約可能かどうかを返す

        Args:
            calendar_cell (WebElement): カレンダーのセル要素

        Returns:
            bool: 予約可能かどうか
        """
        symbol = calendar_cell.find_element(By.CSS_SELECTOR, ".calender-cell > span").text.strip()

        if symbol == self.FULL_SYMBOL:
            return False

        if symbol == self.CLOSED_SYMBOL:
            return False

        return True

    def click_next_month_button(self):
        """
        次の月へ進むボタンをクリックする
        """
        calendar_before_click = self.driver.find_element(By.CSS_SELECTOR, ".c-calendar")

        wait = WebDriverWait(self.driver, 10)
        next_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".calendar-set__pagination--next"))
        )
        next_button.click()

        wait.until(EC.staleness_of(calendar_before_click))

    def close(self):
        """
        WebDriver を閉じる
        """
        self.driver.quit()
