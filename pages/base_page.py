import time
import pytest
import allure
import logging
from time import sleep
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from gz_public import is_element_present
from gz_public import scroll_find_element
from gz_public import element_until_appears
from element_constants import *
from test_data_fixture import LOGIN_DATA
from selenium.common.exceptions import NoSuchElementException


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        self.driver.find_element(*locator).click()

    def input_text(self, locator, text):
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def get_text(self, locator):
        return self.driver.find_element(*locator).text

    def is_element_present(self, locator):
        try:
            self.driver.implicitly_wait(5)
            element = self.driver.find_element(*locator)
            return element
        except NoSuchElementException:
            return None
        finally:
            self.driver.implicitly_wait(10)

    def scroll_find_element(self, locator, timeout=180):
        # 获取屏幕宽和高
        current_phone_size = self.driver.get_window_size()
        current_width = current_phone_size['width']
        current_height = current_phone_size['height']

        # 设置起始时间
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                element = self.driver.find_element(*locator)
                return element
            except NoSuchElementException:
                self.driver.swipe(
                    current_width * 1 / 2, current_height,
                    current_width * 1 / 2, current_height * 1 / 3,
                    1500
                )
        # 超时仍未找到，返回None
        return None
