import logging
from flask import current_app
from flask import g

logger = logging.getLogger('app')

class SqlExecute(object):
    def __init__(self):
        self.open_conn()

    # 创建连接
    def open_conn(self):
        # 获取连接
        pool = current_app.config['PYMYSQL_POOL']
        self.conn = pool.connection()
        # 创建游标
        self.cursor = self.conn.cursor()

    # 事务执行中
    def transact_commit_sql_data(self, sql, args=None):
        result = None
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.lastrowid
        except Exception as Err:
            g.is_continue_exec = False
            g.result['code'] = 0x21
            g.result["message"] = f"sql execute error: {str(Err)}"
            self.conn.rollback()
            self.cursor.close()
            self.conn.close()
            raise Exception('sql execute err : %s' % Err)
        return result

    # 事务提交
    def commit(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


    @staticmethod
    # 获取数据集
    def query_sql_data(sql, args=None):
        result = None
        # 获取连接
        pool = current_app.config['PYMYSQL_POOL']
        conn = pool.connection()
        # 创建游标
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchall()
        except Exception as Err:
            g.is_continue_exec = False
            g.result['code'] = 0x21
            g.result["message"] = f"sql execute error: {str(Err)}"
            logger.exception('sql execute err : %s' % Err)
            raise Exception(Err)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    # 无事务提交
    def commit_sql_data(sql, args=None):
        result = None
        # 获取连接
        pool = current_app.config['PYMYSQL_POOL']
        conn = pool.connection()
        # 创建游标
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            result = cursor.lastrowid
        except Exception as Err:
            g.is_continue_exec = False
            g.result['code'] = 0x21
            g.result["message"] = f"sql execute error: {str(Err)}"
            conn.rollback()
            logger.exception('sql execute err : %s' % Err)
        else:
            conn.commit()
        finally:
            cursor.close()
            conn.close()
            return result
