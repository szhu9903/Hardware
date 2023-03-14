

default_result = {
    'status': 200,
    'code': 0x06,
    'data': None,
    'message': '请求成功'
}

default_limit_size = 300

default_page_data = {
    "page_size": 10,
    "page_index": 1
}

# 补充登录用户数据字段
add_user_col = {
    # 'bloglikelog': 'bll_userid',
    # 'blog': 'b_createuid',
}

# 查询子表数据
depth_data_map = {
    # hardware equip
    "he_type": {
        "tab_name": "hardwaretype",
        "link_column": "he_type:id",
    },
    # hardware config var
    "hcv_type": {
        "tab_name": "hardwaretype",
        "link_column": "hcv_type:id",
    },

    # Demo LED
    "dl_equip": {
        "tab_name": "hardwareequip",
        "link_column": "dl_equipid:id",
    },
    # Demo ENV
    "de_equip": {
        "tab_name": "hardwareequip",
        "link_column": "de_equipid:id",
    },

    # user
    "u_role": {
        "tab_name": "urrelation",
        "link_column": "id:ur_userid",
        "sub_tab": {
            "tab_name": "sysrole",
            "link_column": "ur_roleid:id",
        }
    },
    # role
    "r_purview": {
        "tab_name": "rprelation",
        "link_column": "id:rp_roleid",
        "sub_tab": {
            "tab_name": "syspurview",
            "link_column": "rp_purviewid:id",
        }
    },
    "r_menu": {
        "tab_name": "rmrelation",
        "link_column": "id:rm_roleid",
        "sub_tab": {
            "tab_name": "sysmenu",
            "link_column": "rm_menuid:id",
        }
    }
}

# 提交组合配置
depth_post_map = {
    # user
    "u_role": {
        "tab_name": "urrelation",
        "link_column": "id:ur_userid",
    },
    # role
    "r_purview": {
        "tab_name": "rprelation",
        "link_column": "id:rp_roleid",
    },
    "r_menu": {
        "tab_name": "rmrelation",
        "link_column": "id:rm_roleid",
    }
}


error_info_map = {
    'uk_sys_user_su_account': '用户重复',
    'uk_sys_role_sr_name': '角色重复',
    'uk_hardware_type_ht_name': '设备分类重复',
    'uk_hardware_equip_he_num': '设备重复',
    'uk_sys_configvar_hcv_type_scv_variablekey': '设备配置重复',
    'uk_demo_env_de_equipid': '环境参数重复',
    'uk_demo_led_dl_equipid': '设备LED重复',
}


from enum import Enum

class HardwareType(Enum):
    demo = 1
    full103 = 2

event_meta = {
    # 公共
    'COMM_HEARTBEAT_REPORT': {  # 心跳
        'EVENT': '020001',
        'VALUE': bytes([0x2, 0x0, 0x1])
    },
    'COMM_HEARTBEAT_INTER_REQ': {  # 发送心跳间隔配置到设备
        'EVENT': '020002',
        'VALUE': bytes([0x2, 0x0, 0x2])
    },
    'COMM_HEARTBEAT_INTER_ACK': {  # 设备响应心跳间隔配置信息
        'EVENT': '030002',
        'VALUE': bytes([0x3, 0x0, 0x2])
    },
    'COMM_HE_NUM_SET_REQ': {  # 设置设备编号请求 s->e
        'EVENT': '020003',
        'VALUE': bytes([0x2, 0x0, 0x3])
    },
    'COMM_HE_NUM_SET_ACK': {  # 设置设备编号响应 e -> s
        'EVENT': '030003',
        'VALUE': bytes([0x3, 0x0, 0x3])
    },

    # Demo设备 全局
    'DEMO_LOGIN_REQ': {  # 登录请求 e -> s
        'EVENT': '020101',
        'VALUE': bytes([0x2, 0x1, 0x1]),
    },
    'DEMO_LOGIN_ACK': {  # 登录响应 s -> e
        'EVENT': '030101',
        'VALUE': bytes([0x3, 0x1, 0x1]),
    },
    'DEMO_CONFIG_SET_REQ': {  # 设置DEMO设备参数请求 s->e
        'EVENT': '020102',
        'VALUE': bytes([0x2, 0x1, 0x2]),
    },
    'DEMO_CONFIG_SET_ACK': {  # 设置DEMO设备参数响应 e -> s
        'EVENT': '030102',
        'VALUE': bytes([0x3, 0x1, 0x2]),
    },
    'DEMO_SET_LED_COLOR_REQ': {  # 设置LED请求 s->e
        'EVENT': '020201',
        'VALUE': bytes([0x2, 0x2, 0x1]),
    },
    'DEMO_SET_LED_COLOR_ACK': {  # 设置LED响应 e -> s
        'EVENT': '030201',
        'VALUE': bytes([0x3, 0x2, 0x1]),
    },
    'DEMO_ENV_TH_REQ': {  # 接收到温湿度数据 e -> s
        'EVENT': '020301',
        'VALUE': bytes([0x2, 0x3, 0x1]),
    },
    'DEMO_ENV_TH_ACK': {  # 接收到温湿度数据响应 s -> e
        'EVENT': '030301',
        'VALUE': bytes([0x3, 0x3, 0x1]),
    },
    'DEMO_QUERY_ENV_TH_REQ': {  # 发送查询温湿度指令 s -> e
        'EVENT': '010302',
        'VALUE': bytes([0x1, 0x3, 0x2]),
    },
    'DEMO_QUERY_ENV_TH_ACK': {  # 发送查询温湿度指令 响应 e -> s
        'EVENT': '030302',
        'VALUE': bytes([0x3, 0x3, 0x2]),
    },
    'DEMO_RTC_SET_DATETIME_REQ': {  # RTC 服务发送当前时间 s -> e
        'EVENT': '020401',
        'VALUE': bytes([0x2, 0x4, 0x1]),
    },
    'DEMO_RTC_SET_DATETIME_ACK': {  # RTC 服务发送当前时间 响应 e -> s
        'EVENT': '030401',
        'VALUE': bytes([0x3, 0x4, 0x1]),
    },

    # Full103设备 全局
    'FULL103_LOGIN_REQ': {  # 登录请求 e -> s
        'EVENT': '021001',
        'VALUE': bytes([0x2, 0x10, 0x1]),
    },
    'FULL103_LOGIN_ACK': {  # 登录响应 s -> e
        'EVENT': '031001',
        'VALUE': bytes([0x3, 0x10, 0x1]),
    },
    'FULL103_CONFIG_SET_REQ': {  # 设置Full103设备参数请求 s->e
        'EVENT': '021002',
        'VALUE': bytes([0x2, 0x10, 0x2]),
    },
    'FULL103_CONFIG_SET_ACK': {  # 设置Full103设备参数响应 e -> s
        'EVENT': '031002',
        'VALUE': bytes([0x3, 0x10, 0x2]),
    },
    'FULL103_ENV_TH_REQ': {  # 接收到温湿度数据 e -> s
        'EVENT': '021101',
        'VALUE': bytes([0x2, 0x11, 0x1]),
    },
    'FULL103_ENV_TH_ACK': {  # 接收到温湿度数据响应 s -> e
        'EVENT': '031101',
        'VALUE': bytes([0x3, 0x11, 0x1]),
    },
    'FULL103_QUERY_ENV_TH_REQ': {  # 发送查询温湿度指令 s -> e
        'EVENT': '011102',
        'VALUE': bytes([0x1, 0x11, 0x2]),
    },
    'FULL103_QUERY_ENV_TH_ACK': {  # 发送查询温湿度指令 响应 e -> s
        'EVENT': '031102',
        'VALUE': bytes([0x3, 0x11, 0x2]),
    },

}


config_map = {
    HardwareType.demo: 'DEMO_CONFIG_SET_REQ',
    HardwareType.full103: 'FULL103_CONFIG_SET_REQ',
}

