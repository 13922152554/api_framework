# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import os
from loguru import logger
from datetime import datetime
from common.handle_path import log_path


class HandleLogger(object):

    now_time = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, log_file_name='log.log'):
        """
        拼接log文件名
        """

        self.log_name = os.path.join(log_path, f'{self.now_time}-{log_file_name}')

    def __call__(self, fmt=None):
        """
        设置log日志输出到指定文件，配置输出格式
        :param args: None
        :param kwargs: None
        :return: 配置了日志输出文件及输出格式的logger对象
        """

        if not fmt:

            fmt = "<green>{time:YYYY-MM-DD HH:mm:ss:SSSS}</green> | " \
                  "{module} line:{line} {function} |{level} | {message}"

        logger.add(self.log_name, format=fmt, encoding='utf-8')

        return logger


log = HandleLogger()()







