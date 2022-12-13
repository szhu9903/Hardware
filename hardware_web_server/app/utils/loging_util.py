import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import has_request_context, request

class AppFormatter(logging.Formatter):
    def format(self, record):
        record.method = ""
        record.remote_addr = ""
        if has_request_context():
            record.method = request.method
            record.remote_addr = request.remote_addr
        return super(AppFormatter, self).format(record)

def create_logger():
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.DEBUG)
    appFormatter = AppFormatter("[%(asctime)s - %(levelname)s] %(remote_addr)s %(method)s---> %(message)s", "%Y-%m-%d %H:%M:%S")
    # 输出到控制台
    out_handler = logging.StreamHandler()
    out_handler.setFormatter(appFormatter)
    # 所有日志
    all_handler = TimedRotatingFileHandler('log/all_log.log', when='D', backupCount=3)
    all_handler.setFormatter(appFormatter)
    # error日志
    err_handler = logging.FileHandler('log/error.log')
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(appFormatter)
    # 添加处理器
    app_logger.addHandler(out_handler)
    app_logger.addHandler(all_handler)
    app_logger.addHandler(err_handler)


log_paths = 'log'
if not os.path.exists(log_paths):
    os.mkdir(log_paths)

create_logger()



