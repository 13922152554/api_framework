"""
============================
Author:古一
Time:2020/11/12
E-mail:369799130@qq.com
============================
"""

import json
from common.handle_log import log
from middleware.project_yaml import res_yaml
from middleware.project_yaml import conf_data


def log_info(func):
    """
    日志装饰器，简单记录函数输入输出
    :param func: 装饰的函数
    :return:
    """
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        log.info(f'\n调用函数:{func.__name__},\n传入参数：{args, kwargs}，响应结果：{res}')
        return res

    return inner


def write_res(func):
    """
    将api接口response写入到配置文件中，写入的是一个字典类型：key：当前被装饰函数名，value：response（转换成json字符串类型）
    :param func: 装饰的函数
    :return:
    """

    def inner(*args, **kwargs):
        res = func(*args, **kwargs)

        log.info(f"向yaml文件写入响应结果：{res}")
        # 拼接Key名
        key_name = f"{func.__name__}_res"
        # 向yaml文件写入该函数的响应结果，写入格式：{key_name: json.dumps(res)}
        res_yaml.write_data_to_yaml({key_name: json.dumps(res)})

        return res

    return inner








