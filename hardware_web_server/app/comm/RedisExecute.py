from redis import Redis
from flask import current_app


class RedisExecute(object):

    @staticmethod
    def redis_set(name, value, ex=None):
        redis = Redis(connection_pool=current_app.config['EQUIP_REDIS_POOL'])
        return redis.set(name, value, ex)

    @staticmethod
    def redis_get(name):
        redis = Redis(connection_pool=current_app.config['EQUIP_REDIS_POOL'])
        return redis.get(name)

    @classmethod
    def redis_cmd_ack_getdel(cls, ack_eventid, equip_code):
        redis = Redis(connection_pool=current_app.config['EQUIP_REDIS_POOL'])
        key_name = f'{ack_eventid}-{equip_code}'
        return redis.getdel(key_name)
