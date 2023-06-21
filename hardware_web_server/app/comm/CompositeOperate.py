from flask import g
from app.module_config import table_module_map
from app.unit_config import depth_data_map, add_user_col, depth_post_map
from .GeneralOperate import GeneralOperate
from .SqlExecute import SqlExecute

class CompositeOperate(GeneralOperate):

    def __init__(self, module):
        super(CompositeOperate, self).__init__(module)

    def check_get_permissions(self):
        pass

    def check_operation_permissions(self):
        user = g.flask_httpauth_user
        # 无用户登录信息，不能进行操作
        if not user:
            g.is_continue_exec = False
            g.result["message"] = "未登录！"
            g.result["status"] = 403
            return
        if g.view_args['config_name'] not in user.get(2, []):
            g.is_continue_exec = False
            g.result["message"] = "无权操作！"
            g.result["status"] = 403
            return

    def get_link_module_data(self, module, row_data):
        module_name = module['tab_name']
        main_col, fk_col = module['link_column'].split(':')
        sql_query = table_module_map[module_name].sql_query_default
        sql_query = f'{sql_query} where {fk_col}=%s'
        if row_data[main_col] is None:
            return None
        sub_datas = SqlExecute.query_sql_data(sql_query, (row_data[main_col]))
        if not g.is_continue_exec:
            return None
        if module.get("sub_tab"):
            result_datas = []
            for sub_data in sub_datas:
                sub_sub_data = self.get_link_module_data(module.get("sub_tab"), sub_data)
                if sub_sub_data: result_datas.append(sub_sub_data[0])
            return result_datas if result_datas else None
        else:
            return sub_datas if sub_datas else None

    def deal_get_data(self):
        super(CompositeOperate, self).deal_get_data()
        depth_col = g.args_data.get('depth_col')
        depth_col_list = depth_col.split(',') if depth_col and depth_col.strip() else []
        result_data = g.result.get('data')
        # 数据集遍历
        for row_data in result_data:
            # url sub参数遍历
            for col_name in depth_col_list:
                if col_name not in depth_data_map:
                    continue
                # 存在下级数据配置，分开处理外键关联，和1对多或多对多
                sub_data = self.get_link_module_data(depth_data_map[col_name], row_data)
                row_data[col_name] = sub_data

    # 提交检查前是否补充提交所需用户数据，通过登录用户获取
    def check_column_data(self):
        config_name = g.view_args.get('config_name')
        if config_name in add_user_col:
            g.json_data['data'][add_user_col[config_name]] = g.flask_httpauth_user.get('id')
        super(CompositeOperate, self).check_column_data()

    # 提交操作，检查是够有要组合提交的数据
    def transact_post_after(self, cursor):
        insert_data = g.json_data['data']
        main_id = g.result.get('rowid', None)
        # 未获取到主表插入后的ID
        if main_id is None: return
        for col_name, col_value in insert_data.items():
            if (col_name not in depth_post_map) or not isinstance(col_value, list):
                continue
            module_name = depth_post_map[col_name]['tab_name']
            _, fk_col = depth_post_map[col_name]['link_column'].split(':')
            for depth_data in col_value:
                depth_data[fk_col] = main_id
                # 获取插入语句
                sql_insert = table_module_map[module_name].get_insert_sql(depth_data)
                cursor.transact_commit_sql_data(sql_insert, depth_data)

    # 更新操作，检查是够有要组合更新的数据
    def transact_put_after(self, cursor):
        record_id = g.view_args['record_id']
        update_data = g.json_data['data']
        for col_name, col_value in update_data.items():
            if (col_name not in depth_post_map) or (not isinstance(col_value, list)):
                continue
            module_name = depth_post_map[col_name]['tab_name']
            _, fk_col = depth_post_map[col_name]['link_column'].split(':')
            # 清空关联数据，重新写入
            sql_delete = f"{table_module_map[module_name].sql_delete_default} and {fk_col}=%s"
            cursor.transact_commit_sql_data(sql_delete, (record_id,))
            for depth_data in col_value:
                depth_data[fk_col] = record_id
                # 获取插入语句
                sql_insert = table_module_map[module_name].get_insert_sql(depth_data)
                cursor.transact_commit_sql_data(sql_insert, depth_data)












