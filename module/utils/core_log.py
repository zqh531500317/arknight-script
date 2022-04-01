import logging
import os
import sys
from logzero import LogFormatter, setup_default_logger, logfile, logger
from module.utils.core_config import configList
from module.utils.core_utils import project_root_path


def init_log():
    print("init_log")
    # 日志等级
    level_str = configList["Config"]["Log"]["level"]
    level = logging.INFO
    if level_str == "DEBUG":
        level = logging.DEBUG
    elif level_str == "INFO":
        level = logging.INFO
    elif level_str == "WARNING":
        level = logging.WARNING
    elif level_str == "ERROR":
        level = logging.ERROR
    elif level_str == "CRITICAL":
        level = logging.CRITICAL
    # 时间格式
    data_style = '%Y-%m-%d %H:%M:%S'

    # 控制台输出格式
    handler_format = '%(color)s[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s%(end_color)s'
    hand_format = LogFormatter(fmt=handler_format, datefmt=data_style)
    if configList["Config"]["Log"]["handler"]:
        setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=False)
    else:
        setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=True)

    # 文件输出格式
    if configList["Config"]["Log"]["file"]:
        dic_path = project_root_path() + "/log/"
        file_format = '[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s'
        formatter = logging.Formatter(file_format, data_style)
        # sys.stderr = open(configList["Config"]["System"]["project_path"] + "/log/stderr.txt", "w+", encoding='utf-8')
        # sys.stdout = open(configList["Config"]["System"]["project_path"] + "/log/stdout.txt", "w+", encoding='utf-8')
        logfile(dic_path + 'log.log',
                formatter=formatter,
                maxBytes=1e6, encoding='utf-8', loglevel=level)
    logger.info("初始化日志配置")
