from flask import g, request, jsonify
from functools import wraps
from app.comm.User import User


# 如果用户登录获取用户信息(包含权限信息)， 未登录用户None
def auth_user(func):
    @wraps(func)
    def get_user(*args, **kwargs):
        g.flask_httpauth_user = None
        # 获取token
        if request.headers.get('Authorization'):
            user_token = request.headers.get('Authorization').split(' ')[1]
            # 获取用户
            token_json = User.verify_token(user_token)
            if token_json and token_json.get('id'):
                user = User.user_info(token_json['id'])
                g.flask_httpauth_user = user
        return func(*args, **kwargs)
    return get_user

# 如果用户登录获取用户信息(包含权限信息)， 未登录用户None
def ws_auth_user(func):
    @wraps(func)
    def get_user(*args, **kwargs):
        g.flask_httpauth_user = None
        # 获取token
        user_token = request.args.get('token') or None
        if not user_token:
            return None
        user_token = request.args['token']
        # 获取用户
        token_json = User.verify_token(user_token)
        if token_json and token_json.get('id'):
            user = User.user_info(token_json['id'])
            g.flask_httpauth_user = user
        else:
            return None
        return func(*args, **kwargs)
    return get_user

#
# auth = HTTPTokenAuth(scheme='Token')
#
# @auth.verify_token
# def verify_token(token):
#     serializer_key = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         token_json = serializer_key.loads(token)
#     except Exception as Err:
#         return False
#     if token_json.get('id'):
#         user = User.user_info(token_json['id'])
#         # 在此处可扩展复杂权限，获取数据库配置权限，不通过直接 False 或 None
#         return user  # 返回数据装饰器会自动将用户数据绑定到g.flask_httpauth_user
#     return False
#
# # 权限验证失败
# @auth.error_handler
# def token_auth_error(*args, **kwargs):
#     # return error_response("ERR", message="Token验证失败", code=401)
#     return error_response("ERR", message="Token验证失败", code=401)


