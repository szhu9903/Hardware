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
from app.comm.SqlExecute import SqlExecute
from app.comm.FlaskRabbitMQ import FlaskRabbitMQ
from app.unit_config import event_meta

class DemoLedController(CompositeOperate):

    query_led_sql = """
    select id, dl_equipid, dl_equipcode, dl_switch, dl_r, dl_g, dl_b 
    from Demo_Led where id=%s
    """

    def __init__(self, module):
        super(DemoLedController, self).__init__(module)

    # 修改LED配置
    def after_deal_put(self):
        led_data = SqlExecute.query_sql_data(self.query_led_sql, (g.view_args['record_id'],))
        message_data = {
            'led_switch': led_data[0]['dl_switch'],
            'led_r': led_data[0]['dl_r'],
            'led_g': led_data[0]['dl_g'],
            'led_b': led_data[0]['dl_b'],
        }
        FlaskRabbitMQ.send_to_equip(led_data[0]['dl_equipcode'],
                                    event_meta['DEMO_SET_LED_COLOR_REQ']['EVENT'],
                                    message_data)
