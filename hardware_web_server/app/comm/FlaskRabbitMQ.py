#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：blog_server 
@File    ：RabbitMQ.py
@Author  ：szhu9903
@Date    ：2022/12/2 16:56 
'''

import pika
import json

class FlaskRabbitMQ(object):
    """
    RabbitMQ 接收服务器消息
    """
    __connection_parameters = None
    __connection = None
    __channel = None

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.rabbitmq_config = app.config['RABBITMQ_CONFIG']
        # 在构造链接时传递给连接适配器连接参数的实例。
        FlaskRabbitMQ.__connection_parameters = pika.ConnectionParameters(
            host=self.rabbitmq_config['rabbitmq_host'],  # 要连接的主机名或IP地址
            port=self.rabbitmq_config['rabbitmq_port'],  # 要连接的TCP端口
            virtual_host=self.rabbitmq_config['rabbitmq_virtual_host'],  # 要使用的 RabbitMQ 虚拟主机
            heartbeat=0,
            credentials=pika.PlainCredentials(self.rabbitmq_config['rabbitmq_username'],
                                              self.rabbitmq_config['rabbitmq_password']))
        FlaskRabbitMQ.__connection = pika.BlockingConnection(FlaskRabbitMQ.__connection_parameters)
        FlaskRabbitMQ.__channel = FlaskRabbitMQ.__connection.channel()
        # 声明队列， 不存在会自动创建
        FlaskRabbitMQ.__channel.queue_declare(queue='demo_queue', durable=True)

    @classmethod
    def basic_publish(cls, message_data):
        if not cls.__connection or cls.__connection.is_closed:
            cls.__connection = pika.BlockingConnection(cls.__connection_parameters)
            cls.__channel = cls.__connection.channel()
        # 创建连接内通道
        if not cls.__channel or cls.__channel.is_closed:
            cls.__channel = cls.__connection.channel()

        # 发送消息
        cls.__channel.basic_publish(exchange='',  # 要发布到的交换机
                              routing_key='demo_queue',  # 队列名称
                              body=message_data,
                              properties=pika.BasicProperties(
                                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                              ))

    @classmethod
    def send_to_all_equip(cls, event_no, message_data):
        message_body = {
            'MODE': 'ALL',  # 发送模式 ALL：全部设备 TYPE：分类下所有设备 SINGLE：单一按照指令编码
            'EQUIP_TYPE': '',  # 设备分类，只有mode为TYPE模式时有效
            'EQUIP_NO': '',  # 设备编码， 只有mode为SINGLE模式时有效
            'EVENT_NO': event_no,  # 指令编码
            'DATA': message_data
        }
        message_data = json.dumps(message_body)
        cls.basic_publish(message_data)

    @classmethod
    def send_to_type_equip(cls, equip_type, event_no, message_data):
        message_body = {
            'MODE': 'TYPE',  # 发送模式 ALL：全部设备 TYPE：分类下所有设备 SINGLE：单一按照指令编码
            'EQUIP_TYPE': equip_type,  # 设备分类，只有mode为TYPE模式时有效
            'EQUIP_NO': '',  # 设备编码， 只有mode为SINGLE模式时有效
            'EVENT_NO': event_no,  # 指令编码
            'DATA': message_data
        }
        message_data = json.dumps(message_body)
        cls.basic_publish(message_data)

    @classmethod
    def send_to_equip(cls, equip_no, event_no, message_data):
        message_body = {
            'MODE': 'SINGLE',  # 发送模式 ALL：全部设备 TYPE：分类下所有设备 SINGLE：单一按照指令编码
            'EQUIP_TYPE': '',  # 设备分类，只有mode为TYPE模式时有效
            'EQUIP_NO': equip_no,  # 设备编码， 只有mode为SINGLE模式时有效
            'EVENT_NO': event_no,  # 指令编码
            'DATA': message_data
        }
        send_data = json.dumps(message_body)
        cls.basic_publish(send_data)
