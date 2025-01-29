import time
import allure
import pytest

from gz_public import set_flag
from gz_public import get_device_opts
from gz_public import create_ios_driver, create_android_driver
from gz_public import take_screenshot
from gz_public import is_element_present
from test_user_center import test_login
from Android.test_login_and_logout import test_logout
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from element_constants import *
from test_data_fixture import *


APPIUM_HOST = '127.0.0.1'
APPIUM_PORT = 4723

count = {'count': 0}

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def appium_service():
    service = AppiumService()
    service.start(
        args=['--address', APPIUM_HOST, '--port', str(APPIUM_PORT)],
        timeout_ms=20000
    )
    yield service
    service.stop()


@pytest.fixture(scope='session')
def ios_driver():
    options = get_device_opts()
    ios_opts = options['iPhoneX']
    driver = create_ios_driver(ios_opts)
    yield driver
    driver.quit()
    # session结束后将设备的休眠状态设置为False
    set_flag(False)


@pytest.fixture(scope='session')
def android_driver():
    options = get_device_opts()
    android_opts = options['S10e']
    driver = create_android_driver(android_opts)
    yield driver
    driver.quit()


# 测试开始之前重启app
@pytest.fixture(scope='function')
def restart_app(appium_service, ios_driver):
    driver = ios_driver

    driver.terminate_app(AOSU_PACKAGE_NAME)
    driver.implicitly_wait(5)
    driver.activate_app(AOSU_PACKAGE_NAME)
    driver.implicitly_wait(5)

    # 启动后如果没有登录就登录账号，通过登录后首页左上角的menu图标判断
    if not is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DRAWER):
        test_login(appium_service, ios_driver)
        driver.implicitly_wait(5)

    yield


@pytest.fixture(scope='function')
def ios_debug_mode(appium_service, ios_driver):
    driver = ios_driver

    # 点击菜单栏
    el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=HOME_PAGE_DRAWER)
    el.click()

    # 点击头像7次
    el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=PERSONAL_ICON_NAME)
    el.click()


# 每次回到首页后要清除首页的弹窗
@pytest.fixture(scope='function')
def clear_popup(appium_service, ios_driver):
    driver = ios_driver

    # 低电量弹窗，智能提醒弹窗，点击“知道了”
    while is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, GOT_IT):
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, GOT_IT).click()
        time.sleep(1)

    # 关闭云存广告弹窗
    (el := is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, CLOSE_ADS)) and el.click()

    # 其他弹窗检测
    '''
    首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
    '''

    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call':
        if rep.failed:
            logger.error(f"Test {item.nodeid}: FAILED\n")

            driver = item.funcargs.get("android_driver") or item.funcargs.get("ios_driver")

            if driver:
                platform_name = driver.capabilities.get('platformName')
                if platform_name == "Android":
                    logger.info("进入了Android的判断case")
                    driver = item.funcargs['android_driver']
                elif platform_name == 'iOS':
                    logger.info("进入了iOS的判断case")
                    driver = item.funcargs['ios_driver']

            logger.info(f"driver是：{driver}")
            logger.info(f"item.keywords 是：{item.keywords}")

            screenshot_path = take_screenshot(driver)

            with open(screenshot_path, 'rb') as image_file:
                allure.attach(image_file.read(), name='测试未通过截图', attachment_type=allure.attachment_type.PNG)

            if call.excinfo:
                error_message = str(call.excinfo.value)
                logger.error(f"Test {item.nodeid} failed with error: {error_message}\n")
                print('这是error_message：', error_message)

            # 用例执行失败后重启app
            if "ios" in item.keywords:
                driver.terminate_app(AOSU_PACKAGE_NAME)
                driver.implicitly_wait(5)
                driver.activate_app(AOSU_PACKAGE_NAME)
                driver.implicitly_wait(5)
            elif "android" in item.keywords:
                driver.terminate_app(ANDROID_PACKAGE_NAME)
                driver.implicitly_wait(5)
                driver.activate_app(ANDROID_PACKAGE_NAME)
                driver.implicitly_wait(5)

        elif rep.skipped:
            outcome_status = 'SKIPPED'
            logger.info(f"Test {item.nodeid}: {outcome_status}\n")
        else:
            outcome_status = 'PASSED'
            logger.info(f"Test {item.nodeid}: {outcome_status}\n")


@pytest.fixture()
def get_iphone_time(appium_service, ios_driver):
    driver = ios_driver
    iphone_time = driver.execute_script("mobile: getDeviceTime")
    return iphone_time


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    count['count'] += 1
    logger.info(f"当前是第 {count['count']} 次执行")
    print(f"\n当前是第 {count['count']} 次执行\n")


@pytest.fixture(scope="module")
def screen_size(ios_driver):
    driver = ios_driver
    size = driver.get_window_size()
    logger.info("获取屏幕尺寸完成 in screen_size fixture，只在module级调用1次。")
    return size['width'], size['height']


@pytest.fixture(scope='function')
def init_logout_android(appium_service, android_driver):
    driver = android_driver

    # 启动后如果没有退出就先退出账号，通过登录后首页左上角的menu图标判断
    if is_element_present(driver, AppiumBy.ID, ANDROID_MENU_REID):
        test_logout(appium_service, android_driver)
        driver.implicitly_wait(5)

    yield


@pytest.fixture(scope='function')
def init_logout_ios(appium_service, ios_driver):
    driver = ios_driver

    # 启动后如果没有退出就先退出账号，通过登录后首页左上角的menu图标判断
    if is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DRAWER):
        test_logout(appium_service, ios_driver)
        driver.implicitly_wait(5)

    yield
