#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：down_message.py
@Author  ：szhu9903
@Date    ：2022/11/17 16:02 
'''

import struct, json
from twisted.python import log
from twisted.internet import reactor

from utils.generic_func import get_check_sum
from config import sys_config

# 基于下发消息构建消息
def create_message(dst_equip_code, event_no_data, msg_body_data, protocol):
    result_message = dict()

    result_message['PROTOCOL'] = protocol
    # 消息头
    msg_data = bytes([0x5B, 0x7C])
    msg_data = msg_data + struct.pack('!H', int(dst_equip_code))
    msg_data = msg_data + bytes.fromhex(event_no_data) # === struct.pack('3B', 1, ff, 3)

    msg_data = msg_data + bytes([len(msg_body_data)])
    msg_data = msg_data + msg_body_data
    check_sum = get_check_sum(msg_data[4 : 8 + len(msg_body_data)])
    # 校验和
    msg_data = msg_data + bytes([check_sum])
    msg_data = msg_data + bytes([0x0D, 0x0A])

    result_message['DATA'] = msg_data

    return result_message

# 发送消息
def protocol_send_message(message):
    message['PROTOCOL'].transport.write(message['DATA'])
    log.msg('CommFunc:Send data(ip:%s,port:%s)' % (message['PROTOCOL'].client_host, message['PROTOCOL'].client_port))

# 公共发送消息
def send_message(message):
    reactor.callFromThread(protocol_send_message, message)

# 下发下行消息
def send_downstream_message(down_stream_message):
    # 构建设置消息
    new_message = create_message(down_stream_message['equip_code'],
                                 down_stream_message['event_no_hex'],
                                 down_stream_message.get('msg_body_data') or bytes([]),
                                 down_stream_message['protocol'])
    # 发送请求消息
    send_message(new_message)

# 下发消息到设备
def send_message_to_equip(equip_code, event_no_hex, msg_body_data, protocol):
    node_pair = str(equip_code)

    if node_pair not in sys_config['protocols'].keys():
        log.err(f'[Down Message]:No connection for {equip_code}, skipped')
        return False
    protocol = protocol or sys_config['protocols'][node_pair]

    down_stream_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_stream_messsage)
    return True






