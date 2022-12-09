#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：timetask.py
@Author  ：szhu9903
@Date    ：2022/11/17 14:16 
'''
import time
import json
import traceback
from twisted.python import log
from controller import message_map
from utils.mysql_db import MysqlPool
from utils.RedisExecute import RedisExecute
from config import thread_data, sys_config

def deal_upstream_message(req_message):  # twist定时主动回调
    thread_data.connection = MysqlPool.get_idle_connection()
    try:
        # 如果节点已经存在，替换为新链路,关闭老链路
        new_node_pair = str(req_message['EQUIP_CODE'])
        if new_node_pair in sys_config['protocols'].keys() and req_message['PROTOCOL'] not in sys_config['protocols'].values():
            old_protocol = sys_config['protocols'][new_node_pair]
            log.err('CommFunc:repeat node(%s), old link break(%s) forcely.' % (new_node_pair,
                                                                               str(old_protocol.transport.getPeer())))

            sys_config['protocols'][new_node_pair] = req_message['PROTOCOL']
            log.err('CommFunc:%s new link (%s)' % (new_node_pair,
                                                   str(req_message['PROTOCOL'].transport.getPeer())))
            log.err('CommFunc:new link status(%s)' % str(list(sys_config['protocols'].keys())))
            old_protocol.transport.abortConnection()

        req_message['PROTOCOL'].last_message_time = time.time()

        # 获取消息函数，处理消息
        message_map[req_message['EVENT_NO']]['func'](req_message)
    except Exception as Err:
        traceback.print_exc()
        log.err('CommFunc:Deal upstream message err:%s' % str(Err))
    finally:
        MysqlPool.resume_idle_connection(thread_data.connection)


# 定时读取下行消息表
def deal_downstream_message(channel, method, properties, body):
    try:
        body_dict = json.loads(body)
        mode = body_dict['MODE']
        event_no = body_dict['EVENT_NO']
        msg_body = body_dict['DATA']

        # 检查处理函数是否存在
        if event_no not in message_map.keys():
            log.msg('event_id=%s not event' % event_no, system="server")
            return None

        # 根据消息类型执行消息
        if mode == "ALL":
            for equip, protocol in sys_config['protocols'].items():
                message_map[event_no]['func'](equip, event_no, msg_body, protocol)

        elif mode == 'TYPE':
            equip_type = body_dict['EQUIP_TYPE']
            equip_list = RedisExecute.redis_smembers(equip_type)
            for equip_no in equip_list:
                if equip_no in sys_config['protocols'].keys():
                    message_map[event_no]['func'](int(equip_no), event_no, msg_body, sys_config['protocols'][equip_no])

        else:
            equip_no = body_dict['EQUIP_NO']
            node_pair = str(equip_no)
            if node_pair not in sys_config['protocols'].keys():
                log.err(f'[Down Message]:No connection for {equip_no}, skipped')
                return None
            message_map[event_no]['func'](equip_no, event_no, msg_body, sys_config['protocols'][node_pair])

    except Exception as Err:
        traceback.print_exc()
        log.err(f'down message error :{str(Err)}', system="ERROR")
    finally:
        # 发送ack
        channel.basic_ack(delivery_tag = method.delivery_tag)


# 检测心跳状态，发送设备在线请求到设备端
def check_equip_status():
    thread_data.connection = MysqlPool.get_idle_connection()
    update_equip_status = "UPDATE Hardware_Equip SET he_equipstatus='BROKEN' WHERE he_num=%s"
    while True:
        try:
            for equip_key, equip_val  in sys_config['protocols'].items():
                if (time.time() - equip_val.last_message_time) > 100:
                    # 超时更新设备登录状态
                    MysqlPool.insert_data_db(update_equip_status, (equip_key,))

        except Exception as Err:
            traceback.print_exc()
            log.err('CommFunc:Error in query equip node status:%s' % str(Err))
        time.sleep(10)  # 更新周期30s
