# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe


import json
import pytest
import allure
from decimal import Decimal
from common.handle_log import log
from case.member_case import MemberCase
from middleware.project_yaml import member_data

# 获取提现接口测试数据
withdraw_data = member_data['withdraw']


@pytest.mark.usefixtures("init_account_amount")
class TestWithdraw(MemberCase):
    """ 提现接口测试案例 """

    @allure.story("提现")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", withdraw_data)
    def test_withdraw(self, test_data, conn_db, get_login_data):
        """

        :param test_data: 提现接口测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))

        if test_data['sql']:
            # 提现前数据库余额查询
            before_amount: Decimal = conn_db.query_one(test_data['sql'])['leave_amount'] + \
                                     test_data['recharge_data']['amount']
            log.info(f"提现前账号余额：{before_amount}")

            # 发送提现请求
            result = self.case_withdraw(test_data)

            # 提现后数据库余额查询
            after_amount: Decimal = conn_db.query_one(test_data['sql'])['leave_amount']
            log.info(f"提现后账号余额：{after_amount}")
        else:
            result = self.case_withdraw(test_data)

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['code'], result['code'])

        # 数据库断言
        if test_data['sql']:
            db_amount: Decimal = before_amount - after_amount
            self.assert_equal(self.to_two_decimal(test_data['withdraw_data']['amount']), db_amount)

        log.info(f'{test_data["title"]} 测试案例执行通过！\n')






