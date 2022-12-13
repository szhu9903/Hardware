#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：blog_server 
@File    ：UserController.py
@Author  ：szhu9903
@Date    ：2022/11/25 08:48 
'''

from flask import g
from app.comm.CompositeOperate import CompositeOperate
from app.comm.User import User

class UserController(CompositeOperate):

    def __init__(self, module):
        super(UserController, self).__init__(module)

    def check_get_permissions(self):
        user = g.flask_httpauth_user
        # 无用户登录信息，不能进行查询
        if not user:
            g.is_continue_exec = False
            g.result["message"] = "未登录！"
            g.result["status"] = 403
            g.result["code"] = 0x13
            return

        if g.view_args['config_name'] not in user.get(2, []):
            g.is_continue_exec = False
            g.result["message"] = "无权查询！"
            g.result["status"] = 403
            g.result["code"] = 0x14
            return

    # 提交新用户 加密密码
    def before_deal_post(self):
        su_pwd = g.json_data["data"].get('su_pwd') or None
        if su_pwd:
            g.json_data["data"]['su_pwd'] = User.generate_password(su_pwd)

    # 修改用户 加密密码
    def before_deal_put(self):
        g.json_data["data"].pop('su_pwd')

