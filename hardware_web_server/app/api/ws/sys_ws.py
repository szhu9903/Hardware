#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：blog_server 
@File    ：demo_ws.py
@Author  ：szhu9903
@Date    ：2022/12/7 17:01 
'''

import logging
import json
from flask import request, g
from app.api.ws import ws
from app.utils.auth_utils import ws_auth_user
from .async_config import async_cmd_map

logger = logging.getLogger('app')

@ws.route("/asyncfunc/")
@ws_auth_user
def asyncmsg_func():
    web_socket = request.environ.get("wsgi.websocket")
    if not web_socket:
        return "only support ws connect!"

    while not web_socket.closed:
        ws_message = web_socket.receive()

        if not ws_message:
            break

        try:
            # 检查指令是否有效
            ws_message = json.loads(ws_message)
            if ws_message.get('event') not in async_cmd_map.keys():
                g.result['code'] = 0x52
                g.result['message'] = '下发指令无效！'
                web_socket.send(json.dumps(g.result))
                continue

            # 执行处理函数
            async_cmd_map[ws_message['event']]['func'](ws_message, web_socket)
        except Exception as Err:
            g.result['code'] = 0x52
            g.result['message'] = f'错误：{str(Err)}'
            web_socket.send(json.dumps(g.result))

    logger.info('close websocket(syncfunc)')
    return 'close websocket(syncfunc)'



