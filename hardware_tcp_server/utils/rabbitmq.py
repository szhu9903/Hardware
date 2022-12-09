#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：rabbitmq.py
@Author  ：szhu9903
@Date    ：2022/11/21 16:03 
'''

import pika
from config import RabbitConf

class RabbitMQ(object):
    """
    RabbitMQ 接收服务器消息
    """
    __channel = None

    def __new__(cls, *args, **kwargs):
        # 在构造链接时传递给连接适配器连接参数的实例。
        connection_parameters = pika.ConnectionParameters(
            host=RabbitConf.host,  # 要连接的主机名或IP地址
            port=RabbitConf.port,  # 要连接的TCP端口
            virtual_host=RabbitConf.virtual_host,  # 要使用的 RabbitMQ 虚拟主机
            credentials=pika.PlainCredentials(RabbitConf.username, RabbitConf.password),  # 身份验证
        )
        # 创建连接
        connection = pika.BlockingConnection(connection_parameters)
        # 创建连接内通道
        cls.__channel = connection.channel()
        super(RabbitMQ, cls).__new__(cls)

    @classmethod
    def start_receive(cls, callback_func):
        # 声明队列， 不存在会自动创建
        cls.__channel.queue_declare(queue='demo_queue', durable=True)
        # 接收消息，设置公平模式，当消费者ACK，rabbitMQ再发送下一条消息
        cls.__channel.basic_qos(prefetch_count=1)
        # 接收消息
        cls.__channel.basic_consume(queue='demo_queue',
                                    on_message_callback=callback_func,
                                    auto_ack=False)
        cls.__channel.start_consuming()



