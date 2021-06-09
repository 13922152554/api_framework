# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from api.member_api import MemberApi
from middleware.project_yaml import member_data

# 获取登录接口测试数据
login_data = member_data['login']


class TestLogin(MemberApi):
    """ 用户_测试案例层 """

    @allure.story('登录')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", login_data)
    def test_login(self, test_data):
        """
        登录接口测试
        :param test_data: 登录接口测试数据
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))

        # 发起请求
        result = self.login_api(**test_data['data']).json()

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        log.info(f"{test_data['title']} 测试案例执行通过！\n")
