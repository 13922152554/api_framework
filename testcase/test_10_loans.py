# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from api.loan_api import LoanApi
from middleware.project_yaml import loan_data

# 获取项目列表接口测试数据
loans_data = loan_data['loans']


class TestLoans(LoanApi):
    """ 项目列表接口 测试案例"""

    @allure.story("项目列表")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", loans_data)
    def test_loans(self, test_data):
        """

        :param test_data: 接口测试数据
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 发起获取项目列表请求
        result = self.loans_api(**test_data['data']).json()

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        if test_data['expect'].get("loan_len"):
            self.assert_equal(test_data['expect']['loan_len'], len(result['data']))

        log.info(f"{test_data['title']}测试案例执行成功！\n")
