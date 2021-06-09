# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from api.member_api import MemberApi
from middleware.project_yaml import member_data


# 获取注册接口测试数据
register_data = member_data['register']


class TestRegister(MemberApi):
    """ 用户_测试案例层 """

    @allure.story('注册')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize('test_data', register_data)
    def test_register(self, test_data, conn_db):
        """
        注册接口测试
        :param test_data: 注册接口测试数据（包含：title、data、expect、sql)
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data['data'] = json.loads(self.replace_data(test_data['data']))

        # 发送请求
        result = self.register_api(**test_data['data']).json()

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        # 数据库断言
        if test_data['sql']:
            test_data['sql'] = test_data['sql'].replace("#mobile_phone#", test_data['data']["mobile_phone"])
            count = conn_db.get_count(test_data['sql'])
            self.assert_equal(1, count)

        log.info(f"{test_data['title']} 测试案例执行通过！\n")

