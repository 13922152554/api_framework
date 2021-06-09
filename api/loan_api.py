# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

from common.basi_api import BaseApi


class LoanApi(BaseApi):
    """ 用户_接口层 """

    def add_api(self, member_id: int, title: str, amount: int, loan_rate: float, loan_term: int, loan_date_type: int, bidding_days: int, token):
        """
        新增项目接口
        :param member_id: 用户id
        :param title: 标题
        :param amount: 借款金额
        :param loan_rate: 年利率
        :param loan_term: 借款期限
        :param loan_date_type: 借款期限类型
        :param bidding_days: 竞标天数
        :param token: 令牌
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['add'])

        data = {
            "url": url,
            "method": "POST",
            "headers": self.headers,
            "json": {
                "member_id": member_id,
                "title": title,
                "amount": amount,
                "loan_rate": loan_rate,
                "loan_term": loan_term,
                "loan_date_type": loan_date_type,
                "bidding_days": bidding_days
            }
        }

        data['headers'].update({'Authorization': token})
        response = self.send_http(data)

        return response

    def audit_api(self, loan_id: int, approved_or_not: str, token):
        """
        项目审核接口
        :param loan_id: 项目id
        :param approved_or_not: 审核状态：true 表示通过 false 表示审核不通过
        :param token:
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['audit'])

        data = {
            "url": url,
            "method": "PATCH",
            "headers": self.headers,
            "json": {
                "loan_id": loan_id,
                "approved_or_not": approved_or_not
            }
        }

        data['headers'].update({'Authorization': token})
        response = self.send_http(data)

        return response

    def invest_api(self, member_id: int, loan_id: int, amount: int, token):
        """
        投资接口
        :param member_id: 用户id
        :param loan_id: 标id
        :param amount: 投资金额
        :param token:
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['invest'])

        data = {
            "url": url,
            "method": "POST",
            "headers": self.headers,
            "json": {
                "member_id": member_id,
                "loan_id": loan_id,
                "amount": amount
            }
        }

        data['headers'].update({'Authorization': token})
        response = self.send_http(data)

        return response

    def loans_api(self, pageIndex: int=None, pageSize: int=None):
        """
        项目列表接口
        :param pageIndex: 当页索引
        :param pageSize: 每页大小
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['loans'])

        data = {
            "url": url,
            "method": "GET",
            "headers": self.headers,
            "params": {
                "pageIndex": pageIndex,
                "pageSize": pageSize
            }
        }

        response = self.send_http(data)

        return response

