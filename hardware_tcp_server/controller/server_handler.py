import struct
import os
import json
import time
from twisted.python import log

from comm.down_message import send_downstream_message


# 公共心跳包上报，不做处理，仅是收 020001
def message_comm_beat_report(message):
    log.msg('General Controller(<<==):%s get beat heart' % (message['EQUIP_CODE']))

# 公共配置更新 020001
def message_comm_beat_inter_req(equip_code, event_no_hex, msg_body_json, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!2B',
                                msg_body_json['DEMO_HEART_BEAT_INTERVAL'],
                                msg_body_json['DEMO_REPORT_ENV_INTERVAL'])
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send beat', system="REQ")

# 公共配置更新响应 030001
def message_comm_beat_inter_ack(message):
    log.msg(f"{message['EQUIP_CODE']}set beat", system="ACK")


