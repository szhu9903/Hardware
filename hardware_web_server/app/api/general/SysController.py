#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：hardware_web_server 
@File    ：SysController.py
@Author  ：szhu9903
@Date    ：2023/2/28 15:57 
'''

from flask import g
from app.comm.CompositeOperate import CompositeOperate
from app.comm.SqlExecute import SqlExecute
from app.comm.FlaskRabbitMQ import FlaskRabbitMQ
from app.unit_config import event_meta, config_map

class ConfigVarController(CompositeOperate):
    query_config_sql = """
    select b.*,c.ht_name from
    Hardware_ConfigVar a
    left join Hardware_ConfigVar b on IFNULL(a.hcv_type, 0)=IFNULL(b.hcv_type, 0)
    left join Hardware_Type c on c.id = a.hcv_type
    where a.id=%s
    """

    def __init__(self, module):
        super(ConfigVarController, self).__init__(module)

    # 修改环境数据
    def after_deal_put(self):
        config_data = SqlExecute.query_sql_data(self.query_config_sql, (g.view_args['record_id'],))
        message_data = {config['hcv_variablekey']:config['hcv_variablevalue'] for config in config_data}
        if config_data[0]['hcv_type']:
            event_name = config_map[config_data[0]['hcv_type']]
            FlaskRabbitMQ.send_to_type_equip(config_data[0]['ht_name'],
                                        event_meta[event_name]['EVENT'],
                                        message_data)

        else:
            FlaskRabbitMQ.send_to_all_equip(event_meta['COMM_HEARTBEAT_INTER_REQ']['EVENT'], message_data)

