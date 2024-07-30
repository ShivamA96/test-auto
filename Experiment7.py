import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
from datetime import datetime

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.demoblaze.com/")  
        self.setup_logging()

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def setup_logging(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/test_log_{timestamp}.log"
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()

    def capture_screenshot(self, name):
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{screenshot_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(file_name)
        return file_name

    def report_pass(self, message):
        self.logger.info(f"PASS: {message}")

    def report_fail(self, message):
        self.logger.error(f"FAIL: {message}")
        screenshot = self.capture_screenshot("fail")
        self.logger.info(f"Screenshot saved: {screenshot}")


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        element = self.wait_for_element(locator)
        element.click()

    def type(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "loginusername")
    PASSWORD_FIELD = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//*[contains(@onclick, 'logIn()')]")

    def login(self, username, password):
        self.type(self.USERNAME_FIELD, username)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_page(self):
        return self.wait_for_element(self.USERNAME_FIELD).is_displayed()
    
from selenium.webdriver.common.by import By

class SearchPage(BasePage):
    SEARCH_UNIT = (By.ID, "hrefch")

    def search(self):
        self.click(self.SEARCH_UNIT)

from selenium.webdriver.common.by import By

class ArticleDetailsPage(BasePage):
    ARTICLE_TITLE = (By.ID, "name")
    ARTICLE_PRICE = (By.ID, "price-container")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn btn-success btn-lg")

    def get_article_title(self):
        return self.wait_for_element(self.ARTICLE_TITLE).text

    def get_article_price(self):
        return self.wait_for_element(self.ARTICLE_PRICE).text

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

import openpyxl

class ExcelReader:
    @staticmethod
    def get_data(file_path, sheet_name):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
        return data
    
import time

class ECommerceTest(BaseTest):
    def test_ecommerce_flow(self):
        test_data = ExcelReader.get_data("test_data.xlsx", "ecommerce_tests")

        for username, password, expected_title, expected_price in test_data:
            with self.subTest(username=username):
                login_page = LoginPage(self.driver)
                self.assertTrue(login_page.is_login_page(), "Not on login page")
                login_page.login(username, password)
                self.report_pass("Login successful")

                time.sleep(15)

                search_page = SearchPage(self.driver)
                search_page.search()
                self.report_pass(f"Search successful")


                time.sleep(15)

                article_page = ArticleDetailsPage(self.driver)
                actual_title = article_page.get_article_title()
                actual_price = article_page.get_article_price()

                self.report_pass("Article details validated successfully")

                article_page.add_to_cart()
                self.report_pass("Article added to cart")

if __name__ == "__main__":
    unittest.main()     