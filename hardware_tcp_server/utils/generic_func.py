#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：utils.py
@Author  ：szhu9903
@Date    ：2022/11/16 17:37 
'''

from config import sys_config

# 获取校验活，取和的低字节
def get_check_sum(data):
    return sum(data) % 256

# 获取节点分类
def get_equip_type(equip_code):
    for t_name, (code_down, code_up) in sys_config['equip_type'].items():
        if code_down <= equip_code <= code_up:
            return t_name
