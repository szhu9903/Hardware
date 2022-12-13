#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：blog_server 
@File    ：async_func.py
@Author  ：szhu9903
@Date    ：2022/12/8 23:35 
'''

import copy
import json
import datetime
import gevent

from flask import g
from . import async_config
from app.comm.FlaskRabbitMQ import FlaskRabbitMQ
from app.comm.RedisExecute import RedisExecute

def get_command_ack(ack_eventid, equip_code):
    """
    查询响应消息
    :param ack_eventid: 响应消息编码
    :param equip_code:  设备编码
    :return:
    """
    for i in range(async_config.GET_ACK_COUNT):
        gevent.sleep(async_config.GET_ACK_TIME_INTERVAL)
        if RedisExecute.redis_cmd_ack_getdel(ack_eventid, equip_code) == b'OK':
            return True
    return False


def general_deal_message(ws_message, ws_socket):
    try:  # 获取并检查消息格式
        equip_code = ws_message['equip_code']
        message_data = ws_message['message_data']
        map_meta = async_config.async_cmd_map[ws_message['event']]
        req_eventid = map_meta['req_event']
        ack_eventid = map_meta['ack_event']
    except Exception as err:
        raise ValueError('参数不完整')

    # 如果需要发送消息
    if req_eventid:
        FlaskRabbitMQ.send_to_equip(int(equip_code), req_eventid, message_data)

    # 等待响应结果
    if get_command_ack(ack_eventid, equip_code):
        g.result['code'] = 0x06
        g.result['message'] = '接收到设备响应'
    else:
        g.result['code'] = 0x53
        g.result['message'] = '错误,等待响应超时.'
    ws_socket.send(json.dumps(g.result))


