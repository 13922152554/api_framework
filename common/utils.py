# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

from jsonpath import jsonpath
from decimal import Decimal


class Utils:

    @classmethod
    def deal_token(cls, response):
        """
        从响应结果中获取token
        :param response: 响应结果（已经转换成json格式的响应毕要）
        :return: 返回token值
        """

        token_type = jsonpath(response, '$..token_type')[0]
        token_value = jsonpath(response, '$..token')[0]
        token = f'{token_type} {token_value}'

        return token

    @classmethod
    def handle_decimal(cls, data: float):
        """
        将小数转换为两位数decimal
        :param data:
        :return:
        """
        x = '{0:.2f}'.format(float(data))
        y = f'{float(data):.2f}'

        return Decimal(y)


if __name__ == '__main__':
    data = Utils().handle_decimal(10.67)
    print(type(data))


