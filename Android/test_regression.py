"""
----------------------------------
@Author: Zhang jia min
@Version: 1.0
@Date: 20241223
@desc: 回归用例
----------------------------------
"""

import pytest
import allure
import logging
import time
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

logger = logging.getLogger(__name__)


@allure.story('输入用户名和密码登录aosu app')
def test_login(appium_service, android_driver):
    master = android_driver

    # 获取登录数据
    login_data = LOGIN_DATA.get('cn_test').copy()

    # 点击 aosu 图标7次，在地区列表中出现中国
    x = master.get_window_size()['width']
    y = master.get_window_size()['height']

    xx = x//2
    yy = y//2

    for ii in range(1, 8):
        master.tap([(xx, yy)], 500)
        master.implicitly_wait(1)

    with allure.step('step1：在splash页，点击 登录 按钮'):
        master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login").click()
        master.implicitly_wait(10)

        # 断言进入了登录页面
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == "登录"

    with allure.step('step2：输入用户名'):
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].clear()
        master.implicitly_wait(10)
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].click()
        master.implicitly_wait(10)
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].send_keys(login_data['email'])

        # 输入完成后隐藏键盘
        master.hide_keyboard()

    with allure.step('step3: 输入密码'):
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].clear()
        master.implicitly_wait(10)
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].click()
        master.implicitly_wait(10)
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].send_keys(login_data['password'])

        # 输入完成后隐藏键盘
        master.hide_keyboard()

    with allure.step('step4：选择地区'):
        '''
        # 如果默认是指定的地区，那么就直接点击登录
        if master.find_elements_by_id("com.glazero.android:id/edit_text")[2].text[-3:] == region:
            time.sleep(1)
        else:
            # 如果默认不是指定的地区，那么就在地区列表中选择
        '''
        # 在回归用例中不能直接点击登录按钮，要走一遍地区选择过程
        master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[2].click()
        master.implicitly_wait(10)
        # master.find_element_by_android_uiautomator( 'new UiScrollable(new UiSelector().scrollable(
        # true)).scrollIntoView(new UiSelector().text("%s"))' % region)
        master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector('
                            ').text("%s"))' % "中国  +86")
        master.implicitly_wait(10)
        master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % "中国  +86").click()  # 此时只能写类名
        master.implicitly_wait(10)
        time.sleep(1)

    with allure.step('step5：点击 登录 按钮'):
        # 点击登录按钮之前截图
        ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        master.save_screenshot('./report/regression/login_%s.png' % ts)
        time.sleep(3)

        allure.attach.file("./report/regression/login_%s.png" % ts, name="登录页面",
                           attachment_type=allure.attachment_type.JPG)
        master.implicitly_wait(10)

        master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
        master.implicitly_wait(10)

    with allure.step('step6: 登录成功'):
        # 点击登录按钮之后即进入首页后截图截图
        time.sleep(5)
        master.save_screenshot('./report/regression/homePage.png')
        time.sleep(3)

        allure.attach.file("./report/regression/homePage.png", name="登陆成功 进入首页",
                           attachment_type=allure.attachment_type.JPG)
        master.implicitly_wait(10)

        # 登录后进入首页，有可能会弹出低电量的弹窗，发现后点击“知道了”关闭弹窗
        # while gz_public.isElementPresent(driver=master, by="id",
        #                                  value="com.glazero.android:id/btn_dialog_confirm") is True:
        #     master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_dialog_confirm").click()
        #     master.implicitly_wait(10)

        # 出现固件升级弹窗后，点击 取消/忽略此版本，多个弹窗的话，点击多次
        # while gz_public.isElementPresent(driver=master, by="id",
        #                                  value="com.glazero.android:id/inner_layout_ota_prompt") is True:
        #     master.find_elements(AppiumBy.ID, "com.glazero.android:id/button")[1].click()
        #     master.implicitly_wait(10)

        # 如果出现智能提醒，点击：知道了
        # while gz_public.isElementPresent(driver=master, by="id",
        #                                  value="com.glazero.android:id/smart_warn_iv_top_icon") is True:
        #     master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
        #     master.implicitly_wait(10)

        # 如果出现了新人礼的弹窗，点击关闭按钮
        # while gz_public.isElementPresent(driver=master, by="id",
        #                                  value="com.glazero.android:id/img_ad") is True:
        #     master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
        #     master.implicitly_wait(10)

        """
        if gz_public.isElementPresent(driver=master, by="id",
                                      value="com.glazero.android:id/inner_layout_ota_prompt") is True:
            master.find_element_by_xpath('//android.widget.Button[@text="忽略此版本"]').click()
            master.implicitly_wait(10)
        """
        time.sleep(3)

        # 没有设备的情况下启动app后会进入select model页面，兼容该页面，点击返回<，回到首页
        # if gz_public.isElementPresent(driver=master, by="id",
        #                               value="com.glazero.android:id/tv_title_string") is True:
        #     if master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title_string').text == 'Select Model':
        #         master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_title_back').click()
        #         master.implicitly_wait(10)
        # 断言是否进入首页，关键元素是：菜单按钮、logo、添加设备按钮、设备tab、回放tab、在线客服tab
        # 20230509：以下图标在1.11.18版本中已经发生变化
        assert master.current_activity in (".main.MainActivity", ".account.login.LoginActivity")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu")
        # 20230509：这个图标没有了
        # assert master.find_element_by_id("com.glazero.android:id/img_logo")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_add_device")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_playback")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_service")