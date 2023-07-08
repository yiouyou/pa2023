# coding=utf-8

from pathlib import Path
_pwd = Path(__file__).absolute()
_module_path = _pwd.parent

from module.util import timestamp_now
_ts = timestamp_now()
_log = f"pa.log"

import logging
logger = logging.getLogger(_log)

import os
_log_path = os.path.join(_module_path.parent, "log", _log)

# 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
logger.setLevel(level=logging.DEBUG)

# 获取文件日志句柄并设置日志级别，第二层过滤
handler = logging.FileHandler(_log_path, encoding='utf-8', mode='a')
handler.setLevel(logging.INFO)

# 生成并设置文件日志格式，其中name为上面设置的mylog
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 获取流句柄并设置日志级别，第二层过滤
console = logging.StreamHandler()
console.setLevel(logging.WARNING)

# 为logger对象添加句柄
logger.addHandler(handler)
logger.addHandler(console)

