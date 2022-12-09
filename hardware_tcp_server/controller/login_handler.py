import json
import struct
from twisted.python import log
from comm.down_message import send_downstream_message
from utils.mysql_db import MysqlPool


update_equip_status = "UPDATE Hardware_Equip SET he_equipstatus='LINKED' WHERE he_num=%s"

#  设备登录
def default_equip_login(message, ack_event_hex, equip_desc):
    """
    args:
        message: 接收到的登录消息内容
        ack_event_hex: 登录响应消息的编码
        equip_desc: 设备描述
    """
    log.msg('%s(==>>):equip(%s) login(auto ack)'
            % (equip_desc, message['EQUIP_CODE']))
    log.msg('szhu  log =============>(%s)' % message)

    # 更新设备登录状态
    MysqlPool.insert_data_db(update_equip_status, (message['EQUIP_CODE'],))

    # 应答登录消息
    down_stream_messsage = {
        'equip_code': message['EQUIP_CODE'],
        'event_no_hex': ack_event_hex,
        'msg_body_data': bytes([]),
        'protocol': message['PROTOCOL']
    }
    # 发送响应消息
    send_downstream_message(down_stream_messsage)


#
# # 向设备发送信息查询更新消息,检测在线
# def query_equip_info(equip_code, company_id):
#     new_message = {
#         'equip_code': None,
#         'event_id': None,
#         'param_json': json.dumps(None, ensure_ascii=False, cls=commconfig.JSONEncoder),
#         'companyid': company_id,
#     }
#     _, equip_type = get_message_equip_type(equip_code)
#     event_set = commconfig.equip_setting_event_map.get(equip_type)  # 设备又需要主动发起的消息
#     new_message['equip_code'] = equip_code
#     if event_set:
#         for event_no in event_set:
#             new_message['event_id'] = event_no
#         sql_insert = commconfig.insert_downstreamsql_insert_sql % new_message
#         insert_data_db(sql_insert)
