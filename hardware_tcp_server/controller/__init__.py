#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：__init__.py
@Author  ：szhu9903
@Date    ：2022/11/17 14:22 
'''

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
    'DEMO_LOGIN_REQ': { # 登录请求 e -> s
        'EVENT': '020101',
        'VALUE': bytes([0x2, 0x1, 0x1]),
    },
    'DEMO_LOGIN_ACK': { # 登录响应 s -> e
        'EVENT': '030101',
        'VALUE': bytes([0x3, 0x1, 0x1]),
    },
    'DEMO_CONFIG_SET_REQ': { # 设置DEMO设备参数请求 s->e
        'EVENT': '020102',
        'VALUE': bytes([0x2, 0x1, 0x2]),
    },
    'DEMO_CONFIG_SET_ACK': { # 设置DEMO设备参数响应 e -> s
        'EVENT': '030102',
        'VALUE': bytes([0x3, 0x1, 0x2]),
    },
    'DEMO_SET_LED_COLOR_REQ': { # 设置LED请求 s->e
        'EVENT': '020201',
        'VALUE': bytes([0x2, 0x2, 0x1]),
    },
    'DEMO_SET_LED_COLOR_ACK': { # 设置LED响应 e -> s
        'EVENT': '030201',
        'VALUE': bytes([0x3, 0x2, 0x1]),
    },
    'DEMO_ENV_TH_REQ': { # 接收到温湿度数据 e -> s
        'EVENT': '020301',
        'VALUE': bytes([0x2, 0x3, 0x1]),
    },
    'DEMO_ENV_TH_ACK': { # 接收到温湿度数据响应 s -> e
        'EVENT': '030301',
        'VALUE': bytes([0x3, 0x3, 0x1]),
    },
    'DEMO_QUERY_ENV_TH_REQ': { # 发送查询温湿度指令 s -> e
        'EVENT': '010302',
        'VALUE': bytes([0x1, 0x3, 0x2]),
    },
    'DEMO_QUERY_ENV_TH_ACK': { # 发送查询温湿度指令 响应 e -> s
        'EVENT': '030302',
        'VALUE': bytes([0x3, 0x3, 0x2]),
    },
    'DEMO_RTC_SET_DATETIME_REQ': { # RTC 服务发送当前时间 s -> e
        'EVENT': '020401',
        'VALUE': bytes([0x2, 0x4, 0x1]),
    },
    'DEMO_RTC_SET_DATETIME_ACK': { # RTC 服务发送当前时间 响应 e -> s
        'EVENT': '030401',
        'VALUE': bytes([0x3, 0x4, 0x1]),
    },


    # Full103设备 全局
    'FULL103_LOGIN_REQ': { # 登录请求 e -> s
        'EVENT': '021001',
        'VALUE': bytes([0x2, 0x10, 0x1]),
    },
    'FULL103_LOGIN_ACK': { # 登录响应 s -> e
        'EVENT': '031001',
        'VALUE': bytes([0x3, 0x10, 0x1]),
    },
    'FULL103_CONFIG_SET_REQ': { # 设置Full103设备参数请求 s->e
        'EVENT': '021002',
        'VALUE': bytes([0x2, 0x10, 0x2]),
    },
    'FULL103_CONFIG_SET_ACK': { # 设置Full103设备参数响应 e -> s
        'EVENT': '031002',
        'VALUE': bytes([0x3, 0x10, 0x2]),
    },
    'FULL103_ENV_TH_REQ': { # 接收到温湿度数据 e -> s
        'EVENT': '021101',
        'VALUE': bytes([0x2, 0x11, 0x1]),
    },
    'FULL103_ENV_TH_ACK': { # 接收到温湿度数据响应 s -> e
        'EVENT': '031101',
        'VALUE': bytes([0x3, 0x11, 0x1]),
    },
    'FULL103_QUERY_ENV_TH_REQ': { # 发送查询温湿度指令 s -> e
        'EVENT': '011102',
        'VALUE': bytes([0x1, 0x11, 0x2]),
    },
    'FULL103_QUERY_ENV_TH_ACK': { # 发送查询温湿度指令 响应 e -> s
        'EVENT': '031102',
        'VALUE': bytes([0x3, 0x11, 0x2]),
    },
    'FULL103_RELAY_SWITCH_SET_REQ': {  # 设置Full103继电器开关 s->e
        'EVENT': '021201',
        'VALUE': bytes([0x2, 0x12, 0x1]),
    },
    'FULL103_RELAY_SWITCH_SET_ACK': {  # 设置Full103设备继电器开关响应 e -> s
        'EVENT': '031201',
        'VALUE': bytes([0x3, 0x12, 0x1]),
    },

}


from . import server_handler
from . import demo_handler
from . import full103_handler

# 消息函数映射
message_map = {
    # 公共
    event_meta['COMM_HEARTBEAT_REPORT']['EVENT']: {  # 硬件设备上报心跳
        'event': event_meta['COMM_HEARTBEAT_REPORT']['VALUE'],
        'equiptype': 'ALL',
        'func': server_handler.message_comm_beat_report,
        'operation': 'EQUIP_BEATHEART_REPORT'
    },
    event_meta['COMM_HEARTBEAT_INTER_REQ']['EVENT']: {  # 设置心跳间隔请求
        'event': event_meta['COMM_HEARTBEAT_INTER_REQ']['VALUE'],
        'equiptype': 'ALL',
        'func': server_handler.message_comm_beat_inter_req,
        'operation': 'EQUIP_BEATHEARTINTER'
    },
    event_meta['COMM_HEARTBEAT_INTER_ACK']['EVENT']: {  # 设置心跳间隔响应
        'event': event_meta['COMM_HEARTBEAT_INTER_ACK']['VALUE'],
        'equiptype': 'ALL',
        'func': server_handler.message_comm_beat_inter_ack,
        'operation': 'EQUIP_BEATHEARTINTER'
    },
    event_meta['COMM_HE_NUM_SET_REQ']['EVENT']: {  # 设置编号请求
        'event': event_meta['COMM_HE_NUM_SET_REQ']['VALUE'],
        'equiptype': 'ALL',
        'func': server_handler.message_he_num_set_req,
        'operation': 'EQUIP_NUM'
    },
    event_meta['COMM_HE_NUM_SET_ACK']['EVENT']: {  # 设置编号响应
        'event': event_meta['COMM_HE_NUM_SET_ACK']['VALUE'],
        'equiptype': 'ALL',
        'func': server_handler.message_he_num_set_ack,
        'operation': 'EQUIP_NUM'
    },

    # Demo
    event_meta['DEMO_LOGIN_REQ']['EVENT']: {  # 登录请求
        'event': event_meta['DEMO_LOGIN_REQ']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_login,
        'operation': 'DEMO_LOGIN',
    },
    event_meta['DEMO_LOGIN_ACK']['EVENT']: {  # 登录响应
        'event': event_meta['DEMO_LOGIN_ACK']['VALUE'],
        'equiptype': 'DEMO',
        'func': None,
        'operation': 'DEMO_LOGIN',
    },
    event_meta['DEMO_CONFIG_SET_REQ']['EVENT']: {  # 推送设备配置
        'event': event_meta['DEMO_CONFIG_SET_REQ']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_config_set_req,
        'operation': 'DEMO_CONFIG',
    },
    event_meta['DEMO_CONFIG_SET_ACK']['EVENT']: {  # 设备发送接收推送配置的响应
        'event': event_meta['DEMO_CONFIG_SET_ACK']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_config_set_ack,
        'operation': 'DEMO_CONFIG',
    },
    event_meta['DEMO_SET_LED_COLOR_REQ']['EVENT']: {  # 推送LED
        'event': event_meta['DEMO_SET_LED_COLOR_REQ']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_led_color_req,
        'operation': 'DEMO_LED',
    },
    event_meta['DEMO_SET_LED_COLOR_ACK']['EVENT']: {  # 设备发送接收推送LED的响应
        'event': event_meta['DEMO_SET_LED_COLOR_ACK']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_led_color_ack,
        'operation': 'DEMO_LED',
    },
    event_meta['DEMO_ENV_TH_REQ']['EVENT']: {  # 接收到环境数据
        'event': event_meta['DEMO_ENV_TH_REQ']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_env_th_req,
        'operation': 'DEMO_ENV',
    },
    event_meta['DEMO_ENV_TH_ACK']['EVENT']: {  # 接收到环境数据响应
        'event': event_meta['DEMO_ENV_TH_ACK']['VALUE'],
        'equiptype': 'DEMO',
        'func': None,
        'operation': 'DEMO_ENV',
    },
    event_meta['DEMO_QUERY_ENV_TH_REQ']['EVENT']: {  # 发送查询环境数据
        'event': event_meta['DEMO_QUERY_ENV_TH_REQ']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_query_env_th_req,
        'operation': 'DEMO_QUERY_ENV',
    },
    event_meta['DEMO_QUERY_ENV_TH_ACK']['EVENT']: {  # 查询环境数据响应
        'event': event_meta['DEMO_QUERY_ENV_TH_ACK']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_query_env_th_ack,
        'operation': 'DEMO_QUERY_ENV',
    },
    event_meta['DEMO_RTC_SET_DATETIME_REQ']['EVENT']: {  # 推送当前时间
        'event': event_meta['DEMO_RTC_SET_DATETIME_REQ']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_rtc_set_datetime_req,
        'operation': 'DEMO_RTC',
    },
    event_meta['DEMO_RTC_SET_DATETIME_ACK']['EVENT']: {  # 设备发送接收时间的响应
        'event': event_meta['DEMO_RTC_SET_DATETIME_ACK']['VALUE'],
        'equiptype': 'DEMO',
        'func': demo_handler.demo_rtc_set_datetime_ack,
        'operation': 'DEMO_RTC',
    },

    # Full103
    event_meta['FULL103_LOGIN_REQ']['EVENT']: {  # 登录请求
        'event': event_meta['FULL103_LOGIN_REQ']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_login,
        'operation': 'FULL103_LOGIN',
    },
    event_meta['FULL103_LOGIN_ACK']['EVENT']: {  # 登录响应
        'event': event_meta['FULL103_LOGIN_ACK']['VALUE'],
        'equiptype': 'FULL103',
        'func': None,
        'operation': 'FULL103_LOGIN',
    },
    event_meta['FULL103_CONFIG_SET_REQ']['EVENT']: {  # 推送设备配置
        'event': event_meta['FULL103_CONFIG_SET_REQ']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_config_set_req,
        'operation': 'FULL103_CONFIG',
    },
    event_meta['FULL103_CONFIG_SET_ACK']['EVENT']: {  # 设备发送接收推送配置的响应
        'event': event_meta['FULL103_CONFIG_SET_ACK']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_config_set_ack,
        'operation': 'FULL103_CONFIG',
    },
    event_meta['FULL103_ENV_TH_REQ']['EVENT']: {  # 接收到环境数据
        'event': event_meta['FULL103_ENV_TH_REQ']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_env_th_req,
        'operation': 'FULL103_ENV',
    },
    event_meta['FULL103_ENV_TH_ACK']['EVENT']: {  # 接收到环境数据响应
        'event': event_meta['FULL103_ENV_TH_ACK']['VALUE'],
        'equiptype': 'FULL103',
        'func': None,
        'operation': 'FULL103_ENV',
    },
    event_meta['FULL103_QUERY_ENV_TH_REQ']['EVENT']: {  # 发送查询环境数据
        'event': event_meta['FULL103_QUERY_ENV_TH_REQ']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_query_env_th_req,
        'operation': 'FULL103_QUERY_ENV',
    },
    event_meta['FULL103_QUERY_ENV_TH_ACK']['EVENT']: {  # 查询环境数据响应
        'event': event_meta['FULL103_QUERY_ENV_TH_ACK']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_query_env_th_ack,
        'operation': 'FULL103_QUERY_ENV',
    },
    event_meta['FULL103_RELAY_SWITCH_SET_REQ']['EVENT']: {  # 推送设备配置
        'event': event_meta['FULL103_RELAY_SWITCH_SET_REQ']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_relay_switch_set_req,
        'operation': 'FULL103_RELAY',
    },
    event_meta['FULL103_RELAY_SWITCH_SET_ACK']['EVENT']: {  # 设备发送接收推送配置的响应
        'event': event_meta['FULL103_RELAY_SWITCH_SET_ACK']['VALUE'],
        'equiptype': 'FULL103',
        'func': full103_handler.full103_relay_switch_set_ack,
        'operation': 'FULL103_RELAY',
    },

}



