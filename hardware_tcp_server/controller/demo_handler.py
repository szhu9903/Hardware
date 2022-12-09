import struct
from twisted.python import log
from . import event_meta
from .login_handler import default_equip_login
from comm.down_message import send_downstream_message,send_message_to_equip
from utils.RedisExecute import RedisExecute
from .helper.demo_funcs import demo_env_update_helper

# Demo设备登录  020201
def demo_login(message):
    default_equip_login(message, event_meta['DEMO_LOGIN_ACK']['EVENT'], 'ES Controller')

    # time.sleep(3)
    # # 发送时间
    # es_time_req(message['EQUIP_CODE'],
    #                             message['COMPANY_ID'],
    #                             event_meta['ES_TIME_REQ']['EVENT'],
    #                             None, message['PROTOCOL'])

# # 时间信息推送 ES_TIME_REQ 020301
# def es_time_req(equip_id, company_id, event_no_hex, msg_body_json, protocol):
#     now_date = datetime.datetime.now()
#     msg_body_data = struct.pack('!H', now_date.year) + \
#                     struct.pack('!5B', now_date.month, now_date.day,
#                                 now_date.hour, now_date.minute, now_date.second)
#     log.msg('Login Time (==>>): send %s(%s) time (%s) req' % (equip_id, company_id, msg_body_data))
#     send_message_to_equip(equip_id, company_id, event_no_hex, msg_body_data, protocol)

# # 时间信息推送响应 ES_TIME_ACK 030301
# def es_time_ack(message):
#     company_id = message['COMPANY_ID']
#     result = message['MSG_BODY']
#     # 默认插入响应库
#     default_ack_deal(message)
#     log.msg('PrintCode Controller(<<==):%s(%s) send time ack(%s)'
#             % (message['EQUIP_CODE'], company_id, result))
#

# LED控制 TH_SET_LED_COLOR_REQ 020201
def demo_led_color_req(equip_code, event_no_hex, message_body, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!4B',
                                message_body['led_switch'],
                                message_body['led_r'],
                                message_body['led_g'],
                                message_body['led_b'])
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send SET LED color', system="REQ")

# LED控制 TH_SET_LED_COLOR_ACK 030201
def demo_led_color_ack(message):
    log.msg(f"{message['EQUIP_CODE']} SET LED color", system="ACK")

# 温湿度 接收到数据 020301
def demo_env_th_req(message):
    demo_env_update_helper(message)
    # ACK
    down_stream_messsage = {
        'equip_code': message['EQUIP_CODE'],
        'event_no_hex': event_meta['DEMO_ENV_TH_ACK']['EVENT'],
        'msg_body_data': bytes([]),
        'protocol': message['PROTOCOL']
    }
    send_downstream_message(down_stream_messsage)

# 温湿度 下发查询指令 010302
def demo_query_env_th_req(equip_code, event_no_hex, message_body, protocol):
    send_message_to_equip(equip_code, event_no_hex, message_body, protocol)
    log.msg(f'{equip_code} send Query Env', system="010302-REQ")

# 温湿度 查询环境数据响应 030302
def demo_query_env_th_ack(message):
    demo_env_update_helper(message)
    RedisExecute.redis_cmd_ack_set(event_meta['DEMO_QUERY_ENV_TH_ACK']['EVENT'], message['EQUIP_CODE'])
    log.msg(f"{message['EQUIP_CODE']} send Query Env", system="030302-ACK")
