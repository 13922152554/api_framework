# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from jsonpath import jsonpath
from common.handle_log import log
from api.loan_api import LoanApi
from middleware.project_yaml import loan_data
from middleware.data_replace import DataReplace as DR

# 获取新增项目接口测试数据
add_data = loan_data['add']


class TestAdd(LoanApi):
    """ 新增项目接口 业务层 """

    @allure.story("新增项目")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", add_data)
    def test_add(self, test_data, conn_db, get_login_data):
        """

        :param test_data: 新增项目接口测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))
        log.info(f"替换后的测试数据：{test_data}")

        # 发送新增项目请求
        result = self.add_api(**test_data['data'], token=DR().token).json()

        # 提取loan_id并添加至响应结果中
        if result['code'] == 0:
            result['loan_id'] = jsonpath(result, '$..id')[0]

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        # 数据库断言
        if test_data['sql']:
            test_data['sql'] = test_data['sql'].replace('#loan_id#', str(result['loan_id']))
            db_data = conn_db.query_one(test_data['sql'])
            self.assert_equal(test_data['data']['title'], db_data['title'])
            self.assert_equal(self.to_two_decimal(test_data['data']['amount']), db_data['amount'])
            self.assert_equal(self.to_two_decimal(test_data['data']['loan_rate']), db_data['loan_rate'])
            self.assert_equal(test_data['data']['loan_term'], db_data['loan_term'])
            self.assert_equal(test_data['data']['loan_date_type'], db_data['loan_date_type'])
            self.assert_equal(test_data['data']['bidding_days'], db_data['bidding_days'])

        log.info(f"{test_data['title']} 测试案例执行成功！\n")



