# This is a sample Python script.
from time import sleep

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'


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

        el = driver.find_element(by=AppiumBy.ID, value='登录')
        el.click()

        el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN,
                                 value='**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField')
        el.clear()
        el.click()

        sleep(2)

        el.send_keys('1499405887@qq.com')

        sleep(1)

        if driver.is_keyboard_shown():
            el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Done')
            el.click()

        sleep(1)
        el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN,
                                 value='**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField')
        el.clear()
        el.click()

        sleep(2)

        el.send_keys('Qwe222222')

        sleep(1)

        if driver.is_keyboard_shown():
            el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Done')
            el.click()

        sleep(1)

        # el = driver.find_element(by=AppiumBy.ID, value='登录')
        # el.click()

        # el = driver.find_element(by=AppiumBy.ID, value='登录')
        # el.click()

        el = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value='**/XCUIElementTypeStaticText[`name == "登录"`][2]')
        el.click()

        sleep(5)

        source = driver.page_source
        # print('Page Source: ', source)
        if '以后' in source:
            el = driver.find_element(by=AppiumBy.ID, value='以后')
            el.click()
            sleep(5)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
