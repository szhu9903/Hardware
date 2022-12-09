#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：demo_funcs.py
@Author  ：szhu9903
@Date    ：2022/12/6 15:35 
'''

import struct
from twisted.python import log
from utils.mysql_db import MysqlPool

# 温湿度 数据更新
def demo_env_update_helper(message):
    de_equipcode = message['EQUIP_CODE']
    msg_body = message['MSG_BODY']

    # unpack env data
    temperature_int, temperature_decimal, humidity_int, humidity_decimal = struct.unpack('!4B', msg_body)
    de_temperature = float(f'{temperature_int}.{temperature_decimal}')
    de_humidity = float(f'{humidity_int}.{humidity_decimal}')

    log.msg(f"{de_equipcode} ENV ({de_temperature},{de_humidity})", system="REQ")

    # save env data
    save_env_sql = """
    insert into Demo_Env(de_equipcode, de_temperature, de_humidity)
    values(%(de_equipcode)s, %(de_temperature)s,%(de_humidity)s)
    on duplicate key
    update de_equipcode=%(de_equipcode)s,de_temperature=%(de_temperature)s,de_humidity=%(de_humidity)s
    """
    save_env_data = {
        'de_equipcode': de_equipcode,
        'de_temperature': de_temperature,
        'de_humidity': de_humidity,
    }
    MysqlPool.insert_data_db(save_env_sql, save_env_data)



