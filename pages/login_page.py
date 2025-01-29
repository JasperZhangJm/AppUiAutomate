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


class LoginPage(BasePage):
    # 页面元素
    email_field = (AppiumBy.IOS_CLASS_CHAIN, EMAIL_TYPE_TEXT_FIELD_CLASS_CHAIN)
    pwd_field = (AppiumBy.IOS_CLASS_CHAIN, PWD_TYPE_SECURE_TEXT_FIELD_CLASS_CHAIN)

    region_selected_cn = (AppiumBy.IOS_CLASS_CHAIN, REGION_TYPE_TEXT_FIELD_CLASS_CHAIN_CN)
    region_field = (AppiumBy.IOS_CLASS_CHAIN, REGION_TYPE_OTHER_CLASS_CHAIN)
    region_list_CN = (AppiumBy.IOS_PREDICATE, COUNTRY_PREDICATE_CN)

    login_button = (AppiumBy.IOS_CLASS_CHAIN, LOGIN_TYPE_STATIC_TEXT_2)

    # 登录方法
    def login(self, email, password):
        self.input_text(self.email_field, email)
        self.input_text(self.pwd_field, password)

        if self.is_element_present(self.region_selected_cn) is None:
            self.click(self.region_field)
            el = self.scroll_find_element(self.region_list_CN, 180)
            el.click()

        self.click(self.login_button)
