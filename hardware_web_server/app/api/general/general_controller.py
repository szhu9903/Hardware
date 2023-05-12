import logging
from . import general
from flask import request, g, jsonify
from app.comm.CompositeOperate import CompositeOperate
from .UserController import UserController
from .DemoController import DemoLedController
from .Full103Controller import Full103RelayController
from .SysController import ConfigVarController
from app.module_config import table_module_map
from app.unit_config import error_info_map

logger = logging.getLogger('app')

operate_config = {
    'sysuser': UserController(table_module_map['sysuser']),
    'sysrole': CompositeOperate(table_module_map['sysrole']),
    'syspurview': CompositeOperate(table_module_map['syspurview']),
    'sysmenu': CompositeOperate(table_module_map['sysmenu']),
    'hardwaretype': CompositeOperate(table_module_map['hardwaretype']),
    'hardwareequip': CompositeOperate(table_module_map['hardwareequip']),
    'hardwareconfigvar': ConfigVarController(table_module_map['hardwareconfigvar']),

    'demoenv': CompositeOperate(table_module_map['demoenv']),
    'demoled': DemoLedController(table_module_map['demoled']),

    'full103env': CompositeOperate(table_module_map['full103env']),
    'full103relay': Full103RelayController(table_module_map['full103relay']),

}

# get 请求通用处理
@general.route('/<string:config_name>/', methods=["GET"])
@general.route('/<string:config_name>/<int:record_id>/', methods=["GET"])
def general_get_api(config_name, record_id=None):
    logger.info(f"{config_name}-GET")
    try:
        if config_name.lower() in operate_config.keys():
            operate_config[config_name].deal_get_method(request)
        else:
            g.result["message"] = f'未匹配到视图{config_name}'
    except Exception as Err:
        g.result["message"] = f'异常{str(Err)}'
    logger.info(f"res-{config_name}-GET===={g.result['status']}")
    return jsonify(g.result)

# post 请求通用处理
@general.route('/<string:config_name>/', methods=["POST"])
def general_post_api(config_name):
    logger.info(f"{config_name}")
    try:
        if config_name.lower() in operate_config.keys():
            operate_config[config_name].deal_post_method(request)
        else:
            g.result["message"] = f'未匹配到视图{config_name}'
    except Exception as Err:
        g.result["message"] = f'异常{str(Err)}'
        for e, v in error_info_map.items():
            if e in str(Err):
                g.result["message"] = v
    logger.info(f"[res-{config_name}]===={g.result['status']}")
    return jsonify(g.result)

# put 请求通用处理
@general.route('/<string:config_name>/<int:record_id>/', methods=["PUT"])
def general_put_api(config_name, record_id):
    logger.info(f"{config_name}-{record_id}")
    try:
        if config_name.lower() in operate_config.keys():
            operate_config[config_name].deal_put_method(request)
        else:
            g.result["message"] = f'未匹配到视图{config_name}'
    except Exception as Err:
        g.result["message"] = f'异常{str(Err)}'
        for e, v in error_info_map.items():
            if e in str(Err):
                g.result["message"] = v
    logger.info(f"res-{config_name}-{record_id}===={g.result['status']}")
    return jsonify(g.result)

# delete 请求通用处理
@general.route('/<string:config_name>/<int:record_id>/', methods=["DELETE"])
def general_delete_api(config_name, record_id):
    logger.info(f"{config_name}-{record_id}")
    try:
        if config_name.lower() in operate_config.keys():
            operate_config[config_name].deal_delete_method(request)
        else:
            g.result["message"] = f'未匹配到视图{config_name}'
    except Exception as Err:
        g.result["message"] = f'异常{str(Err)}'
    logger.info(f"res-{config_name}-{record_id}===={g.result['status']}")
    return jsonify(g.result)

