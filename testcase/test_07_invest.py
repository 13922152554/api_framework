# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from case.loan_case import LoanCase
from middleware.project_yaml import loan_data


# 获取投资接口测试数据
invest_data = loan_data['invest']


class TestInvest(LoanCase):
    """ 投资接口  案例层"""

    @allure.story("投资")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", invest_data)
    def test_invest(self, test_data, conn_db, init_account_amount, get_login_data):
        """

        :param test_data: 测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :param init_account_amount: 账号余额初始化
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))

        log.info(f"替换后的测试数据为：{test_data}")

        # 发送投资请求
        result = self.case_invest(test_data, get_login_data)

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        # 账户余额 + 数据库断言
        if test_data['sql']:
            # sql语句数据替换
            test_data['sql'] = json.loads(json.dumps(test_data['sql']).replace('#loan_id#', str(result['data']['loan_id'])))
            log.info(f"替换后的sql语句：{test_data['sql']}")

            # 数据库查询
            invest_db_data = conn_db.query_one(test_data['sql']['invest'])
            finance_db_data = conn_db.query_one(test_data['sql']['financeLog'])

            # 数据库断言
            self.assert_equal(self.to_two_decimal(test_data['invest_data']['amount']), invest_db_data['amount'])
            self.assert_equal(test_data['invest_data']['member_id'], finance_db_data['pay_member_id'])
            self.assert_equal(self.to_two_decimal(test_data['invest_data']['amount']), finance_db_data['amount'])

            # 账户余额断言
            member_db_data = conn_db.query_one(test_data['sql']['member'])
            self.assert_equal(self.to_two_decimal(test_data['recharge_data']['amount'] -
                                                  test_data['invest_data']['amount']), member_db_data['leave_amount'])

        log.info(f"{test_data['title']} 测试案例执行成功！\n")

