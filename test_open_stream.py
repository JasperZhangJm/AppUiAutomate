import time
import allure
import logging
import pytest
from datetime import datetime
from element_constants import *
from network_request import get_dev_name_over_request
from gz_public import scroll_find_element
from gz_public import is_element_present
from gz_public import set_flag, get_flag
from gz_public import pull_down_refresh
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from interact_with_phone import (get_dev_start_wake_state_result, get_dev_wake_state_result, get_dev_p2p_state_result,
                                 get_dev_play_state_result, get_dev_dormancy_state_result, log_process_after_case_fail)

logger = logging.getLogger(__name__)


@allure.feature("开流专项")
class TestOpenStream(object):
    """
    开流专项，例如，多次开流，每次记录节点时间
    """

    @allure.title('C6L 多次开流')
    @allure.story('用户循环测试C6L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c6l_open_stream(self, appium_service, ios_driver, restart_app, clear_popup, global_data, screen_size):
        """
        :前提条件：① 账号下要绑定C9S设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :步骤：
        :1. 确认设备已休眠
        :2. 冷启动App
        :3. 开流，等结果（成功 or 失败）
        :重复以上 1 2 3，记录下每次的结果
        """
        logger.info("开始创建iOS驱动，调用fixture ios_driver")
        driver = ios_driver
        x, y = screen_size
        logger.info(f"获取屏幕的尺寸，调用fixture screen_size，屏幕尺寸是：{x}, {y}")

        # 获取c9s设备的名字
        dev_name = get_dev_name_over_request(global_data['dev_model'])
        logger.info(f"调用接口获取设备的名称：{dev_name}")
        print("找到的设备名称是：", dev_name)

        with allure.step(
                'step1: 等待25秒，设备休眠。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 状态文件默认是"False"，第一次休眠25秒
            sleep_flag = get_flag()
            if sleep_flag is False:
                logger.info(f"第1步：获取当前设备的休眠状态：{sleep_flag}，休眠25秒")
                time.sleep(25)
            else:
                logger.info(f"第1步：当前的休眠状态是：{sleep_flag}，在首页停留1秒")
                # 进入首页后等1秒
                time.sleep(1)
            # 下拉刷新首页设备列表
            logger.info(f"第1步：进入首页后下拉刷新")
            pull_down_refresh(driver, x, y)

        with (allure.step('step2: 在设备列表中滑动找到要开流的设备，例如，c6l。step时间点：%s'
                          % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 确认找到了设备
            logger.info("第2步：开始找设备")
            el = scroll_find_element(driver, AppiumBy.ACCESSIBILITY_ID, dev_name)
            assert el is not None, f"首页设备列表中没有找到设备：{dev_name}"
            driver.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step3: 点击前面拿到的设备名称，例如，c6l。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 获取当前时间
            click_time = datetime.now()
            logger.info(f"第3步：点击设备的时间点是：{click_time}")
            print(f"点击设备卡片的时间点是：{click_time}")

            # 点击设备名称
            el.click()
            driver.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, dev_name)

        with (allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                          % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 目前没有适配新手引导，因为改版需求中会出新的
            """
            # 进入开流页后检查，是否新手引导-知道了
            while is_element_present(driver, AppiumBy.ID, GOT_IT) or is_element_present(driver, AppiumBy.ID, NEXT):
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 变声对讲引导 ,点击屏幕中的 知道了
                driver.find_element(AppiumBy.ID, GOT_IT).click()
                driver.implicitly_wait(10)

                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航 ,点击屏幕中的 下一波
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '下一步').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航第二个引导页面  ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航第三个引导页面  ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)
            """

            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            logger.info("第4步：进入开流页面后等待加载状态消失")
            WebDriverWait(driver, 45).until_not(expected_conditions.presence_of_element_located(
                (AppiumBy.IOS_CLASS_CHAIN, OPEN_FLOW_STATUS)))
            time.sleep(1)

            logger.info("第4步：进入开流页面先截一张图")
            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            driver.save_screenshot(f"./report/{global_data['dev_model']}/start_flow_{start_flow}.png")
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file(f"./report/{global_data['dev_model']}/start_flow_{start_flow}.png", name="start flow",
                               attachment_type=allure.attachment_type.JPG)
            driver.implicitly_wait(10)
            '''
            # 当开流不成功,屏幕出现刷新重试时,点击刷新重试按钮.
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/bt_play_retry") is True:
                master.implicitly_wait(10)
                # 点击屏幕刷新重试按钮.
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '刷新重试').click()
                time.sleep(40)

                # 截一张图
                start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6L/start_flow_%s.png' % start_flow)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/C6L/start_flow_%s.png" % start_flow, name="start flow",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)
            '''
            with allure.step('step4-1: 查看从首页，进入开流页面的结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # iOS没有这个状态
                pass
                # 判断开流过程中,进入开流页面的状态，日志中出现字符串 LivePlayFragment:onCreate 表示设备唤醒成功。
                # create_LivePlay_fragment_state = initPhone.get_start_create_LivePlay_fragment_result(
                #     initPhone.get_dev_id(), click_time)
                # print("开流播放片段 创建成功：%s" % create_LivePlay_fragment_state)

                # 进入开流页面失败时处理
                # if create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate':
                #     assert create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate', "LivePlaySingleFragment:onCreate 表示设备创建开流页面成功。"
                # else:
                    # 在手机中查找对应的日志文件
                    # current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    # current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志,并且保存到本地
                    # gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                    # 将日志添加到报告中
                    # allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                    #                    attachment_type=allure.attachment_type.TEXT)
                    # master.implicitly_wait(10)

                    # 获取ty日志
                    # gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                    # 将日志添加到报告中
                    # allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                    #                    attachment_type=allure.attachment_type.TEXT)
                    # master.implicitly_wait(10)

                    # with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     # % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        # master.terminate_app(android_package_name)
                        # master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    # assert create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate', "LivePlaySingleFragment:onCreate 表示设备唤醒成功。"

            with allure.step('step4-2: 进入开流页面，查看设备接收到唤醒指令结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 wakeStart.
                start_wake_state = get_dev_start_wake_state_result(click_time,
                                                                   global_data['iphone_model'], global_data['sn'])
                logger.info(f"第4-2步：获取wakeStart状态是：{start_wake_state}")
                print("设备收到开始唤醒指令的状态是：%s" % start_wake_state)

                if start_wake_state == 'wakeStart':
                    logger.info("第4-2步：获取到的wakeStart状态是：wakeStart，success")
                    assert start_wake_state == 'wakeStart', "得到的状态不是wakeStart，有可能设备没有开始唤醒。"
                else:
                    # 设备唤醒失败时处理
                    logger.info("第4-2步：获取到的wakeStart状态不是wakeStart success，开始错误处理，获取app 日志")
                    log_process_after_case_fail(driver, global_data['iphone_model'], global_data['dev_model'])

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        logger.info("第4-2步：错误日志处理完成，杀死app")
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                    logger.info("第4-2步：断言失败，结束本次执行")
                    assert start_wake_state == 'wakeStart', "得到的状态不是wakeStart，有可能设备没有开始唤醒。"

            with allure.step('step4-3: 进入开流页面，查看设备唤醒结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中，设备唤醒状态，日志中出现字符串 awake success 表示设备唤醒成功。
                dev_wake_state = get_dev_wake_state_result(click_time, global_data['iphone_model'], global_data['sn'])
                logger.info(f"第4-3步：获取到的唤醒状态是：{dev_wake_state}")
                print("当前设备唤醒状态是：%s" % dev_wake_state)

                if dev_wake_state == 'awake success':
                    assert dev_wake_state == 'awake success', "得到的状态不是awake success，有可能设备没有唤醒成功。"
                else:
                    # 设备唤醒失败时处理
                    log_process_after_case_fail(driver, global_data['iphone_model'], global_data['dev_model'])

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤,去执行下一遍
                    assert dev_wake_state == 'awake success', "得到的状态不是awake success，有可能设备没有唤醒成功。"

            with allure.step('step4-4: 进入开流页面，查看P2P连接结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备唤醒状态，日志中出现字符串 connectP2P {sn}connect Suc 表示p2p连接成功。
                dev_p2p_state = get_dev_p2p_state_result(click_time, global_data['iphone_model'], global_data['sn'])
                logger.info(f"第4-4步：获取到的p2p状态是：{dev_p2p_state}")
                print("当前设备P2P状态是：%s" % dev_p2p_state)

                if dev_p2p_state == f'connectP2P {global_data['sn']}connect Succ':
                    assert dev_p2p_state == f'connectP2P {global_data['sn']}connect Succ', \
                        "得到的状态不是connectP2P success，设备p2p没有连接成功。"
                else:
                    # p2p连接失败时处理
                    log_process_after_case_fail(driver, global_data['iphone_model'], global_data['dev_model'])

                    with allure.step('step4-2-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                    assert dev_p2p_state == f'connectP2P {global_data['sn']}connect Succ', \
                        "得到的状态不是connectP2P success，设备p2p没有连接成功。"

            with allure.step('step4-5: 进入开流页面，查看开流结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流结果，加载过程消失后开流成功或者失败
                play_state = get_dev_play_state_result(click_time, global_data['iphone_model'], global_data['sn'])
                logger.info(f"第4-5步：获取到的播放状态是：{play_state}")
                print("当前开流状态是：%s" % play_state)

                if play_state == 'previewSuccess':
                    assert play_state == 'previewSuccess', "得到的状态不是previewSuccess，开流失败。"
                else:
                    # 开流失败时处理
                    log_process_after_case_fail(driver, global_data['iphone_model'], global_data['dev_model'])

                    with allure.step('step4-5-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                    assert play_state == 'previewSuccess', "得到的状态不是previewSuccess，开流失败。"

        with (((allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                            % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))))):
            # 开流页面左上角的 返回 按钮
            el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=PLAY_BACK_ICON)

            # 获取当前时间
            click_time = datetime.now()
            logger.info(f"第5步：点击返回按钮的时间是：{click_time}")
            print(f"点击开流页面左上角返回按钮的时间点是：{click_time}")

            el.click()

            # 根据不同的设备设定的时间不一样，例如C6L，20秒之内就休眠了
            time.sleep(global_data['sleep_time'])

            # 判断设备是否休眠，日志中出现字符串 "deviceId":"{sn}","dp":"149","value":"0" 表示设备休眠成功。
            dev_dormancy_state = get_dev_dormancy_state_result(click_time, global_data['iphone_model'],
                                                               global_data['sn'])
            logger.info(f"第5步：获取到的休眠状态是：{dev_dormancy_state}")
            print("当前设备休眠状态是：%s" % dev_dormancy_state)

            if dev_dormancy_state == f'{{"deviceId":"{global_data['sn']}","dp":"149","value":"0"}}':
                # 设置状态文件为休眠状态，下次执行step1的时候不用再等25秒
                logger.info("第5步：设备休眠成功，将休眠标志设置为True")
                set_flag(True)

                assert dev_dormancy_state == f'{{"deviceId":"{global_data['sn']}","dp":"149","value":"0"}}', \
                    "得到的状态不是'dpStr={\"149\":false}' 设备休眠失败。"
            else:
                # 设备唤醒失败时处理
                # 获取失败或者休眠失败，将状态置为False，这样在第一步中仍需要等待25秒
                logger.info("第5步：休眠失败，将休眠标志设置为False，并开始错误处理获取app日志")
                set_flag(False)
                log_process_after_case_fail(driver, global_data['iphone_model'], global_data['dev_model'])

                with allure.step('step5-1-1: 冷启app。step时间点：%s'
                                 % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                    driver.terminate_app(AOSU_PACKAGE_NAME)
                    driver.implicitly_wait(10)

                # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                assert dev_dormancy_state == f'{{"deviceId":"{global_data['sn']}","dp":"149","value":"0"}}', \
                    "得到的状态不是'dpStr={\"149\":false}' 设备休眠失败。"

                # 确认回到了首页
            assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DEVICES) is not None, \
                "首页底部 ‘设备’标签 没有出现，没有回到首页。"
            logger.info("第5步，回到了首页，断言成功")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            logger.info("第6步：杀死app")
            driver.terminate_app(AOSU_PACKAGE_NAME)
            driver.implicitly_wait(10)

    @allure.title('C8S 多次开流')
    @allure.story('用户循环测试C8S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    @pytest.mark.parametrize("device_data", ['C8S'], indirect=True)
    def test_c8s_open_stream(self, appium_service, ios_driver, restart_app, clear_popup, device_data, screen_size):
        """
        :前提条件：① 账号下要绑定C8S设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :步骤：
        :1. 确认设备已休眠
        :2. 冷启动App
        :3. 开流，等结果（成功 or 失败）
        :重复以上 1 2 3，记录下每次的结果
        """
        logger.info("开始创建iOS驱动，调用fixture ios_driver")

        driver = ios_driver
        x, y = screen_size

        logger.info(f"获取屏幕的尺寸，调用fixture screen_size，屏幕尺寸是：{x}, {y}")

        # 获取设备的名字
        dev_name = device_data['dev_name']
        logger.info(f"调用接口获取设备的名称：{dev_name}")

        with allure.step(
                'step1: 等待25秒，设备休眠。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            time.sleep(25)
            # 下拉刷新首页设备列表
            # logger.info(f"第1步：进入首页后下拉刷新")
            # pull_down_refresh(driver, x, y)

            # 状态文件默认是"False"，第一次休眠25秒
            # sleep_flag = get_flag()

            # if sleep_flag is False:
            #     logger.info(f"第1步：获取当前设备的休眠状态：{sleep_flag}，休眠25秒")
            #     time.sleep(25)
            # else:
            #     logger.info(f"第1步：当前的休眠状态是：{sleep_flag}，在首页停留1秒")
            #     # 进入首页后等1秒
            #     time.sleep(1)

        with (allure.step('step2: 在设备列表中滑动找到要开流的设备并点击，例如，%s。step时间点：%s'
                          % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))):
            # 确认找到了设备
            logger.info("第2步：开始找设备")
            el = scroll_find_element(driver, AppiumBy.ACCESSIBILITY_ID, dev_name)

            # 获取当前时间
            click_time = datetime.now()

            el.click()

            # assert el is not None, f"首页设备列表中没有找到设备：{dev_name}"
            driver.implicitly_wait(10)

        with allure.step('step3: 进入开流页面，页面顶部为开流设备的设备名称，例如，%s。step时间点：%s'
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 第2步中的el.click()有时点不到，如果没有进入开流页面在首页再点一次
            if is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, dev_name+' ') is None:
                logger.info("第二次进行点击，第一次没有点到，此时还在首页")
                el = driver.find_element(AppiumBy.ACCESSIBILITY_ID, dev_name)
                # 获取当前时间
                click_time = datetime.now()
                el.click()

            logger.info(f"第3步：点击设备的时间点是：{click_time}")

            driver.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称太阳能摄像机
            assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, dev_name+' ')

        with (allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                          % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 目前没有适配新手引导，因为改版需求中会出新的
            """
            # 进入开流页后检查，是否新手引导-知道了
            while is_element_present(driver, AppiumBy.ID, GOT_IT) or is_element_present(driver, AppiumBy.ID, NEXT):
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 变声对讲引导 ,点击屏幕中的 知道了
                driver.find_element(AppiumBy.ID, GOT_IT).click()
                driver.implicitly_wait(10)

                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航 ,点击屏幕中的 下一波
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '下一步').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航第二个引导页面  ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航第三个引导页面  ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)
            """

            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # Android resource-id相同：com.glazero.android:id/tv_live_play_loading
            # iOS 的class chain和name每个状态都不一样，所以分开处理
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            logger.info("第4步：进入开流页面后等待加载状态消失")
            WebDriverWait(driver, 35).until_not(expected_conditions.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, STREAM_LOADING_STATUS_NAME_1)))
            logger.info("状态1'实时视频加载中…'处理完成")
            WebDriverWait(driver, 35).until_not(expected_conditions.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, STREAM_LOADING_STATUS_NAME_2)))
            logger.info("状态2'正在建立访问通道…'处理完成")
            WebDriverWait(driver, 35).until_not(expected_conditions.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, STREAM_LOADING_STATUS_NAME_3)))
            logger.info("状态3'正在连接网络服务…'处理完成")
            WebDriverWait(driver, 35).until_not(expected_conditions.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, STREAM_LOADING_STATUS_NAME_4)))
            logger.info("状态4'实时视频加载中…'处理完成")
            WebDriverWait(driver, 35).until_not(expected_conditions.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, STREAM_LOADING_STATUS_NAME_5)))
            logger.info("状态5'加载较慢，尝试切换至流畅模式'处理完成")

            logger.info("第4步：进入开流页面先截一张图")
            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            driver.save_screenshot(f"./report/{device_data['dev_model']}/start_flow_{start_flow}.png")
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file(f"./report/{device_data['dev_model']}/start_flow_{start_flow}.png", name="start flow",
                               attachment_type=allure.attachment_type.JPG)
            driver.implicitly_wait(10)

            with allure.step('step4-1: 查看从首页，进入开流页面的结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # iOS没有这个状态
                pass

            with allure.step('step4-2: 进入开流页面，查看设备接收到唤醒指令结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 wakeStart.
                start_wake_state = get_dev_start_wake_state_result(click_time,
                                                                   device_data['iphone_model'], device_data['sn'])
                logger.info(f"第4-2步：获取wakeStart状态是：{start_wake_state}")

                if start_wake_state == 'wakeStart':
                    logger.info("第4-2步：获取到的wakeStart状态是：wakeStart，success")
                    assert start_wake_state == 'wakeStart', "得到的状态不是wakeStart，有可能设备没有开始唤醒。"
                else:
                    # 开流失败后等待30秒，等待iOS日志获取完成
                    time.sleep(30)

                    # 设备唤醒失败时处理
                    logger.info("第4-2步：获取到的wakeStart状态不是wakeStart success，开始错误处理，获取app 日志")
                    log_process_after_case_fail(driver, device_data['iphone_model'], device_data['dev_model'])

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        logger.info("第4-2步：错误日志处理完成，杀死app")
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                    logger.info("第4-2步：断言失败，结束本次执行")
                    assert start_wake_state == 'wakeStart', "得到的状态不是wakeStart，有可能设备没有开始唤醒。"

            with allure.step('step4-3: 进入开流页面，查看设备唤醒结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中，设备唤醒状态，日志中出现字符串 awake success 表示设备唤醒成功。
                dev_wake_state = get_dev_wake_state_result(click_time, device_data['iphone_model'], device_data['sn'])
                logger.info(f"第4-3步：获取到的唤醒状态是：{dev_wake_state}")

                if dev_wake_state == 'awake success':
                    assert dev_wake_state == 'awake success', "得到的状态不是awake success，有可能设备没有唤醒成功。"
                else:
                    # 开流失败后等待30秒，等待iOS日志获取完成
                    time.sleep(30)

                    # 设备唤醒失败时处理
                    log_process_after_case_fail(driver, device_data['iphone_model'], device_data['dev_model'])

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤,去执行下一遍
                    assert dev_wake_state == 'awake success', "得到的状态不是awake success，有可能设备没有唤醒成功。"

            with allure.step('step4-4: 进入开流页面，查看P2P连接结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备唤醒状态，日志中出现字符串 connectP2P {sn}connect Suc 表示p2p连接成功。
                dev_p2p_state = get_dev_p2p_state_result(click_time, device_data['iphone_model'], device_data['sn'])
                logger.info(f"第4-4步：获取到的p2p状态是：{dev_p2p_state}")

                if dev_p2p_state == f'connectP2P {device_data['sn']}connect Succ':
                    assert dev_p2p_state == f'connectP2P {device_data['sn']}connect Succ', \
                        "得到的状态不是connectP2P success，设备p2p没有连接成功。"
                else:
                    # 开流失败后等待30秒，等待iOS日志获取完成
                    time.sleep(30)

                    # p2p连接失败时处理
                    log_process_after_case_fail(driver, device_data['iphone_model'], device_data['dev_model'])

                    with allure.step('step4-2-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                    assert dev_p2p_state == f'connectP2P {device_data['sn']}connect Succ', \
                        "得到的状态不是connectP2P success，设备p2p没有连接成功。"

            with allure.step('step4-5: 进入开流页面，查看开流结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流结果，加载过程消失后开流成功或者失败
                play_state = get_dev_play_state_result(click_time, device_data['iphone_model'], device_data['sn'])
                logger.info(f"第4-5步：获取到的播放状态是：{play_state}")

                if play_state == 'previewSuccess':
                    assert play_state == 'previewSuccess', "得到的状态不是previewSuccess，开流失败。"
                else:
                    # 开流失败后等待30秒，等待iOS日志获取完成
                    time.sleep(30)

                    # 开流失败时处理
                    log_process_after_case_fail(driver, device_data['iphone_model'], device_data['dev_model'])

                    with allure.step('step4-5-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        driver.terminate_app(AOSU_PACKAGE_NAME)
                        driver.implicitly_wait(10)

                    # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                    assert play_state == 'previewSuccess', "得到的状态不是previewSuccess，开流失败。"

        with (((allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                            % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))))):
            # 开流页面左上角的 返回 按钮
            el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=PLAY_BACK_ICON)
            el.click()

            # 获取当前时间
            click_time = datetime.now()

            logger.info(f"第5步：点击开流页面左上角返回按钮的时间点是：{click_time}")

            # 根据不同的设备设定的时间不一样，例如C6L，20秒之内就休眠了
            time.sleep(device_data['sleep_time'])
            logger.info(f"第5步完成，回到首页等待设备休眠，休眠{device_data['sleep_time']}秒")

            # 判断设备是否休眠，日志中出现字符串 "deviceId":"{sn}","dp":"149","value":"0" 表示设备休眠成功。
            dev_dormancy_state = get_dev_dormancy_state_result(click_time, device_data['iphone_model'],
                                                               device_data['sn'])
            logger.info(f"第5步：获取到的休眠状态是：{dev_dormancy_state}")

            if dev_dormancy_state == f'{{"deviceId":"{device_data['sn']}","dp":"149","value":"0"}}':
                # 设置状态文件为休眠状态，下次执行step1的时候不用再等25秒
                logger.info("第5步：设备休眠成功！")
                # set_flag(True)

                assert dev_dormancy_state == f'{{"deviceId":"{device_data['sn']}","dp":"149","value":"0"}}', \
                    "得到的状态不是'dpStr={\"149\":false}' 设备休眠失败。"
            else:
                # 休眠失败后等待30秒，等待iOS日志获取完成
                time.sleep(30)

                # 设备唤醒失败时处理
                # 获取失败或者休眠失败，将状态置为False，这样在第一步中仍需要等待25秒
                # logger.info("第5步：休眠失败，将休眠标志设置为False，并开始错误处理获取app日志")
                # set_flag(False)

                log_process_after_case_fail(driver, device_data['iphone_model'], device_data['dev_model'])

                with allure.step('step5-1-1: 冷启app。step时间点：%s'
                                 % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                    driver.terminate_app(AOSU_PACKAGE_NAME)
                    driver.implicitly_wait(10)

                # 断言失败，用来结束本条用例后面的步骤，去执行下一遍
                assert dev_dormancy_state == f'{{"deviceId":"{device_data['sn']}","dp":"149","value":"0"}}', \
                    "得到的状态不是'dpStr={\"149\":false}' 设备休眠失败。"

                # 确认回到了首页
            assert is_element_present(driver, AppiumBy.ACCESSIBILITY_ID, HOME_PAGE_DEVICES) is not None, \
                "首页底部 ‘设备’标签 没有出现，没有回到首页。"
            logger.info("第5步，回到了首页，断言成功")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            logger.info("第6步：杀死app")
            driver.terminate_app(AOSU_PACKAGE_NAME)
            driver.implicitly_wait(10)
