# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from case.loan_case import LoanCase
from middleware.project_yaml import loan_data
from middleware.data_replace import DataReplace as DR


# 获取审核项目接口测试数据
audit_data = loan_data['audit']


class TestAudit(LoanCase):
    """ 项目审核接口 案例层"""

    @allure.story("审核项目")
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", audit_data)
    def test_audit(self, test_data, conn_db, get_login_data):
        """

        :param test_data: 项目审核接口测试数据
        :param conn_db: 数据库连接对象
        :param get_login_data: 普通用户登录_响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(self.replace_data(test_data))

        # 发起项目审核请求
        result = self.case_audit(test_data)

        # 响应结果断言
        self.assert_equal(test_data['expect']['code'], result['code'])
        self.assert_equal(test_data['expect']['msg'], result['msg'])

        log.info(f"替换后的测试数据为：{test_data}")

        # 数据库断言
        if test_data['sql']:
            # sql语句数据替换
            test_data['sql'] = test_data['sql'].replace('#loan_id#', str(result['loan_id']))

            db_data = conn_db.query_one(test_data['sql'])

            self.assert_equal(test_data['expect']['status'], db_data['STATUS'])

        log.info(f"{test_data['title']} 测试案例执行成功！\n")


if __name__ == '__main__':
    pytest.main()

