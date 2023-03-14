import struct
import os
import json
import time
from twisted.python import log
from . import event_meta
from comm.down_message import send_downstream_message
from utils.RedisExecute import RedisExecute
from utils.mysql_db import MysqlPool

# 公共心跳包上报，不做处理，仅是收 020001
def message_comm_beat_report(message):
    log.msg('General Controller(<<==):%s get beat heart' % (message['EQUIP_CODE']))

# 公共配置更新 020002
def message_comm_beat_inter_req(equip_code, event_no_hex, msg_body_json, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!B', msg_body_json['SYS_HEART_BEAT_INTERVAL'])
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send beat', system="REQ")

# 公共配置更新响应 030002
def message_comm_beat_inter_ack(message):
    log.msg(f"{message['EQUIP_CODE']}set beat", system="ACK")


# 编号更新 020003
def message_he_num_set_req(equip_code, event_no_hex, msg_body_json, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!H', int(msg_body_json['he_num']))
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send set he num', system="REQ")

# 编号更新响应 030003
def message_he_num_set_ack(message):
    RedisExecute.redis_cmd_ack_set(event_meta['COMM_HE_NUM_SET_ACK']['EVENT'], message['EQUIP_CODE'])
    de_equipcode = message['EQUIP_CODE']
    msg_body = message['MSG_BODY']
    # unpack env data
    new_equipcode, = struct.unpack('!H', msg_body)
    # 更新设备启用状态为启用
    update_equip_start_sql = """
    UPDATE Hardware_Equip SET he_starttype='START' WHERE he_num=%s
    """
    MysqlPool.insert_data_db(update_equip_start_sql, (new_equipcode,))
    log.msg(f"{de_equipcode}set he num", system="ACK")
