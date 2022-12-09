#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：config.py
@Author  ：szhu9903
@Date    ：2022/11/17 14:17 
'''

import threading

# 线程会话变量,隔离数据库链接
thread_data = threading.local()

# 系统变量
sys_config = {
    'protocols': {}, # 链接中的节点
    'last_stamp': None, # 服务起始时间
    'equip_type': {},
}

# 响应消息保存时间
REDIS_ACK_SAVE_TIME = 30

# mysql 连接
class MysqlConf():
    host     = 'xx.xx.xx.xx'
    user     = 'root'
    password = 'xx'
    port     = 3306
    db_name  = 'myhardware'

# rabbitmq 连接
class RabbitConf():
    username     = 'admin'
    password     = 'xxx'
    host         = 'xx.xx.xx.xx'
    port         =  5672
    virtual_host = 'my_vhost'

# redis 连接
class RedisConf():
    host         = 'xx.xx.xx.xx'
    port         = 6379
    password     = 'xx'
    db           = 6

