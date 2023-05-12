#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：hardware_web_server 
@File    ：Full103Controller.py
@Author  ：szhu9903
@Date    ：2023/5/12 16:41 
'''

from flask import g
from app.comm.CompositeOperate import CompositeOperate
from app.comm.SqlExecute import SqlExecute
from app.comm.FlaskRabbitMQ import FlaskRabbitMQ
from app.unit_config import event_meta

class Full103RelayController(CompositeOperate):

    query_relay_sql = """
    select id, fr_equipid, fr_equipcode, fr_switch, fr_controlmode
    from Full103_Relay where id=%s
    """

    def __init__(self, module):
        super(Full103RelayController, self).__init__(module)

    # 修改
    def after_deal_put(self):
        relay_data = SqlExecute.query_sql_data(self.query_relay_sql, (g.view_args['record_id'],))
        message_data = {
            'relay_switch': relay_data[0]['fr_switch']
        }
        FlaskRabbitMQ.send_to_equip(relay_data[0]['fr_equipcode'],
                                    event_meta['FULL103_RELAY_SWITCH_SET_REQ']['EVENT'],
                                    message_data)

