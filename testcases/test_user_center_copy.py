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

logger = logging.getLogger(__name__)

@pytest.mark.login
@pytest.mark.dependency()
@pytest.mark.parametrize("login_data", ['cn_test', 'us_test', 'us', 'eu'], indirect=True)
def test_login(request, appium_service, ios_driver, login_data):
    driver = ios_driver

    # 获取登录数据
    # login_data = LOGIN_DATA.get('cn_test').copy()

    with allure.step('step1: 启动app'):
        logger.info("第一步：启动app")
        driver.activate_app(AOSU_PACKAGE_NAME)
        logger.info("app启动成功！")
        # 第一次启动会弹出权限弹窗，点击‘允许’
        (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, ALLOW)) and el.click()

    with allure.step('step2: 点击 登录'):
        logger.info("第二步：点击 登录")
        el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=LOGIN)
        el.click()

    with allure.step('step3: 输入 邮箱'):
        el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value=EMAIL_TYPE_TEXT_FIELD_CLASS_CHAIN)
        el.clear()
        el.click()
        logger.info(f"第三步：输入邮箱：{login_data['email']}")
        el.send_keys(login_data['email'])

        # 隐藏键盘
        if driver.is_keyboard_shown():
            logger.info("收起键盘")
            # 有完成，点完成
            (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, DONE)) and el.click()
            # 有回车，点回车
            (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, RETURN)) and el.click()

    with allure.step('step4: 输入 密码'):
        el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value=PWD_TYPE_SECURE_TEXT_FIELD_CLASS_CHAIN)
        el.clear()
        el.click()
        logger.info(f"第四步：输入密码：{login_data['password']}")
        el.send_keys(login_data['password'])

        if driver.is_keyboard_shown():
            logger.info("收起键盘")
            # 有完成，点完成
            (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, DONE)) and el.click()
            # 有回车，点回车
            (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, RETURN)) and el.click()

    with allure.step('step5: 选择地区'):
        if is_element_present(driver, AppiumBy.IOS_CLASS_CHAIN, login_data['region_type_text_field_class_chain']):
            logger.info("第五步：默认是中国的话，不需要点击进入地区选择列表")
            sleep(1)
        else:
            # 点击 选择国家/地区
            el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value=REGION_TYPE_OTHER_CLASS_CHAIN)
            el.click()

            # 出现‘以后’就点击
            (el := element_until_appears(driver, AppiumBy.ACCESSIBILITY_ID, NOT_NOW, 3)) and el.click()
            logger.info("第五步：默认不是中国，需要在地区列表中滚动查找到中国")
            # 选择地区，例如，中国
            el = scroll_find_element(driver, AppiumBy.IOS_PREDICATE, login_data['country_predicate'])
            el.click()

    with (allure.step('step6: 点击 登录')):
        el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value=LOGIN_TYPE_STATIC_TEXT_2)
        el.click()
        logger.info("第六步：点击登录按钮")

        # 如果弹出权限弹窗，点击‘允许’
        # (el := is_element_present(driver, AppiumBy.ID, '允许')) and el.click() # 时间过短点不到
        (el := element_until_appears(driver, AppiumBy.ACCESSIBILITY_ID, ALLOW, 3)) and el.click()

        # 如果出现‘以后’，点击‘以后’
        (el := element_until_appears(driver, AppiumBy.ACCESSIBILITY_ID, NOT_NOW, 3)) and el.click()

        # 低电量弹窗，智能提醒弹窗，点击“知道了”
        while is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, GOT_IT):
            logger.info("首页有弹窗，点击：知道了")
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, GOT_IT).click()
            sleep(1)

        # 关闭云存广告弹窗
        (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, CLOSE_ADS)) and el.click()
        logger.info("进入首页后开始断言：导航按钮、+、设备、云存储、在线客服")
        # 断言首页元素
        assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DRAWER) is not None, \
            "首页左上角的导航按钮没有出现"
        assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_ADD) is not None, \
            "首页右上角的+号没有出现"
        assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DEVICES) is not None, \
            "首页底部 ‘设备’标签 没有出现"
        assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_CLOUD) is not None, \
            "首页底部 ‘云存储’标签 没有出现"
        assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_ONLINE_SUPPORT) is not None, \
            "首页底部 ‘在线客服’标签 没有出现"

    # request.node.add_dependency('test_logout', depends=['test_login'], scope='function')
    # request.node.session.items[1].runtest()
    test_logout(appium_service, ios_driver)


@pytest.mark.logout
@pytest.mark.dependency(depends=["test_login"])
def test_logout(appium_service, ios_driver):
    driver = ios_driver

    with allure.step('step1: 点击左上角 导航 按钮'):
        el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=HOME_PAGE_DRAWER)
        el.click()

    with allure.step('step2: 点击 退出登录'):
        el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=LOGOUT)
        el.click()

    with allure.step('step3: 点击 确定'):
        el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=YES)
        el.click()

        sleep(1)

        # 断言回到登录页面
        assert is_element_present(driver, AppiumBy.IOS_CLASS_CHAIN, LOGIN_TYPE_STATIC_TEXT_1) is not None, \
            "没有回到登录页面"
