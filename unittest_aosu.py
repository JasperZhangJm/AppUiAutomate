# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import time
from time import sleep
import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from func_timeout import func_timeout, FunctionTimedOut
from func_timeout import func_set_timeout
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import Interaction
from appium import webdriver
from element_constants import *

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'


def test_get_text(appium_service, ios_driver):
    driver = ios_driver
    region = driver.find_element(AppiumBy.IOS_CLASS_CHAIN, REGION_TYPE_TEXT_FIELD_CLASS_CHAIN_CN).text
    print("begin:")
    print(f"region is {region}")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-ra", "test_get_text"])


"""
def test_w3c_action(appium_service, ios_driver):
    driver = ios_driver
    actions = ActionChains(driver)
    actions.click_and_hold().move_by_offset(100, 0).release().perform()
"""

"""
def test_pull_down_refresh(appium_service, ios_driver, screen_size):
    driver = ios_driver
    x, y = screen_size
    s_x = x * 0.50
    s_y = y * 0.25
    e_x = x * 0.5
    e_y = y * 0.75
    driver.swipe(s_x, s_y, e_x, e_y, 500)
    #driver.execute_script("mobile: swipe", {"startX": s_x,
    #                                        "startY": s_y,
    #                                        "endX": e_x,
    #                                        "endY": e_y,
    #                                        "duration": 500,
    #                                        "direction": "down"})
"""

"""
def test_right_swipe(appium_service, ios_driver):
    driver = ios_driver
    driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN)
    screen_weight = driver.get_window_size()['width']
    screen_height = driver.get_window_size()['height']
    from_x = 0
    from_y = screen_height * 0.5
    to_x = screen_weight
    to_y = screen_height * 0.5
    duration = 0.2
    #print(phone_weight, phone_height)
    #s_x = phone_weight * 0.9
    #e_x = phone_weight * 0.1
    #y = phone_height * 0.5
    #actions = TouchAction(driver)
    #actions.press(x=300, y=400,).move_to(x=75, y=400).release().perform()
    driver.execute_script("mobile: dragFromToForDuration", {
                                            "fromX": from_x,
                                            "fromY": from_y,
                                            "toX": to_x,
                                            "toY": to_y,
                                            "duration": duration
                                            })
    """
"""
    driver.execute_script("mobile: swipe", {"startX": 0,
                                            "startY": 500,
                                            "endX": 200,
                                            "endY": 500,
                                            "duration": 1000,
                                            "direction": "right"})
"""

"""
@pytest.fixture(scope='session')
def appium_service():
    service = AppiumService()
    service.start(
        args=['--address', APPIUM_HOST, '--port', str(APPIUM_PORT)],
        timeout_ms=20000
    )
    yield service
    service.stop()


def create_ios_driver(custom_opts=None):
    options = XCUITestOptions()
    # iPhoneXR
    # options.platform_version = '17.1.2'
    # options.udid = '00008020-001828440A69002E'

    # iPhoneX
    # options.platform_version = '16.5.1'
    # options.udid = 'f89d929e8c45a81c0fe2d22f80c1a36e227e90ef'
    # options.set_capability("useNewWDA", True)

    # 模拟器，iPhone14pro
    # options.platform_version = '16.2'
    # options.udid = '4EC1EBA2-0FB0-431D-B663-E5992132CC21'

    if custom_opts is not None:
        options.load_capabilities(custom_opts)
    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)


@pytest.fixture
def ios_driver_factory():
    return create_ios_driver


@pytest.fixture
def ios_driver():
    driver = create_ios_driver()
    yield driver
    driver.quit()


def test_ios_click(appium_service, ios_driver_factory):
    with ios_driver_factory({
        # 示例程序UICatalog
        # 'appium:app': 'com.example.zjm.UICatalog',
        'platformName': 'iOS',
        # 'appium:app': 'com.glazero.ios',
        # 'appium:bundled': 'com.glazero.ios',
        'appium:udid': 'f89d929e8c45a81c0fe2d22f80c1a36e227e90ef',
        'appium:automationName': 'XCUITest',
        'appium:platformVersion': '16.5.1'
        # 'appium:bundleId': 'com.glazero.ios',
        # 'appium:xcodeOrgId': 'D56XGY9WS7',
        # 'appium:xcodeOrgId': 'WN595JYUJX',
        # 'appium:xcodeOrgId': 'WN595JYUJX',
        # 'appium:xcodeSigningId': 'iPhone Distribution'
        # Apple Developer 也可以，没有区别
        # 'appium:xcodeSigningId': 'iPhone Developer',
        # 'appium: updatedWDABundleId': 'glazero.qa.WebDriverAgentRunner'
        # 'appium:showXcodeLog': True
    }) as driver:
        # el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Buttons')
        # el = driver.find_element(by=AppiumBy.ID, value='0C000000-0000-0000-474E-010000000000')
        # el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='0C000000-0000-0000-474E-010000000000')
        # el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='登录')
        driver.activate_app('com.glazero.ios')

        current_phone_size = driver.get_window_size()

        current_width = current_phone_size['width']
        print('\n')
        print(current_width)

        current_height = current_phone_size['height']
        print(current_height)
        print('\n')

        # driver.execute_script('mobile:dragFromToForDuration', {'duration': 200, 'fromX': current_width * 1 / 2,
        # 'fromY': current_height, 'toX': current_width * 1 / 2, 'toY': 0})

        # driver.swipe(current_width * 1 / 2, current_height * 4 / 5, current_width * 1 / 2, current_height * 1 / 5,
        # 100)

        # for i in range(1, 30):
        # driver.swipe(current_width * 1 / 2, current_height, current_width * 1 / 2, current_height * 1 / 3, 1500)
        # sleep(2)

        # driver.find_element(by=AppiumBy.ID, value='	中国 +86')
        # driver.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypeStaticText[@name=" 中国 +86"]')
        # driver.find_element(by=AppiumBy.IOS_PREDICATE, value='name LIKE "*+86*"')
        # driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value='**/XCUIElementTypeStaticText[`name == " 中国 +86"`]')

        # sleep(3)

        # driver.flick(200, 800, 200, 200)

        # ok
        # 要设置超时时间
        @func_set_timeout(180)
        def scroll_find_element(by, value):
            while 1:
                try:
                    element = driver.find_element(by=by, value=value)
                    # driver.find_element(
                    # by=AppiumBy.IOS_CLASS_CHAIN, value='**/XCUIElementTypeStaticText[`name == " 中国 +86"`]') source =
                    # driver.page_source print('Page Source: ', source) driver.find_element(by=AppiumBy.XPATH,
                    # value='//XCUIElementTypeStaticText[@name=" 中国 +86"]')
                    # driver.find_element(by=AppiumBy.ID, value="   中国  +86")
                except Exception as e:
                    if e:
                        driver.swipe(current_width * 1 / 2, current_height, current_width * 1 / 2, current_height * 1 / 3,
                                     1500)
                        # print(ele)
                        # return ele
                else:
                    # print("111111111")
                    return element

        ele = scroll_find_element(AppiumBy.IOS_PREDICATE, 'name == "   中国  +86" AND visible == true')
        ele.click()


        
        # ok
        def scroll_find_element(by, value):
            while 1:
                try:
                    element = driver.find_element(by=by, value=value)
                except Exception as e:
                    if e:
                        driver.swipe(current_width * 1 / 2, current_height, current_width * 1 / 2,
                                     current_height * 1 / 3, 1500)
                else:
                    return element

        try:
            ele = func_timeout(180, scroll_find_element,
                               args=(AppiumBy.IOS_PREDICATE, 'name == "   中国  +86" AND visible '
                                                             '== true'))
        except FunctionTimedOut:
            print("执行超时！")
        else:
            ele.click()

        # 应该是不执行
        # driver.find_element(by=AppiumBy.ID, value='icon 24 back').click()
        

        def scroll_find_element(by, value, timeout):
            @func_set_timeout(timeout)
            def specific_execution():
                while 1:
                    try:
                        element = driver.find_element(by=by, value=value)
                    except Exception as e:
                        if e:
                            driver.swipe(current_width * 1 / 2, current_height, current_width * 1 / 2,
                                         current_height * 1 / 3,1500)
                    else:
                        return element

        scroll_find_element(AppiumBy.IOS_PREDICATE, 'name == "   中国  +86" AND visible == true', 180)
        # element_1.click()
        # 直到元素出现

"""
