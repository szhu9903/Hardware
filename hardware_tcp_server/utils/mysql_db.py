import threading
import pymysql
import traceback
from collections import deque
from twisted.python import log
from config import thread_data, MysqlConf

class MysqlPool():
    """
    mysql 连接池
    """
    __connection_pool = deque(maxlen=10)
    pool_mutex = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """初始化数据库连接队列"""
        for i in range(10):
            connection = pymysql.connect(host=MysqlConf.host,
                                         user=MysqlConf.user,
                                         password=MysqlConf.password,
                                         port=MysqlConf.port,
                                         db=MysqlConf.db_name,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            connection.autocommit(True)
            cls.__connection_pool.append(connection)
        super(MysqlPool, cls).__new__(cls)

    @classmethod
    def get_idle_connection(cls):
        """ 获取空闲连接 """
        idle_connection = None
        try:
            cls.pool_mutex.acquire()
            idle_connection = cls.__connection_pool.pop()
            cls.pool_mutex.release()
        except Exception as Err:
            cls.pool_mutex.release()
            log.err('err:', str(Err))
        return idle_connection

    @classmethod
    def resume_idle_connection(cls, used_connection):
        """ 返回空闲连接 """
        try:
            cls.pool_mutex.acquire()
            cls.__connection_pool.appendleft(used_connection)
            cls.pool_mutex.release()
        except Exception as Err:
            cls.pool_mutex.release()
            log.err('release err:', str(Err))

    @staticmethod
    def insert_data_db(insert_sql, params=None):
        """插入数据库"""
        result = False
        last_id = 0
        for tries_times in range(3):
            cursor = thread_data.connection.cursor()
            try:
                cursor.execute(insert_sql, params)
                last_id = cursor.lastrowid
                result = True
                break
            except Exception as Err:
                thread_data.connection.ping(reconnect=True)
                if tries_times == 2:
                    log.err('CommFunc:Error in DB Execute(%s):%s' % (insert_sql, str(Err)))
                    traceback.print_exc()
            finally:
                cursor.close()
        return result, last_id

    @staticmethod
    def query_data_db(query_sql, params=None):
        """ 查询数据库数据集 """
        data_set = None
        for tries_times in range(3):
            cursor = thread_data.connection.cursor()
            try:
                cursor.execute(query_sql, params)
                data_set = cursor.fetchall()
                break
            except Exception as Err:
                thread_data.connection.ping(reconnect=True)
                if tries_times == 2:
                    log.err('CommFunc:Error in DB Execute(%s):%s' % (query_sql, str(Err)))
                    traceback.print_exc()
            finally:
                cursor.close()
        return data_set

