import time
import struct
import datetime
from twisted.python import log
from . import event_meta
from .login_handler import default_equip_login
from comm.down_message import send_downstream_message,send_message_to_equip
from utils.RedisExecute import RedisExecute
from .helper.demo_funcs import demo_env_update_helper

# Demo设备登录  020101
def demo_login(message):
    default_equip_login(message, event_meta['DEMO_LOGIN_ACK']['EVENT'], 'ES Controller')

    time.sleep(1)
    # 发送时间
    demo_rtc_set_datetime_req(message['EQUIP_CODE'],
                                event_meta['DEMO_RTC_SET_DATETIME_REQ']['EVENT'],
                                None, message['PROTOCOL'])


# Demo配置更新 020102
def demo_config_set_req(equip_code, event_no_hex, msg_body_json, protocol):
    # 构建设置请求消息
    msg_body_data = struct.pack('!B', msg_body_json['DEMO_REPORT_ENV_INTERVAL'])
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send set config', system="REQ")

# Demo配置更新响应 030102
def demo_config_set_ack(message):
    log.msg(f"{message['EQUIP_CODE']}set config", system="ACK")


# 时间信息推送 DEMO_RTC_SET_DATETIME_REQ 020401
def demo_rtc_set_datetime_req(equip_code, event_no_hex, message_body, protocol):
    now_date = datetime.datetime.now()
    # 构建消息
    msg_body_data = struct.pack('!3B', now_date.year % 100, now_date.month, now_date.day) + \
                    struct.pack('!3B', now_date.hour, now_date.minute, now_date.second)
    # 发送下行消息
    down_messsage = {
        'equip_code': equip_code,
        'event_no_hex': event_no_hex,
        'msg_body_data': msg_body_data,
        'protocol': protocol
    }
    send_downstream_message(down_messsage)
    log.msg(f'{equip_code} send SET RTC Datetime', system="020401-REQ")

# 时间信息推送响应 DEMO_RTC_SET_DATETIME_ACK 030401
def demo_rtc_set_datetime_ack(message):
    RedisExecute.redis_cmd_ack_set(event_meta['DEMO_RTC_SET_DATETIME_ACK']['EVENT'], message['EQUIP_CODE'])
    log.msg(f"{message['EQUIP_CODE']} send RTC datetime", system="030401-ACK")


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
