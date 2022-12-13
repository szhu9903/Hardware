import logging
from flask import current_app
from app.unit_config import depth_post_map

logger = logging.getLogger('app')

class TableModule():
    def __init__(self, table_name, view_list=list()):
        self.table_name = table_name
        self.view_list = view_list
        self.views_query = {}
        self.init_table_sql()
        self.init_view_sql()

    # 获取字段属性
    def get_col_info(self, table_name):
        colnames = []
        coltypes = []
        pool = current_app.config['PYMYSQL_POOL']
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute('select * from %s where id=0' % table_name)
        except Exception as Err:
            logger.exception('error to init %s:%s' % (self.table_name, str(Err)))
        else:
            cols = cursor.description
            for col in cols:
                colnames.append(col[0])
                coltypes.append(col[1])
        finally:
            cursor.close()
            conn.close()
        return colnames, coltypes

    # 初始化表属性
    def init_table_sql(self):
        self.colnames, self.coltypes = self.get_col_info(self.table_name)
        self.col_meta = dict(zip(self.colnames, self.coltypes))
        col_key = ','.join(self.colnames)
        col_val = '"%(' + ')s","%('.join(self.colnames) + ')s"'
        self.sql_query_default = "select %s from %s " % (col_key, self.table_name)
        self.sql_insert_default = "insert into %s (%s) VALUES (%s)" % (self.table_name, col_key, col_val)
        self.sql_delete_default = "delete from %s where 1=1 " %(self.table_name)
        self.sql_count_default = "select count(*) as total_count from %s" % (self.table_name)

    # 初始化视图属性
    def init_view_sql(self):
        # 构建视图dict
        for view_name in self.view_list:
            self.views_query[view_name] = {}
            # 获取视图列属性
            self.views_query[view_name]['col_names'], self.views_query[view_name]['col_types'] = self.get_col_info(view_name)
            self.views_query[view_name]['col_meta'] = dict(zip(self.views_query[view_name]['col_names'],
                                                         self.views_query[view_name]['col_types']))
            col_key = ','.join(self.views_query[view_name]['col_names'])
            # 视图查询语句
            self.views_query[view_name]['sql_query'] = 'select %s from %s ' % (col_key, view_name)
            self.views_query[view_name]['sql_query_count'] = 'select count(*) as total_count from %s' % view_name


    # 获取更新数据语句
    def get_update_sql(self, update_data, record_id):
        if "id" in update_data: del update_data["id"]
        update_data_keys = [col_name for col_name in update_data.keys() if col_name not in depth_post_map]
        # 生成更新语句
        col_data = ','.join(["%s=%%(%s)s" % (k, k) for k in update_data_keys])
        update_sql = "update %s set %s where id=%s" % (self.table_name, col_data, record_id)
        return update_sql

    # 获取提交数据sql
    def get_insert_sql(self, insert_data, is_replace=False):
        """
        :param insert_data: dict
        :param is_replace: replace true > insert update
        :return: sql str
        """
        if "id" in insert_data: del insert_data["id"]
        insert_data_keys = [col_name for col_name in insert_data.keys() if col_name not in depth_post_map]
        # 生成插入语句
        col_key = ','.join(insert_data_keys)
        col_val = "%(" + ")s,%(".join(insert_data_keys) + ")s"
        sql_insert = "insert into %s (%s) VALUES (%s)" % (self.table_name, col_key, col_val)
        if is_replace:
            update_str = ','.join([f"{key}=VALUES({key})" for key in insert_data_keys])
            sql_insert = f"{sql_insert} on duplicate key update {update_str}"
        logger.info(sql_insert)
        return sql_insert

    # 获取删除数据sql
    def get_delete_sql(self, record_id):
        delete_sql = "%s and id=%s" %(self.sql_delete_default, record_id)
        return delete_sql

