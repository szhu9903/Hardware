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
    'COMM_HEARTBEAT_REPORT': {
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


    # Demo设备 全局
    # 登录请求 e -> s
    'DEMO_LOGIN_REQ': {
        'EVENT': '020101',
        'VALUE': bytes([0x2, 0x1, 0x1]),
    },
    # 登录响应 s -> e
    'DEMO_LOGIN_ACK': {
        'EVENT': '030101',
        'VALUE': bytes([0x3, 0x1, 0x1]),
    },

    # 设置LED请求 s->e
    'DEMO_SET_LED_COLOR_REQ': {
        'EVENT': '020201',
        'VALUE': bytes([0x2, 0x2, 0x1]),
    },
    # 设置LED响应 e -> s
    'DEMO_SET_LED_COLOR_ACK': {
        'EVENT': '030201',
        'VALUE': bytes([0x3, 0x2, 0x1]),
    },

    # 接收到温湿度数据 e -> s
    'DEMO_ENV_TH_REQ': {
        'EVENT': '020301',
        'VALUE': bytes([0x2, 0x3, 0x1]),
    },
    # 接收到温湿度数据响应 s -> e
    'DEMO_ENV_TH_ACK': {
        'EVENT': '030301',
        'VALUE': bytes([0x3, 0x3, 0x1]),
    },
    # 发送查询温湿度指令 s -> e
    'DEMO_QUERY_ENV_TH_REQ': {
        'EVENT': '010302',
        'VALUE': bytes([0x1, 0x3, 0x2]),
    },
    # 发送查询温湿度指令 响应 e -> s
    'DEMO_QUERY_ENV_TH_ACK': {
        'EVENT': '030302',
        'VALUE': bytes([0x3, 0x3, 0x2]),
    },

    # RTC 服务发送当前时间 s -> e
    'DEMO_RTC_SET_DATETIME_REQ': {
        'EVENT': '020401',
        'VALUE': bytes([0x2, 0x4, 0x1]),
    },
    # RTC 服务发送当前时间 响应 e -> s
    'DEMO_RTC_SET_DATETIME_ACK': {
        'EVENT': '030401',
        'VALUE': bytes([0x3, 0x4, 0x1]),
    }

}


from . import server_handler
from . import demo_handler

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

}



