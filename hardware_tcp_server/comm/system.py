#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：system.py
@Author  ：szhu9903
@Date    ：2022/11/18 16:42 
'''
import json
import sys
import datetime
from twisted.python import log
from collections import defaultdict
from config import sys_config, thread_data
from utils.mysql_db import MysqlPool
from utils.RedisExecute import RedisExecute

def sys_param_init():
    """ 初始化系统参数 """
    thread_data.connection = MysqlPool.get_idle_connection()
    try:
        # 当前时间作为解析消息的起始时间，历史消息不解析
        sys_config['last_stamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.msg('CommFunc:Init event_last_stamp:%s' % sys_config['last_stamp'])

        # 初始化设备分类列表
        reflesh_equiptype()
        # 初始化节点列表
        reflesh_equipid()

        log.msg('Init OK!',  system="SYS")
    except Exception as Err:
        log.msg(Err.args, system="INIT ERROR")
    finally:
        MysqlPool.resume_idle_connection(thread_data.connection)

# 初始化设备分类
def reflesh_equiptype():
    """ 初始化设备节点列表 """
    query_sql = "SELECT * FROM Hardware_Type"
    equip_types = MysqlPool.query_data_db(query_sql)

    # 没有设备分类，初始化失败，退出
    if not equip_types:
        log.err('CommFunc:Init equip type failed,exit!')
        sys.exit(1)

    # 建立分类列表
    for e_type in equip_types:
        sys_config['equip_type'][e_type['ht_name']] = (e_type['ht_code_down'],e_type['ht_code_up'])

    return True

# 初始化设备列表
def reflesh_equipid():
    """ 初始化设备节点列表 """
    query_sql = "SELECT * FROM Hardware_Equip_V"
    data_set = MysqlPool.query_data_db(query_sql)

    # 没有设备节点，初始化失败，退出
    if not data_set:
        log.err('CommFunc:Init equip id failed,exit!')
        sys.exit(1)

    # 建立节点列表
    for data_set_unit in data_set:
        RedisExecute.redis_sadd(data_set_unit['ht_name'], [str(data_set_unit['he_num'])])

    return True