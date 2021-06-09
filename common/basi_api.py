# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import requests
from common.handle_log import log
from middleware.project_yaml import conf_data
from common.utils import Utils
from common.handle_assert import HandleAssert
from middleware.data_replace import DataReplace as DR


class BaseApi:
    conf_data = conf_data
    host = conf_data['env']['host']
    mysql_conf = conf_data['mysql']
    headers = conf_data['request_headers']['headers']
    account = conf_data['account']

    @staticmethod
    def send_http(data):
        try:
            log.info(f"请求参数：{data}")
            response = requests.request(**data)
            log.info(f"响应结果：{response.json()}")
        except Exception as e:
            log.error(f"发送请求失败，错误信息：{e}")
            raise e
        else:
            return response

    @staticmethod
    def deal_url(api_url):
        """
        处理请求地址
        :param api_url: 接口地址
        :return: 包含服务器地址的接口请求地址
        """

        if api_url.startswith("http://") or api_url.startswith("https://"):
            pass
        else:
            base_url = f"{BaseApi().host}{api_url}"
            return base_url

    @staticmethod
    def get_token(response):
        """
        获取token
        :param response:
        :return:
        """

        return Utils().deal_token(response)

    @staticmethod
    def to_two_decimal(data):
        """
        将整数/浮点数 转化为两位数decimal
        :param data:
        :return:
        """
        return Utils.handle_decimal(data)

    @staticmethod
    def assert_equal(ex, re):
        """
        断言预期结果与实际结果是否相等
        :param ex: 预期结果
        :param re: 实际结果
        :return:
        """

        return HandleAssert().eq(ex, re)

    @staticmethod
    def assert_contains(ex, re):
        """
        断言预期结果是否包含在实际结果中
        :param ex: 预期结果
        :param re: 实际结果
        :return:
        """

        return HandleAssert().contains(ex, re)

    @staticmethod
    def replace_data(target_string: str, source_string: dict = None):
        """
        测试数据替换
        :param target_string:
        :param source_string:
        :return:
        """

        return DR().replace_data(target_string, source_string=source_string)











