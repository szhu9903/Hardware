from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from app.comm.TableModule import TableModule
from app.comm.SqlExecute import SqlExecute


class User():
    def __init__(self):
        self.id = None
        self._password = None
        self.user_non_sensitive = {}

    # 用户名获取用户信息
    def get_user_message(self, zaccount):
        user_module = TableModule('sys_user')
        sql_query = f"{user_module.sql_query_default} where su_account=%s and su_delflag=0"
        user_message = SqlExecute.query_sql_data(sql_query, (zaccount))
        if user_message:
            self.id = user_message[0]['id']
            self._password = user_message[0]['su_pwd']
            self.user_non_sensitive = {
                "id": user_message[0]['id'],
                "su_username": user_message[0]['su_username'],
                "su_userphoto": user_message[0]['su_userphoto'],
                "su_isadmin": user_message[0]['su_isadmin'],
                }
            return True
        return False

    # 验证密码
    def verify_password(self, password):
        if self._password:
            return check_password_hash(self._password, password)
        return False

    # 生成密码
    @staticmethod
    def generate_password(password):
        if password:
            return generate_password_hash(password)
        return None

    # 生成token
    @staticmethod
    def generate_auth_token(user_id, long_time=600):
        user_token = Serializer(current_app.config['SECRET_KEY'], long_time)
        return user_token.dumps({'id':user_id})

    # 解析token
    @staticmethod
    def verify_token(token):
        serializer_key = Serializer(current_app.config['SECRET_KEY'])
        try:
            token_json = serializer_key.loads(token)
        except Exception as Err:
            token_json = None
        return token_json

    # 获取用户详细信息
    @staticmethod
    def user_info(id):
        sql_query = """
        select
            a.id,a.su_account,a.su_username,a.su_delflag,e.sp_type,
            group_concat(distinct e.sp_apipath) as sp_apipath
        from sys_user a
        left join ur_relation b on (a.id=b.ur_userid)
        left join sys_role c on (b.ur_roleid = c.id)
        left join rp_relation d on (c.id = d.rp_roleid)
        left join sys_purview e on (d.rp_purviewid = e.id)
        where a.id=%s
        group by e.sp_type
        """
        user_message = SqlExecute.query_sql_data(sql_query, (id))
        if user_message:
            user_data = user_message[0]
            user_data.update({user['sp_type']:user['sp_apipath'].split(',') for user in user_message if user['sp_type']})
            return user_data
        return None
