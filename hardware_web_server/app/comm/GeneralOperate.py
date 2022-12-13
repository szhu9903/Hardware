import copy
from flask import g
from app.comm.TableModule import TableModule
from app.comm.SqlExecute import SqlExecute
from app.unit_config import default_result, default_limit_size, depth_post_map

class GeneralOperate(object):
    def __init__(self, module:TableModule):
        self.module = module
        # 请求参数检查链
        self.get_deal_func_link = []
        self.post_deal_func_link = []
        self.put_deal_func_link = []
        self.delete_deal_func_link = []
        self.init_check_func_link()

    # 初始化请求处理链
    def init_check_func_link(self):
        self.get_deal_func_link.extend([
            self.check_get_permissions,
            self.check_view_param,
            self.check_pagination_param,
            self.before_deal_get,
            self.deal_get_data,
            self.after_deal_get,

        ])
        self.post_deal_func_link.extend([
            self.check_operation_permissions,
            self.check_request_data,
            self.check_column_data,
            self.before_deal_post,
            self.deal_post_data,
            self.after_deal_post,
        ])
        self.put_deal_func_link.extend([
            self.check_operation_permissions,
            self.check_request_data,
            self.check_unique_record,
            self.check_column_data,
            self.before_deal_put,
            self.deal_put_data,
            self.after_deal_put,
        ])
        self.delete_deal_func_link.extend([
            self.check_operation_permissions,
            self.check_unique_record,
            self.before_deal_delete,
            self.deal_delete_data,
            self.after_deal_delete,
        ])

    # 通用 - 初始化请求参数解析
    def init_general_data(self, request):
        g.args_data = request.args.to_dict() # url参数
        g.is_continue_exec = True # 检查链执行结果
        if request.method in ["POST", "PUT"]:
            g.json_data = request.json
        g.view_args = request.view_args # 动态url路径参数

    # 处理GET请求
    def deal_get_method(self, request):
        # 初始化参数
        self.init_general_data(request)
        # 执行处理函数链
        for deal_func in self.get_deal_func_link:
            deal_func()
            # 出现异常退出检查链
            if not g.is_continue_exec:
                break
        return g.result

    # 处理GET请求 -> 检查权限
    def check_get_permissions(self):
        return

    # 处理GET请求 -> 检查视图参数
    def check_view_param(self):
        view = g.args_data.get("view")
        if view:
            if (not self.module.view_list) or (view not in self.module.view_list):
                g.is_continue_exec = False
                g.result['message'] = f"view({view}):视图不存在！ "

    # 处理GET请求 -> 检查分页参数
    def check_pagination_param(self):
        pagination = g.args_data.get("pagination")
        if pagination:
            page_index, page_size = pagination.split(',')
            if (not page_index.isdigit()) and (not page_size.isdigit()):
                g.is_continue_exec = False
                g.result['message'] = f"pagination({pagination}):分页数据错误，参考格式:index,size！ "

    # 处理GET请求 -> 执行get获取数据前操作
    def before_deal_get(self):
        return

    # 处理GET请求 -> 执行get获取数据
    def deal_get_data(self):
        # 获取总数
        self.filter_str, self.filter_args = self.get_filter_str()
        total_count = self.query_total_count()
        if not g.is_continue_exec:
            g.result['message'] = '获取数据量失败！'
            return
        g.result['total_count'] = total_count
        # 获取查询结果集
        data = self.query_data()
        if not g.is_continue_exec:
            g.result['message'] = '获取结果集失败！'
            return
        g.result['data'] = data

    # 处理GET请求 -> 执行get获取数据 -> 查询数据总量
    def query_total_count(self):
        view = g.args_data.get('view')
        if view:
            count_query = self.module.views_query[view]['sql_query_count']
        else:
            count_query = self.module.sql_count_default
        count_query = f'{count_query} {self.filter_str}'
        total_count = SqlExecute.query_sql_data(count_query, self.filter_args)
        return total_count[0]['total_count'] if g.is_continue_exec else None

    # 处理GET请求 -> 执行get获取数据 -> 获取数据集
    def query_data(self):
        default_sql = self.get_default_sql()
        order_str = self.get_order_str()
        pagination_str = self.get_pagination_str()
        sql_default_query = f'{default_sql} {self.filter_str} {order_str} {pagination_str}'
        # 获取数据集
        data = SqlExecute.query_sql_data(sql_default_query, self.filter_args)
        return data if g.is_continue_exec else None

    # 处理GET请求 -> 执行get获取数据 -> 获取数据集 -> 获取默认查询语句
    def get_default_sql(self):
        view = g.args_data.get('view')
        if view:
            sql_query = self.module.views_query[view]['sql_query']
        else:
            sql_query = self.module.sql_query_default
        return sql_query

    # 处理GET请求 -> 执行get获取数据 -> 获取数据集 -> 获取过滤条件str 和 参数
    def get_filter_str(self):
        record_id = g.view_args.get('record_id')
        filter_param = g.args_data.get('filter')
        fuzzy_filter_param = g.args_data.get('fuzzyfilter')
        filter_str = "where 1=1 "
        filter_args = dict()
        # 获取详细数据
        if record_id:
            filter_str += "and id=%(id)s "
            filter_args['id'] = record_id
            return (filter_str, filter_args)
        # 模糊条件
        if fuzzy_filter_param:
            fuzzy_filter_list = fuzzy_filter_param.split(',')
            for fuzzy_filter in fuzzy_filter_list:
                fuzzy_key, fuzzy_val = fuzzy_filter.split('=')
                filter_str += f"and ({fuzzy_key} like %({fuzzy_key})s) "
                filter_args[fuzzy_key] = f"%{fuzzy_val}%"
        # 精准条件查询
        if filter_param:
            filter_args_list = filter_param.split(',')
            for filter in filter_args_list:
                filter_key, filter_val = filter.split('=')
                if filter_key in filter_args.keys(): continue
                filter_str += f"and ({filter_key}=%({filter_key})s) "
                filter_args[filter_key] = filter_val
        return (filter_str, filter_args)

    # 处理GET请求 -> 执行get获取数据 -> 获取数据集 -> 获取排序str
    def get_order_str(self):
        # 排序条件
        order_param = g.args_data.get('order')
        order_str = ""
        if order_param:
            order_str = order_param.replace('|', ',')
            order_str = 'order by %s' % (order_str)
        return order_str

    # 处理GET请求 -> 执行get获取数据 -> 获取数据集 -> 获取分页参数str
    def get_pagination_str(self):
        # 获取分页语句
        pagination_param = g.args_data.get('pagination')
        pagination_str = ""
        if pagination_param:
            page_index, page_size = pagination_param.split(',')
            page_index = 1 if int(page_index) < 1 else int(page_index)
            page_size = 1 if int(page_size) < 1 else int(page_size)
            pagination_str = 'limit %d, %d' % ((page_index - 1) * page_size, page_size)
        return pagination_str if pagination_str else f"limit {default_limit_size}"

    # 处理GET请求 -> get获取数据后处理
    def after_deal_get(self):
        return

    # 处理POST请求
    def deal_post_method(self, request):
        # 初始化参数
        self.init_general_data(request)
        # 执行链
        for deal_func in self.post_deal_func_link:
            deal_func()
            # 出现异常退出检查链
            if not g.is_continue_exec:
                break
        return g.result

    # [POST、PUT、DELETE] 操作权限检查
    def check_operation_permissions(self):
        return

    # [POST、PUT]检查请求提交数据结构体
    def check_request_data(self):
        if not g.json_data:
            g.is_continue_exec = False
            g.result["message"] = '无要提交的数据～'
        if 'data' not in g.json_data.keys():
            g.is_continue_exec = False
            g.result["message"] = '参数不完整：缺少data参数～'

    # [POST、PUT]检查有效数据列合法性，清除无效数据
    def check_column_data(self):
        req_data = g.json_data["data"]
        table_column = self.module.colnames
        req_data_keys = list(req_data.keys())
        for data_key in req_data_keys:
            if (req_data[data_key] is None) or (len(str(req_data[data_key])) == 0):
                del req_data[data_key]
                continue
            if (data_key not in table_column) and (data_key not in depth_post_map):
                g.is_continue_exec = False
                g.result['code'] = 0x11
                g.result["message"] = f'非法列名：{data_key}～'

    # POST 提交数据前操作
    def before_deal_post(self):
        return

    # POST 提交数据
    def deal_post_data(self):
        sqlExecute = SqlExecute()
        self.transact_post_before(sqlExecute)
        if not g.is_continue_exec:
            return
        self.transact_post(sqlExecute)
        if not g.is_continue_exec:
            return
        self.transact_post_after(sqlExecute)
        if not g.is_continue_exec:
            return
        sqlExecute.commit()

    # 插入数据前事务
    def transact_post_before(self, cursor):
        return

    # 插入post数据
    def transact_post(self, cursor):
        insert_data = g.json_data['data'].copy()
        if g.json_data.get("type", None) == "replace":
            sql_insert = self.module.get_insert_sql(insert_data, is_replace=True)
        else:
            sql_insert = self.module.get_insert_sql(insert_data)
        insert_data_keys = list(insert_data.keys())
        for col_name in insert_data_keys:
            if col_name in depth_post_map: del insert_data[col_name]
        rowid = cursor.transact_commit_sql_data(sql_insert, insert_data)
        g.result['rowid'] = rowid

    # 插入数据后事务
    def transact_post_after(self, cursor):
        return

    # POST 提交后操作
    def after_deal_post(self):
        return

    # 处理PUT请求
    def deal_put_method(self, request):
        # 初始化参数
        self.init_general_data(request)
        # 执行链
        for deal_func in self.put_deal_func_link:
            deal_func()
            # 出现异常退出检查链
            if not g.is_continue_exec:
                break
        return g.result

    # [PUT、DELETE] 修改删除记录前，检查记录唯一性
    def check_unique_record(self):
        record = g.view_args['record_id']
        query_sql = f" {self.module.sql_query_default} where id={record}"
        data = SqlExecute.query_sql_data(query_sql)
        if not g.is_continue_exec:
            return
        if len(data) == 0:
            g.is_continue_exec = False
            g.result["message"] = "未匹配到要操作的数据"
            return

    # PUT 提交数据前操作
    def before_deal_put(self):
        return

    # PUT 提交数据
    def deal_put_data(self):
        sqlExecute = SqlExecute()
        self.transact_put_before(sqlExecute)
        if not g.is_continue_exec:
            return
        self.transact_put(sqlExecute)
        if not g.is_continue_exec:
            return
        self.transact_put_after(sqlExecute)
        if not g.is_continue_exec:
            return
        sqlExecute.commit()

    # put 事务中提交前
    def transact_put_before(self, cursor):
        pass

    # put 事务提交
    def transact_put(self, cursor):
        record_id = g.view_args['record_id']
        update_data = g.json_data['data'].copy()
        sql_update = self.module.get_update_sql(update_data, record_id)
        insert_data_keys = list(update_data.keys())
        for col_name in insert_data_keys:
            if col_name in depth_post_map: del update_data[col_name]
        cursor.transact_commit_sql_data(sql_update, update_data)
        if not g.is_continue_exec:
            return
        g.result['rowid'] = record_id

    # put 事务中提交后
    def transact_put_after(self, cursor):
        pass

    # PUT 提交后操作
    def after_deal_put(self):
        return

    # 处理DELETE请求
    def deal_delete_method(self, request):
        # 初始化参数
        self.init_general_data(request)
        # 执行链
        for deal_func in self.delete_deal_func_link:
            deal_func()
            # 出现异常退出检查链
            if not g.is_continue_exec:
                break
        return g.result

    # DELETE 删除数据前操作
    def before_deal_delete(self):
        return

    # DELETE 删除数据
    def deal_delete_data(self):
        record_id = g.view_args['record_id']
        sql_delete = self.module.get_delete_sql(record_id)
        SqlExecute.commit_sql_data(sql_delete)
        if not g.is_continue_exec:
            return
        g.result['rowid'] = record_id

    # DELETE 删除后操作
    def after_deal_delete(self):
        return
