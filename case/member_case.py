# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import allure
from api.member_api import MemberApi
from middleware.data_replace import DataReplace as DR
from common.wrapper import log_info
from common.handle_log import log


class MemberCase(MemberApi):
    """ 用户_业务层
    业务层：负责关联接口、替换关联接口动态参数、传递token"""

    @log_info
    @allure.step('step:调用业务api-提现')
    def case_withdraw(self, data: dict):
        """
        提现业务场景：登录 -> 提现
        :param data: 提现接口参数
        :return: 响应结果
        """
        if data.get("recharge_data"):
            self.recharge_api(**data['recharge_data'], token=DR().token)

        response = self.withdraw_api(**data['withdraw_data'], token=DR().token).json()

        return response


if __name__ == '__main__':
    test_data = {'title': '正确手机号与密码带注册名注册管理员账号_注册成功',
                 'data': {'mobile_phone': '#mobile_phone#', 'pwd': '12345678', 'type': 0, 'reg_name': 'keke'}}

    MemberCase().case_register(test_data)



