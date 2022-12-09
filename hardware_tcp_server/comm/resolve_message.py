#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：resolve_message.py
@Author  ：szhu9903
@Date    ：2022/11/16 17:29 
'''

import struct
from twisted.python import log
from controller import message_map
from utils.RedisExecute import RedisExecute
from utils.generic_func import get_check_sum, get_equip_type
from config import sys_config

# 上行消息格式化
def extract_req_message(data, protocol):
    """
    args:
        data: 消息体
        protocol: 链接对象
    return：dict()
        EQUIP_CODE: 设备编码
        MSG_LENGTH: 消息体长度
        MSG_BODY: 消息体
        MSG_HEAD: 消息头
        MSG_TAIL: 消息尾
        PROTOCOL: 本消息的链接
        EVENT_NO: 消息编码
    """
    # 解析消息头 : 帧头、设备编码、帧类型、指令类型、指令编码、参数长度
    frame_head, equip, frame_type, cmd_type, cmd_code, msg_length = \
        struct.unpack('!2H4B', data[0:8])

    # 解析消息尾 : 校验位 帧尾
    frame_check, _ = struct.unpack('!BH', data[-3:])

    # 检测校验和
    if get_check_sum(data[4:8+msg_length]) != frame_check:
        log.err('校验位错误!', system='ERROR')
        return None

    # 获取节点 分类
    equip_type = get_equip_type(equip)

    # 检查节点是否合法
    if not RedisExecute.redis_sismember(equip_type, str(equip)):
        log.err(f'非法节点(equip_id={equip},equip_type={equip_type})!', system='ERROR')
        return None

    # 解析消息体
    msg_head = data[0:8]
    msg_body = data[8:8 + msg_length]
    msg_tail = data[-3:]

    req_message = dict()

    req_message['EQUIP_CODE'] = equip

    # 检查事件号是否存在对应处理函数
    req_message['EVENT_NO'] = '%02X%02X%02X' % (frame_type, cmd_type, cmd_code)
    if req_message['EVENT_NO'] not in message_map.keys():
        log.err('CommFunc:Invalid event(event_id=%s,equip_id=%s), '
                'no match func or invalid event, discard!'
                % (req_message['EVENT_NO'], equip))
        return None

    req_message['MSG_LENTH'] = msg_length
    req_message['MSG_HEAD'] = msg_head
    req_message['MSG_BODY'] = msg_body
    req_message['MSG_TAIL'] = msg_tail
    # 记录本消息的链接,以便应答
    req_message['PROTOCOL'] = protocol

    # 合法的消息，记录其远端链接 刷新消息时间
    if str(equip) not in sys_config['protocols'].keys():
        protocol.equip_id = str(equip)
        sys_config['protocols'][str(equip)] = protocol

    return req_message


