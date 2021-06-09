# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from api.member_api import MemberApi
from middleware.project_yaml import member_data
from middleware.data_replace import DataReplace as DR


# 获取用户信息接口测试数据
member_info_data = member_data['member_info']


class TestMemberInfo(MemberApi):
    """ 获取用户信息接口  测试案例 """

    @allure.story("获取用户信息")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", member_info_data)
    def test_member_info(self, test_data, conn_db, get_login_data):
        """

        :param test_data: 接口测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 管理员登录
        if test_data['data']['user_type'] == 'admin':
            # 管理员用户登录
            MemberApi().get_login_data(user_type=0)

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))

        log.info(f"替换后的测试数据为：{test_data}")

        # 发起获取用户信息请求
        result = self.member_info_api(test_data['data']['member_id'], token=DR().token).json()

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        # 数据库断言
        if test_data['sql']:
            db_data = conn_db.query_one(test_data['sql'])
            self.assert_equal(test_data['expect']['mobile_phone'], db_data['mobile_phone'])

        log.info(f"{test_data['title']}测试案例执行成功！\n")

