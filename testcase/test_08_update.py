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


# 获取更新昵称接口测试数据
update_data = member_data['update']


class TestUpdate(MemberApi):
    """ 更新昵称接口  测试案例"""

    @allure.story("更新昵称")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", update_data)
    def test_update(self,test_data, conn_db, get_login_data):
        """

        :param test_data: 测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 更新测试数据
        test_data = json.loads(self.replace_data(test_data))

        # 发送更新昵称请求
        result = self.update_api(**test_data['data'], token=DR().token).json()

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        # 数据库断言
        if test_data['sql']:
            db_data = conn_db.query_one(test_data['sql'])
            self.assert_equal(test_data['data']['reg_name'], db_data['reg_name'])

        log.info(f"{test_data['title']}测试案例执行成功！\n")


