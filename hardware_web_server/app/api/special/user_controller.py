import time
import logging
from app.api.special import special
from flask import current_app, request, g, jsonify
from app.comm.RedisExecute import RedisExecute
from app.comm.User import User

logger = logging.getLogger('app')

# 用户登陆
@special.route('/login/', methods=['POST'])
def user_login():
    try:
        req_data = request.json
        username = req_data['data'].get('user_name')
        password = req_data['data'].get('user_pwd')
        if not (username and password):
            g.result['status'] = 401.1
            g.result['message'] = '请求数据不完善'
            return jsonify(g.result)
        # 查询用户是否存在
        user = User()
        user_name = user.get_user_message(username)
        # 验证用户密码
        if not (user_name and user.verify_password(password)):
            g.result['status'] = 401.1
            g.result['message'] = '请检查用户名、密码！'
            return jsonify(g.result)
        # 生成验证Token和刷新Token
        access_token= user.generate_auth_token(user.id, current_app.config['ACCESS_TOKEN_TIME'])
        refresh_token = user.generate_auth_token(user.id, current_app.config['REFRESH_TOKEN_TIME'])
        token_data = {'access_token': str(access_token, encoding='utf-8'),
                      'refresh_token': str(refresh_token, encoding='utf-8'),
                      'token_time': time.time() + current_app.config['ACCESS_TOKEN_TIME'],
                      'user_info': user.user_non_sensitive}
        # 验证Token存入Redis，用于服务端控制Token,等
        RedisExecute.redis_set(user.id, token_data['refresh_token'], current_app.config['REFRESH_TOKEN_TIME'])
        g.result['message'] = '登录成功!'
        g.result['data'] = token_data
    except Exception as Err:
        logger.exception('服务器发生错误！%s' % Err)
        g.result['status'] = 500
        g.result['message'] = f'登录失败：{Err}'
    return jsonify(g.result)

# 验证token失效，刷新Token
@special.route('/update/tokens', methods=['POST'])
def update_tokens():
    try:
        req_data = request.json
        refresh_token = req_data['data'].get('refresh_token')
        if not (refresh_token):
            g.result['message'] = '请求数据不完善'
            return jsonify(g.result)
        # 解析Token
        token_json = User.verify_token(refresh_token)
        if token_json is None:
            g.result['status'] = 401
            g.result['message'] = '刷新Token失效!'
            return jsonify(g.result)
        if token_json.get('id'):
            # 去redis验证刷新Token白名单
            redis_refresh_token = RedisExecute.redis_get(token_json['id'])
            if redis_refresh_token and refresh_token == str(redis_refresh_token, encoding='utf-8'):
                # 生成验证Token和刷新Token
                access_token = User.generate_auth_token(token_json['id'], current_app.config['ACCESS_TOKEN_TIME'])
                token_data = {'access_token': str(access_token, encoding='utf-8'),
                              'token_time': time.time() + current_app.config['ACCESS_TOKEN_TIME']}
                g.result['message'] = '刷新Token成功!'
                g.result['data'] = token_data
                return jsonify(g.result)
        g.result['status'] = 401
        g.result['message'] = 'refresh token 失效'
    except Exception as Err:
        logger.exception('服务器发生错误！%s' % Err)
        g.result['message'] = f'登录失败：{Err}'
    return jsonify(g.result)

