import copy
from flask import Blueprint, request, g, jsonify
from app.unit_config import default_result


special = Blueprint("special", __name__)

@special.before_request
def before_request_special():
    g.result = copy.deepcopy(default_result)
    # 特殊类型接口不做处理
    if request.path == "/api/v2/upload/img/":
        return
    if request.method in ['PUT', 'POST']:
        # 校验请求头信息
        if 'application/json' != request.headers['CONTENT_TYPE'].lower():
            g.result["message"] = "请求头错误"
            return jsonify(g.result)
        req_data = request.json
        if not (req_data and req_data.get('data')):
            g.result["message"] = "请求结构错误"
            return jsonify(g.result)


from . import user_controller
from . import sys_controller
