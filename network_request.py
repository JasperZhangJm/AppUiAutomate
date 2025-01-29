import requests
import hashlib
import time
import logging
from test_data_fixture import REQUEST_DATA
from urllib.parse import unquote


HEADERS = {
    "Gz-AppId": "com.glazero.ios",
    "Gz-AppVer": "3.4.56.6338",
    "Gz-Brand": "apple",
    "Gz-BuildType": "debug",
    "Gz-Channel": "internal",
    "Gz-FontSize": "17",
    "Gz-Imei": "2DF236B7-6FAE-4A9F-A4B8-25E407C1D98A",
    "Gz-Lang": "zh",
    "Gz-Model": "iPhone X",
    "Gz-Network": "{vpn=false}",
    "Gz-NotifyPermission": "{enabled=true}",
    "Gz-OsLang": "zh-Hans-CN",
    "Gz-OsType": "iOS",
    "Gz-OsVer": "16.5.1",
    "Gz-Pid": "glazero",
    "Gz-Sid": "ca2f47b35cd99fd4a028120c384e64ae",
    "Gz-Sign": "6e01cd4cceebee47cf87967ebafde917",
    "Gz-Timezone": "+08:00",
    "Gz-Uid": "66179ca5018fa56985526281"
}

# 获取请求基本数据
request_data = REQUEST_DATA.get('cn_test').copy()

logger = logging.getLogger(__name__)


def hash_md5(passwd: str) -> str:
    try:
        return hashlib.md5(passwd.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f'Error encoding passwd: {e}')
        return ""


def gz_login(pm: request_data):
    timestamp_ms = int(time.time() * 1000)
    url = f'https://{pm['host']}/v1/user/login?uuid=ios_ui_auto&t={timestamp_ms}'

    pwd_md5 = hash_md5(pm['passwd'])

    data = {
        'countryAbbr': pm['region'],
        'countryCode': pm['country_code'],
        'email': pm['email'],
        'password': pwd_md5,
        'type': pm['gz_type']
    }

    try:
        rsp = requests.post(url, headers=HEADERS, data=data, timeout=(10, 10), verify=False)
        rsp.raise_for_status()

        gz_sid = rsp.json().get('data', {}).get('sid')
        gz_uid = rsp.json().get('data', {}).get('uid')

        decode_body = unquote(rsp.request.body.decode('utf-8') if isinstance(rsp.request.body, bytes) else rsp.request.body)

        logger.info("==== HTTP Request ====")
        logger.info(f"URL: {url}")
        logger.info(f"Method: POST")
        logger.info(f"Headers: {rsp.request.headers}")
        logger.info(f"Body: {decode_body}")

        logger.info("==== HTTP Response ====")
        logger.info(f"Status Code: {rsp.status_code}")
        logger.info(f"Body: {rsp.text}")

        return gz_sid, gz_uid

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        logger.error(f"Request failed: {e}")

        return None, None


def get_dev_name_over_request(dev_model):
    # 复制登录参数
    login_params = request_data
    # 获取sid和uid
    gz_sid, gz_uid = gz_login(login_params)

    timestamp_ms = int(time.time() * 1000)
    url = f'https://{login_params['host']}/v1/dev/getList?uuid=ios_ui_auto&t={timestamp_ms}'

    headers = HEADERS.copy()
    headers['Gz-Sid'] = gz_sid
    headers['Gz-Uid'] = gz_uid

    try:
        rsp = requests.post(url, headers=headers, timeout=(10, 10), verify=False)
        rsp.raise_for_status()

        logger.info("==== HTTP Request ====")
        logger.info(f"URL: {url}")
        logger.info(f"Method: POST")
        logger.info(f"Headers: {rsp.request.headers}")
        logger.info(f"Body: {rsp.request.body}")

        logger.info("==== HTTP Response ====")
        logger.info(f"Status Code: {rsp.status_code}")
        logger.info(f"Body: {rsp.text}")

        devices = rsp.json().get('data', {}).get('list', [])

        for device in devices:
            if device.get('model') == dev_model and device.get('role') == 0 and device.get('online') == 1:
                dev_name = device.get('name')
                logger.info(f"获取设备名称成功：{dev_name}")

                return dev_name

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        print(f"请求失败: {e}")

    return None
