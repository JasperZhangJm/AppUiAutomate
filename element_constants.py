AOSU_PACKAGE_NAME = 'com.glazero.ios'

# 按钮
ALLOW = '允许'
LOGIN = '登录'
NOT_NOW = '以后'
DONE = 'Done'
RETURN = 'Return'
YES = "确认"
LOGOUT = "退出登录"
GOT_IT = '知道了'
NEXT = '下一步'
CLOSE_ADS = 'close ads'
CLOSE_ICON_NAME = 'icon 24 close'
ICON_LOGO_NAME = 'icon_logo'

# 首页
HOME_PAGE_DRAWER = 'icon navigationbar drawer'
HOME_PAGE_ADD = 'icon navigationbar add'
HOME_PAGE_DEVICES = '设备'
HOME_PAGE_CLOUD = '云存储'
HOME_PAGE_ONLINE_SUPPORT = '在线客服'

# 侧边栏
PERSONAL_ICON_NAME = 'icon_drawer_personal'

# 开流页面左上角返回按钮
PLAY_BACK_ICON = 'playBack icon'
BACK_CLASS_CHAIN = '**/XCUIElementTypeButton[`name == "playBack icon"`]'
BACK_PREDICATE = 'name == "playBack icon"'

# 其他页面左上角返回按钮
ICON_24_BACK = 'icon 24 back'
CHINA_PREDICATE = 'name == "   中国  +86" AND visible == true'

# 登录页面
LOGIN_TYPE_STATIC_TEXT_1 = '**/XCUIElementTypeStaticText[`name == "登录"`][1]'
LOGIN_TYPE_STATIC_TEXT_2 = '**/XCUIElementTypeStaticText[`name == "登录"`][2]'
REGION_TYPE_TEXT_FIELD_CLASS_CHAIN_CN = '**/XCUIElementTypeTextField[`value == "中国 +86"`]'
COUNTRY_PREDICATE_CN = 'name == "   中国  +86" AND visible == true'
REGION_TYPE_OTHER_CLASS_CHAIN = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[4]'
EMAIL_TYPE_TEXT_FIELD_CLASS_CHAIN = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField'
PWD_TYPE_SECURE_TEXT_FIELD_CLASS_CHAIN = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField'
REGION_SEARCH = '**/XCUIElementTypeTextField[`value == "搜索"`]'

# 开流页面加载状态
OPEN_FLOW_STATUS = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther'
STREAM_LOADING_STATUS_NAME_1 = '实时视频加载中…'
STREAM_LOADING_STATUS_CLASS_CHAIN_1 = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeImage'
STREAM_LOADING_STATUS_NAME_2 = '正在建立访问通道…'
STREAM_LOADING_STATUS_CLASS_CHAIN_2 = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeImage'
STREAM_LOADING_STATUS_NAME_3 = '正在连接网络服务…'
STREAM_LOADING_STATUS_CLASS_CHAIN_3 = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeImage'
STREAM_LOADING_STATUS_NAME_4 = '实时视频加载中…'
STREAM_LOADING_STATUS_CLASS_CHAIN_4 = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeImage'
STREAM_LOADING_STATUS_NAME_5 = '加载较慢，尝试切换至流畅模式'
STREAM_LOADING_STATUS_CLASS_CHAIN_5 = '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeImage'
STREAM_LOADING_FAILED = '视频打开失败，请重试'

# 国家
CN_REGION_NAME = '   中国  +86'
US_REGION_NAME = '   美国  +1'
DE_REGION_NAME = '   德国  +49'

# Android
# 包名
ANDROID_PACKAGE_NAME = 'com.glazero.android'

# 启动页面
ANDROID_CREATE_ACCOUNT_REID = 'com.glazero.android:id/splash_create_account'

# 登录页面
ANDROID_LOGIN_REID = 'com.glazero.android:id/tv_title'
ANDROID_LOGIN_LOADING_REID = 'com.glazero.android:id/button_loading'
ANDROID_LOGIN_CLOSE_REID = 'com.glazero.android:id/img_title_close'

# 首页
ANDROID_MENU_REID = 'com.glazero.android:id/img_menu'
ANDROID_ADD_REID = 'com.glazero.android:id/img_add_device'
ANDROID_DEVICES_REID = 'com.glazero.android:id/tv_tab_device'
ANDROID_CLOUD_REID = 'com.glazero.android:id/tv_tab_playback'
ANDROID_ONLINE_SUPPORT_REID = 'com.glazero.android:id/tv_tab_service'
ANDROID_AD_CLOSE_REID = 'com.glazero.android:id/iv_close'

# 侧边栏
ANDROID_PERSONAL_ICON_REID = 'com.glazero.android:id/ivUserIcon'
ANDROID_USER_EMAIL_REID = 'com.glazero.android:id/tvUserEmail'
ANDROID_LOGOUT_XPATH = '//android.widget.TextView[@text="退出登录"]'
ANDROID_LOGOUT_TEXT = '退出登录'
ANDROID_LOGOUT_REID = 'com.glazero.android:id/tv_menu_item_name'
ANDROID_CONFIRM_REID = "com.glazero.android:id/btn_dialog_confirm"
ANDROID_REGION_SEARCH_REID = 'com.glazero.android:id/edit_search'
