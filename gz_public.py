"""
public method.

Author: Zhang Jia Min
Version: 1.0
Date: 2024-08-08
"""

import os
import re
import time
import yaml
import logging
from appium import webdriver
from datetime import datetime
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from element_constants import *


APPIUM_HOST = '127.0.0.1'
APPIUM_PORT = 4723

logger = logging.getLogger(__name__)


def get_device_opts():
    path = os.path.dirname(os.path.realpath(__file__))
    devices_conf_path = os.path.join(path, 'devices_conf.yaml')

    with open(devices_conf_path, 'r') as file:
        content = yaml.safe_load(file)

    return content


def create_ios_driver(custom_opts=None):
    # 创建对象
    options = XCUITestOptions()

    if custom_opts is not None:
        options.load_capabilities(custom_opts)

    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)


def create_android_driver(custom_opts=None):
    # 创建对象
    options = UiAutomator2Options()

    if custom_opts is not None:
        options.load_capabilities(custom_opts)

    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)


def is_element_present(driver, by, value):
    try:
        element = driver.find_element(by=by, value=value)
        return element
    except NoSuchElementException:
        return None


def scroll_find_element(driver, by, value, timeout=180):
    # 获取屏幕宽和高
    current_phone_size = driver.get_window_size()
    current_width = current_phone_size['width']
    current_height = current_phone_size['height']

    # 设置起始时间
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            element = driver.find_element(by=by, value=value)
            return element
        except NoSuchElementException:
            driver.swipe(
                current_width * 1 / 2, current_height,
                current_width * 1 / 2, current_height * 1 / 3,
                1500
            )
    # 超时仍未找到，返回None
    return None


def swipe_once_in_menu(driver):
    # 获取屏幕宽和高
    current_phone_size = driver.get_window_size()
    current_width = current_phone_size['width']
    current_height = current_phone_size['height']

    driver.swipe(
        current_width * 1 / 3, current_height * 2 / 3,
        current_width * 1 / 3, current_height * 1 / 3,
        1500
    )

    time.sleep(1)


def element_until_appears(driver, by, value, timeout=180):
    try:
        element = WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        return None


def take_screenshot(driver):
    ts = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    screenshot_name = f'screenshot_{ts}.png'
    screenshot_dir = 'screenshots'
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, screenshot_name)
    logger.info(f"截图地址是：{screenshot_path}")
    driver.save_screenshot(screenshot_path)
    return screenshot_path


def time_difference(log_last_line, click_time):
    """
    计算日志中开流节点与点击时间的时间差，返回格式为 时:分:秒.毫秒
    """

    # 取出日志中前两段，日期和时间，例如，2024-11-04 10:29:46.518
    match_words = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})', log_last_line)

    if match_words:
        date_time_str = match_words.group(1)
        print("提取到的日期和时间字符串: ", date_time_str)

        # 将提取的日期和时间字符串解析成datetime格式：
        success_specified_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        print("开流节点的时间为:", success_specified_time)

        # 判断 开流的节点时间跟点击时间的大小关系即先后次序，因为iOS的日志来源是app日志文件，历史的节点状态会保留在日志文件中，
        # 如果当次开流失败时，会取到上次的节点成功日志，为了发现这种情况，通过时间次序来判断，
        # 在一次成功地开流过程中，开流节点的时间应该大于点击时间，如果出现了开流节点时间小于或者等于点击时间的情况，说明本次开流失败了。
        if success_specified_time > click_time:
            # 计算时间差
            success_time_difference = success_specified_time - click_time
            print("时间差：", success_time_difference)

            # 将时间差格式化为时分秒毫秒形式
            days, seconds = success_time_difference.days, success_time_difference.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            milliseconds = f"{success_time_difference.microseconds:06d}"

            formatted_time = "{:02}:{:02}:{:02}.{}".format(hours, minutes, seconds, milliseconds)

            print("格式化后的时间差（时:分:秒.毫秒）:", formatted_time)

            return success_time_difference
        else:
            print("开流节点时间早于点击时间，本次开流失败!")
            return None

    else:
        print("未匹配到日期和时间！")
        return None


def get_flag():
    flag_file = 'flag_value.txt'
    # 读取文件中记录的状态值，文件中默认是"False"
    if os.path.exists(flag_file):
        with open(flag_file, 'r') as file:
            return file.read().strip() == "True"
    return False


def set_flag(flag_value):
    flag_file = 'flag_value.txt'
    if os.path.exists(flag_file):
        with open(flag_file, 'w') as file:
            file.write("True" if flag_value else "False")
    else:
        print(f"flag文件不存在：{flag_file}")


def gesture_right_drag(driver):
    screen_weight = driver.get_window_size()['width']
    screen_height = driver.get_window_size()['height']
    from_x = 0
    from_y = screen_height * 0.5
    to_x = screen_weight
    to_y = screen_height * 0.5
    duration = 0.2

    driver.execute_script("mobile: dragFromToForDuration", {
                                            "fromX": from_x,
                                            "fromY": from_y,
                                            "toX": to_x,
                                            "toY": to_y,
                                            "duration": duration
                                            })


def pull_down_refresh(driver, x, y):
    s_x = int(x * 0.50)
    s_y = int(y * 0.25)
    e_x = int(x * 0.5)
    e_y = int(y * 0.75)
    driver.swipe(s_x, s_y, e_x, e_y, 500)


# 地区选择页面的搜索框
def region_search(driver, region_name):
    country_name = region_name[3:5]

    # 点击搜索
    el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value=REGION_SEARCH)
    el.click()
    driver.implicitly_wait(5)

    # 输入地区，例如，中国
    el.send_keys(country_name)

    # 隐藏键盘
    if driver.is_keyboard_shown():
        logger.info("收起键盘")
        # 有完成，点完成
        (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, DONE)) and el.click()
        # 有回车，点回车
        # (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, RETURN)) and el.click()

    el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=region_name)
    el.click()

    driver.implicitly_wait(5)


def region_search_for_android(driver, region_name):
    country_name = region_name[3:5]
    logger.info(f"gz_public::region_search_for_android国家名字是：{country_name}")

    # 搜索框
    el = driver.find_element(by=AppiumBy.ID, value=ANDROID_REGION_SEARCH_REID)

    # 输入地区，例如，中国
    el.send_keys(country_name)

    country_code = region_name.lstrip()
    logger.info(f"gz_public::region_search_for_android country_code是：{country_code}")

    el = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                             value=f'new UiSelector().resourceId("com.glazero.android:id/tv_country_name").text("{country_code}")')
    el.click()

    driver.implicitly_wait(5)
