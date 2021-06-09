# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import allure
from jsonpath import jsonpath
from common.basi_api import BaseApi
from common.wrapper import write_res


class MemberApi(BaseApi):
    """ 用户_接口层 """

    def register_api(self, mobile_phone: str, pwd: str, type: int = 1, reg_name: str = None):
        """
        注册接口
        :param mobile_phone: 手机号
        :param pwd: 密码
        :param type: 用户类型：0 管理员 1 普通会员，不传默认为 1
        :param reg_name: 昵称
        :return: 响应结果
        """

        # 拼接完整的url地址
        url = self.deal_url(self.conf_data['member_api']['register'])
        # 按接口要求配置请求参数
        data = {
            'url': url,
            'method': 'POST',
            'headers': self.headers,
            'json': {
                'mobile_phone': mobile_phone,
                'pwd': pwd,
                'type': type
            }
        }

        if reg_name:
            data['json']['reg_name'] = reg_name

        # 发送请求
        response = self.send_http(data)
        return response

    def login_api(self, mobile_phone: str, pwd: str):
        """
        登录接口
        :param mobile_phone: 手机号
        :param pwd: 密码
        :return: 响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['login'])
        data = {
            "url": url,
            "method": "POST",
            "headers": self.headers,
            "json": {
                "mobile_phone": mobile_phone,
                "pwd": pwd
            }
        }

        response = self.send_http(data)
        return response

    @write_res
    def get_login_data(self, user_type: int = 1):
        """
        获取登录后的响应结果数据
        :param user_type: 用户类型：0 管理员 非0 普通会员，不传默认为 1
        :return: 返回登录后的响应结果
        """

        if not user_type:
            account = self.conf_data['account']['admin']
        else:
            account = self.conf_data['account']['user']

        # 调用登录接口发起登录请求
        response = self.login_api(account['mobile_phone'], account['pwd']).json()
        res = dict()
        res["id"] = jsonpath(response, '$..id')[0]
        res['mobile_phone'] = jsonpath(response, '$..mobile_phone')[0]
        res['leave_amount'] = jsonpath(response, '$..leave_amount')[0]
        res["token"] = self.get_token(response)

        return res

    def recharge_api(self, member_id: int, amount: float, token):
        """
        充值接口
        :param member_id: 会员id
        :param amount: 充值金额
        :param token: 令牌
        :return: 响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['recharge'])
        data = {
            "url": url,
            "method": 'POST',
            "headers": self.headers,
            "json": {
                "member_id": member_id,
                "amount": amount
            }
        }

        data['headers'].update({'Authorization': token})
        response = self.send_http(data)

        return response

    def withdraw_api(self, member_id, amount: float, token):
        """
        提现接口
        :param member_id:  会员id
        :param amount: 充值金额
        :param token: 令牌
        :return: 响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['withdraw'])

        data = {
            "url": url,
            "method": "POST",
            "headers": self.headers,
            "json": {
                "member_id": member_id,
                "amount": amount
            }
        }

        data['headers'].update({'Authorization': token})
        response = self.send_http(data)

        return response

    def update_api(self, member_id: int, reg_name: str, token):
        """
        更新昵称接口
        :param member_id: 用户id
        :param reg_name: 用户昵称
        :param token:
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['update'])

        data = {
            "url": url,
            "method": "PATCH",
            "headers": self.headers,
            "json": {
                "member_id": member_id,
                "reg_name": reg_name
            }
        }

        data['headers'].update({'Authorization': token})

        response = self.send_http(data)

        return response

    def member_info_api(self, member_id: int, token):
        """
        用户信息接口
        :param member_id: 用户id
        :param token:
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['member_info'].replace('#member_id#', str(member_id)))

        data = {
            "url": url,
            "method": "GET",
            "headers": self.headers
        }

        data['headers'].update({'Authorization': token})

        response = self.send_http(data)

        return response







