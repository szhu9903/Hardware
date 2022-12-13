import os
import pymysql
from redis import ConnectionPool
# dbutils 2.x 版本写法
from dbutils.pooled_db import PooledDB

# 公共环境
class BaseConfig(object):
    ACCESS_TOKEN_TIME = 3600 # 验证TOKEN时效
    REFRESH_TOKEN_TIME = 3600 * 24 * 15 # 刷新TOKEN时效

    # 路径配置
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    mysql_config = dict()
    equip_redis = dict()
    RABBITMQ_CONFIG = dict()

    def __init__(self, pytest_config):
        if pytest_config is not None:
            self.mysql_config['mysql_host'] = pytest_config.get('db_host', None)
            self.mysql_config['mysql_password'] = pytest_config.get('db_pwd', None)

            self.equip_redis['redis_host'] = pytest_config.get('db_host', None)
            self.equip_redis['redis_password'] = pytest_config.get('db_pwd', None)

            self.SECRET_KEY = pytest_config.get('secret_key', None)

    @property
    def PYMYSQL_POOL(self):
        return self.init_mysql(self.mysql_config)

    @property
    def EQUIP_REDIS_POOL(self):
        return self.init_redis(self.equip_redis)


    # 初始化 mysql连接
    @staticmethod
    def init_mysql(conn_message):
        PYMYSQL_POOL = PooledDB(
            creator = pymysql,
            maxconnections = 10,  # 连接池最大连接数
            mincached = 3,  # 初始化最创建空闲小连接数
            maxcached = 5,  # 最大空闲连接数
            maxshared = 5,  # 最大空闲连接数，无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，永远共享
            blocking = True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage = None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession = [],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping = 0,  # ping MySQL服务端，检查是否服务可用。0：从不,1：从池中获取时,2 创建游标时,4 执行一个查询时,7和所有其他的组合这些值)
            # 以下参数传递给数据库连接模块 pymysql
            host = conn_message["mysql_host"],
            port = 3306,
            user = conn_message["mysql_user"],
            password = conn_message["mysql_password"],
            db = conn_message["mysql_db"],
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )
        return PYMYSQL_POOL

    # 初始化 redis连接
    @staticmethod
    def init_redis(conn_message):
        TOKEN_REDIS_POOL = ConnectionPool(
            max_connections=100,
            host=conn_message["redis_host"],
            port=6379,
            password=conn_message["redis_password"],
            db=conn_message["redis_db"])
        return TOKEN_REDIS_POOL

# 生产环境
class RunConfig(BaseConfig):
    SECRET_KEY = ""
    DEBUG = False
    mysql_config = {
        "mysql_host": "xx.xx.xx.xx",
        "mysql_user": "root",
        "mysql_password": "xxx",
        "mysql_db": "myhardware",
    }
    equip_redis = {
        "redis_host": "xx.xx.xx.xx",
        "redis_password": "xxx",
        "redis_db": 6,
    }
    RABBITMQ_CONFIG = {
        "rabbitmq_host": "xx.xx.xx.xx",
        "rabbitmq_port": 5672,
        "rabbitmq_virtual_host": "my_vhost",
        "rabbitmq_username": "xxx",
        "rabbitmq_password": "xxx",
    }

# 测试环境
class TestConfig(BaseConfig):
    DEBUG = False
    mysql_config = {
        "mysql_host": "",
        "mysql_user": "root",
        "mysql_password": "",
        "mysql_db": "myhardware_test",
    }
    equip_redis = {
        "redis_host": "",
        "redis_password": "",
        "redis_db": 6,
    }
    rabbitmq_config = {
        "rabbitmq_host": "localhost",
        "rabbitmq_port": 5672,
        "rabbitmq_virtual_host": "my_vhost",
        "rabbitmq_username": "xxx",
        "rabbitmq_password": "xxx",
    }

# case
config_map = {
    "run": RunConfig,
    "test": TestConfig,
}
