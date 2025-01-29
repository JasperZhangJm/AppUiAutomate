# AppUiAutomate
主要是iOS UI 自动化，该框架也可以进行Android UI 自动化

一、执行前需要确认，本地挂载目录是否生效：
  1、挂载iOS沙盒目录：ifuse ~/ios_sandbox/iPhoneX --container com.glazero.ios --udid f89d929e8c45a81c0fe2d22f80c1a36e227e90ef
    （f89d929e8c45a81c0fe2d22f80c1a36e227e90ef 是 iphone X的udid，udid通过idevice_id查看）；
  2、挂载后查看挂载目录，可以看到Document/Logs/目录下的app业务日志；
  3、如果挂载关系在，但是看不到挂载目录下的沙盒日志，需要先卸载挂载的目录，执行：umount ~/ios_sandbox/iPhoneX；
  4、重新挂载（命令与第一步相同）。
注：换包时需要重新挂载、拔插数据线时需要重新挂载。

二、测试数据中用到的数据有 app登录数据、测试设备信息、网络请求数据、iPhone手机信息：
  1、app登录数据用的是：test_data_fixture.py中的LOGIN_DATA
  2、测试设备信息用的是：test_data_fixture.py中的device_data
  3、网络请求数据用的是：test_data_fixture.py中的REQUEST_DATA
  4、iPhone手机信息在devices_conf.yaml中存储

三、在代码中修改的地方有：
  1、在devices_conf.yaml中添加iPhone手机信息，格式参考已有的数据；
  2、在test_data_fixture.py中的LOGIN_DATA添加登录信息，格式参考已有的数据；
  3、在test_data_fixture.py中的device_data添加设备信息，格式参考已有的数据；

四、在终端中执行测试脚本，命令如下：
  pytest -q -s -ra --count=200  test_open_stream.py::TestOpenStream::test_c8s_open_stream --alluredir=./report/C8S/resource | tee pytest_summary.log

五、执行完成后会生成两个日志文件：
  1、pytest_project_log.txt 测试脚本运行日志，记录关键节点信息，用于调试测试脚本；
  2、pytest_summary.log pytest summary日志，输出pytest的统计结果，用于查看最后结果；

六、测试结果包含两部分：
  1、allure报告部分，例如，report/C8S/resource
  2、开流节点时间统计部分，记录在根目录下的data.xlsx中

七、保存测试完成后的app日志

八、iOS app可以用debug包和release包，因为debug包现在有内存泄漏提示弹窗，所以现在用release包。
