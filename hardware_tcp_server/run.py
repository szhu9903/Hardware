#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：run.py
@Author  ：szhu9903
@Date    ：2022/11/16 15:51 
'''

import sys
import traceback
import logging

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.python import log
from twisted.python import context

from comm.resolve_message import extract_req_message
from timetask import deal_upstream_message, deal_downstream_message, check_equip_status
from config import sys_config

context.setDefault(log.ILogContext, {"system": "Twisted"})
log.FileLogObserver.timeFormat = "%Y-%m-%d %H:%M:%S"
log.startLogging(sys.stdout)


class GenericProtocol(Protocol):
    """ Protocol连接 """
    def __init__(self, factory):
        self.factory = factory
        self.data = bytes([])
        self.equip_id = 0
        self.last_message_time = 0
        self.client_host = None
        self.client_port = None

    def connectionMade(self):
        """ 连接创建时 """
        self.client_host = self.transport.getPeer().host
        self.client_port = self.transport.getPeer().port
        log.msg('new client [%s : %s]' % (self.client_host, self.client_port))

    def dataReceived(self, data):
        """ 接收到消息时 """
        log.msg(f'Get new data ({data.hex()})', system="Receive")
        self.data = self.data + data

        # 检查消息完整性
        while len(self.data) > 10:
            # 非法消息头，重置链接
            if self.data[0] != 0x5B or self.data[1] != 0x7c:
                self.data = self.data[1:]  # 不是包头则跳过,丢弃包头
                continue
            # 消息总长度 = 消息固定的头尾部分：11个字节 + 消息体数据长度
            message_length = self.data[7] + 11
            if len(self.data) < message_length:
                return

            try:
                # 非法消息尾，重置链接
                if self.data[message_length-1] != 0x0A or self.data[message_length-2] != 0x0D:
                    error_msg = 'Protocol:Error Message Received(Wrong tail:0x%0X 0x%0X), close link.!' % \
                                (self.data[message_length-2], self.data[message_length-1])
                    log.err(error_msg)
                    # 错误消息直接切断链路
                    self.close_connection()
                    return

                # 获取消息
                message_data = self.data[:message_length]
                # 剩余未解析的消息
                self.data = self.data[message_length:]

                # 解析消息
                req_message = extract_req_message(message_data, self)
                if not req_message:
                    log.err('Protocol:Corrupt Message! discard')
                    return
                log.msg('======== %s ==========> %s' % (req_message['EVENT_NO'], req_message),  system="Receive")
                # 调用辅助线程执行事件处理函数
                reactor.callInThread(deal_upstream_message, req_message)

            except Exception as Err:
                traceback.print_exc()
                log.err('Protocol:Deal upstream message err:%s' % str(Err))

    def connectionLost(self, reason):
        """ 链路断 """
        log.msg('Protocol:Connection broken(%s)' % (str(self.transport.getPeer())))
        self.close_connection()

    # 关闭连接，同时清理信息
    def close_connection(self):
        log.msg('close socket [%s : %s]' % (self.client_host, self.client_port))
        if hasattr(self, 'data'):
            del self.data
        self.transport.abortConnection()
        # self.transport.loseConnection()


# Protocol连接工厂函数
class GenericFactory(Factory):

    def buildProtocol(self, addr):
        return GenericProtocol(self)


def sys_init():
    """ 初始化工程 """
    # 初始化Mysql
    from utils.mysql_db import MysqlPool
    MysqlPool()
    log.msg('Init OK!', system="Mysql")

    # 初始化RabbitMQ
    from utils.rabbitmq import RabbitMQ
    RabbitMQ()
    log.msg('Init OK!', system="RabbitMQ")

    # 初始化系统参数
    from utils.RedisExecute import RedisExecute
    RedisExecute()
    log.msg('Init OK!', system="Redis")

    from comm.system import sys_param_init
    sys_param_init()

    # 5秒后执行下行消息检查线程
    def start_deal_downstream_message():
        reactor.callInThread(RabbitMQ.start_receive, deal_downstream_message)

    reactor.callLater(5, start_deal_downstream_message)

    # 10秒后执行查询设备状态
    def start_check_equip_status():
        reactor.callInThread(check_equip_status)

    reactor.callLater(10, start_check_equip_status)


if __name__ == '__main__':
    log.msg('start twisted server ...')
    sys_init()
    reactor.listenTCP(8891, GenericFactory())
    reactor.suggestThreadPoolSize(10)  # 定义线程池
    log.msg('Twisted listen ...')
    reactor.run()
