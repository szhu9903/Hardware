#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：RedisExecute.py
@Author  ：szhu9903
@Date    ：2022/12/5 16:38 
'''

from typing import List
from redis import Redis, ConnectionPool
from config import RedisConf, REDIS_ACK_SAVE_TIME


class RedisExecute(object):

    __connection_pool = None

    def __init__(self):
        self.create_connection_poll()

    def create_connection_poll(self):
        RedisExecute.__connection_pool = ConnectionPool(
            max_connections=10,
            host=RedisConf.host,
            port=RedisConf.port,
            password=RedisConf.password,
            db=RedisConf.db)

    # string
    @classmethod
    def redis_set(cls, name, value, ex=None):
        redis = Redis(connection_pool=cls.__connection_pool)
        return redis.set(name, value, ex)

    @classmethod
    def redis_get(cls, name):
        redis = Redis(connection_pool=cls.__connection_pool)
        return redis.get(name)

    @classmethod
    def redis_cmd_ack_set(cls, ack_eventid, equip_code, value='OK'):
        redis = Redis(connection_pool=cls.__connection_pool)
        key_name = f'{ack_eventid}-{equip_code}'
        return redis.set(key_name, value, REDIS_ACK_SAVE_TIME)

    @classmethod
    def redis_cmd_ack_getdel(cls, ack_eventid, equip_code):
        redis = Redis(connection_pool=cls.__connection_pool)
        key_name = f'{ack_eventid}-{equip_code}'
        return redis.getdel(key_name)

    # Set
    @classmethod
    def redis_sadd(cls, name, values:List):
        redis = Redis(connection_pool=cls.__connection_pool)
        return redis.sadd(name, *values)

    @classmethod
    def redis_smembers(cls, name):
        redis = Redis(connection_pool=cls.__connection_pool)
        return redis.smembers(name)

    @classmethod
    def redis_sismember(cls, name, values):
        redis = Redis(connection_pool=cls.__connection_pool)
        return redis.sismember(name, values)
