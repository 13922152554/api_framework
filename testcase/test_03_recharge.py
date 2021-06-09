# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from decimal import Decimal
from common.handle_log import log
from api.member_api import MemberApi
from middleware.project_yaml import member_data
from middleware.data_replace import DataReplace as DR

# 获取注册接口测试数据
register_data = member_data['register']
login_data = member_data['login']
recharge_data = member_data['recharge']


class TestRecharge(MemberApi):
    """ 用户_测试案例层 """

    @allure.story("充值")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", recharge_data)
    def test_recharge(self, test_data, conn_db, get_login_data):
        """

        :param test_data: 充值接口测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))

        # 充值前查询数据库余额
        if test_data['sql']:
            before_amount: Decimal = conn_db.query_one(test_data['sql'])['leave_amount']
            log.info(f"充值前账户余额：{before_amount}")

            # 发送充值请求
            result = self.recharge_api(**test_data['data'], token=DR().token).json()

            # 充值后数据库余额查询
            after_amount: Decimal = conn_db.query_one(test_data['sql'])['leave_amount']
            log.info(f"充值后账户余额：{after_amount}")
        else:
            result = self.recharge_api(**test_data['data'], token=DR().token).json()

        # 响应结果code、msg校验
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        # 数据库断言
        if test_data['sql']:
            # 数据库余额与响应结果余额校验（需要先更新测试数据中的sql语句预期结果中的leave_amount字段值）
            db_amount = after_amount - before_amount
            self.assert_equal(self.to_two_decimal(test_data['data']['amount']), db_amount)

        log.info(f"{test_data['title']} 测试案例执行通过！\n")


if __name__ == '__main__':
    pytest.main()




