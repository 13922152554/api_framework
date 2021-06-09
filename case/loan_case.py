# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import allure
from jsonpath import jsonpath
from api.loan_api import LoanApi
from api.member_api import MemberApi
from middleware.data_replace import DataReplace as DR
from common.wrapper import log_info


class LoanCase(LoanApi):
    """ 用户_业务层
        业务层：负责关联接口、替换关联接口动态参数、传递token"""

    member_api = MemberApi()

    @log_info
    @allure.step('step:调用业务api-审核项目')
    def case_audit(self, data: dict):
        """
        审核项目业务场景
        :param data: 审核项目接口测试数据
        :return: 响应数据
        """

        if data.get('add_data'):
            # 发起新增项目请求
            add_res = self.add_api(**data['add_data'], token=DR().token).json()
            # 提取loan_id
            loan_id = jsonpath(add_res, "$..id")[0]
            # 管理员登录，发起项目审核请求
            self.member_api.get_login_data(user_type=0)
            response = self.audit_api(loan_id, data['audit_data']['approved_or_not'], token=DR().token).json()
            response['loan_id'] = loan_id
        else:
            # 管理员登录，发起项目审核请求
            self.member_api.get_login_data(user_type=0)
            response = self.audit_api(**data['audit_data'], token=DR().token).json()

        return response

    @log_info
    @allure.step('step:调用业务api-投资项目')
    def case_invest(self, data: dict, login_data):
        """
        投资业务场景
        :param data: 投资接口测试数据
        :param login_data: 普通用户登录响应数据
        :return: 响应数据
        """

        # 发起充值请求
        self.member_api.recharge_api(**data['recharge_data'], token=DR().token)

        # 新增/审核项目
        if data.get('add_data'):
            audit_res = self.case_audit(data)
            # 投资
            response = self.invest_api(data['invest_data']['member_id'], audit_res['loan_id'],
                                       data['invest_data']['amount'], token=login_data['token']).json()
        else:
            response = self.invest_api(**data['invest_data'], token=DR().token).json()

        return response

















