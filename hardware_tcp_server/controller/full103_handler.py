#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：hardware_tcp_server 
@File    ：full1033_handler.py
@Author  ：szhu9903
@Date    ：2023/2/27 19:49 
'''

import time
import struct
import datetime
from twisted.python import log
from . import event_meta
from .login_handler import default_equip_login
from comm.down_message import send_downstream_message,send_message_to_equip
from utils.RedisExecute import RedisExecute
from .helper.demo_funcs import full103_env_update_helper

# full103设备登录  021001
def full103_login(message):
    default_equip_login(message, event_meta['FULL103_LOGIN_ACK']['EVENT'], 'ES Controller')


# full103配置更新 021002
def full103_config_set_req(equip_code, event_no_hex, msg_body_json, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!B', msg_body_json['FULL103_REPORT_ENV_INTERVAL'])
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send set config', system="REQ")

# full103配置更新响应 031002
def full103_config_set_ack(message):
    log.msg(f"{message['EQUIP_CODE']}set config", system="ACK")

# 温湿度 接收到数据 021101
def full103_env_th_req(message):
    full103_env_update_helper(message)
    # ACK
    down_stream_messsage = {
        'equip_code': message['EQUIP_CODE'],
        'event_no_hex': event_meta['FULL103_ENV_TH_ACK']['EVENT'],
        'msg_body_data': bytes([]),
        'protocol': message['PROTOCOL']
    }
    send_downstream_message(down_stream_messsage)

# 温湿度 下发查询指令 011102
def full103_query_env_th_req(equip_code, event_no_hex, message_body, protocol):
    send_message_to_equip(equip_code, event_no_hex, message_body, protocol)
    log.msg(f'{equip_code} send Query Env', system="011102-REQ")

# 温湿度 查询环境数据响应 031102
def full103_query_env_th_ack(message):
    full103_env_update_helper(message)
    RedisExecute.redis_cmd_ack_set(event_meta['FULL103_QUERY_ENV_TH_ACK']['EVENT'], message['EQUIP_CODE'])
    log.msg(f"{message['EQUIP_CODE']} send Query Env", system="031102-ACK")

# 设置Full103继电器开关 021201
def full103_relay_switch_set_req(equip_code, event_no_hex, msg_body_json, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!B', msg_body_json['relay_switch'])
    msg_body_data += struct.pack('!B', msg_body_json['relay_control'])
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send set relay switch', system="REQ")

# 设置Full103设备继电器开关响应 031201
def full103_relay_switch_set_ack(message):
    log.msg(f"{message['EQUIP_CODE']}set relay switch", system="ACK")
