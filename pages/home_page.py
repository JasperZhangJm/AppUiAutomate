from pages.base_page import BasePage
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


class HomePage(BasePage):
    # 页面元素
    drawer_icon = (AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DRAWER)
    add_icon = (AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_ADD)

    device_tab_icon = (AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DEVICES)
    cloud_tab_icon = (AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_CLOUD)
    online_support_icon = (AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_ONLINE_SUPPORT)

    # 进入首页验证方法
    def is_logged_in(self):
        if self.is_element_present(self.drawer_icon) and           \
                self.is_element_present(self.add_icon) and         \
                self.is_element_present(self.device_tab_icon) and  \
                self.is_element_present(self.cloud_tab_icon) and   \
                self.is_element_present(self.online_support_icon):
            return True
        else:
            return False
