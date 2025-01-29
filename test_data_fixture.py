import pytest
import logging
from interact_with_phone import clear_sandbox_log

logger = logging.getLogger(__name__)


# 登录数据
# 跟@pytest.mark.parametrize("login_data", ['cn_test'], indirect=True)配合使用
@pytest.fixture
def login_data(request):
    env = request.param
    if env == 'cn_test':
        return {
            'email': '1499405887@qq.com',
            'password': 'Qwe222222',
            'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "中国 +86"`]',
            'country_predicate': 'name == "   中国  +86" AND visible == true',
            'region_name': '   中国  +86',
            'assert_region_name': '中国区'
        }
    elif env == 'us_test':
        return {
            'email': '1499405887@qq.com',
            'password': 'Qwe111111',
            'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "美国 +1"`]',
            'country_predicate': 'name == "   美国  +1" AND visible == true',
            'region_name': '   美国  +1',
            'assert_region_name': 'change pid'
        }
    elif env == 'us':
        return {
            'email': '1499405887@qq.com',
            'password': 'Qwe111111',
            'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "美国 +1"`]',
            'country_predicate': 'name == "   美国  +1" AND visible == true',
            'region_name': '   美国  +1',
            'assert_region_name': 'change pid'
        }
    elif env == 'eu':
        return {
            'email': 'aosu20230306@163.com',
            'password': 'Qwe111111',
            'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "德国 +49"`]',
            'country_predicate': 'name == "   德国  +49" AND visible == true',
            'region_name': '   德国  +49',
            'assert_region_name': '欧洲'
        }
    else:
        raise ValueError("Unknown environment: {}".format(env))


# 登录数据，字典形式
LOGIN_DATA = {
    'cn_test': {
        'email': '1499405887@qq.com',
        'password': 'Qwe222222',
        'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "中国 +86"`]',
        'country_predicate': 'name == "   中国  +86" AND visible == true'
    },
    'us_test': {
        'email': '1499405887@qq.com',
        'password': 'Qwe111111',
        'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "美国 +1"`]',
        'country_predicate': 'name == "   美国  +1" AND visible == true'
    },
    'us': {
        'email': '1499405887@qq.com',
        'password': 'Qwe111111',
        'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "美国 +1"`]',
        'country_predicate': 'name == "   美国  +1" AND visible == true'
    },
    'eu': {
        'email': 'aosu20230306@163.com',
        'password': 'Qwe111111',
        'region_type_text_field_class_chain': '**/XCUIElementTypeTextField[`value == "德国 +49"`]',
        'country_predicate': 'name == "   德国  +49" AND visible == true'
    }
}


# 设备数据
@pytest.fixture(scope="module")
def device_data(request):
    from network_request import get_dev_name_over_request

    dev_model = request.param
    dev_name = get_dev_name_over_request(dev_model)
    logger.info(f"获取到设备的名称完成 in device_data fixture，只在module级调用1次。")
    logger.info(f"设备名称是：{dev_name}")

    if dev_model == 'C8S':
        result = clear_sandbox_log('iPhoneX')
        logger.info(f"沙盒日志清除完成！返回结果是：{result}")
        return {
            'iphone_model': 'iPhoneX',
            'sn': 'C8S2DA110000043',
            'dev_model': 'C8S',
            'dev_name': dev_name,
            'sleep_time': 25
        }
    elif dev_model == 'C6L':
        result = clear_sandbox_log('iPhoneX')
        logger.info(f"沙盒日志清除完成！返回结果是：{result}")
        return {
            'iphone_model': 'iPhoneX',
            'sn': 'C6L2BA110004740',
            'dev_model': 'C6L',
            'dev_name': dev_name,
            'sleep_time': 35
        }
    else:
        raise ValueError("Unknown device model: {}".format(dev_model))


# 服务端请求数据
REQUEST_DATA = {
    "cn_test": {
        'host': 'api-test-cn.aosulife.com',
        'email': '1499405887@qq.com',
        'region': 'CN',
        'country_code': '86',
        'passwd': 'Qwe222222',
        'gz_type': 1
    },
    "us_test": {
        'host': 'api-test-us.aosulife.com',
        'email': '1499405887@qq.com',
        'region': 'US',
        'country_code': '1',
        'passwd': 'Qwe111111',
        'gz_type': 1
    },
    "us": {
        'host': 'api-test-us.aosulife.com',
        'email': '1499405887@qq.com',
        'region': 'US',
        'country_code': '1',
        'passwd': 'Qwe111111',
        'gz_type': 1
    },
    "eu": {
        'host': 'api-eu.aosulife.com',
        'email': 'aosu20230306@163.com',
        'region': 'DE',
        'country_code': '49',
        'passwd': 'Qwe111111',
        'gz_type': 1
    }
}


"""
@pytest.fixture
def request_data(request):
    env = request.param
    return REQUEST_DATA.get(env)
"""
