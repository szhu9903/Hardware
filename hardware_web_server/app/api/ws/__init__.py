#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：blog_server 
@File    ：__init__.py.py
@Author  ：szhu9903
@Date    ：2022/12/7 16:44 
'''

import copy
from flask import Blueprint, request, g, render_template
from app.unit_config import default_result


ws = Blueprint("ws", __name__)

@ws.before_request
def before_request_special():
    g.result = copy.deepcopy(default_result)


from . import demo_ws
