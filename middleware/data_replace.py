# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import re
import json
import random
from jsonpath import jsonpath
from faker import Faker
from middleware.project_yaml import conf_data
from middleware.project_mysql import ProjectMysql
from middleware.project_yaml import res_yaml


class DataReplace:

    def __init__(self):
        self.db = ProjectMysql()

    @property
    def token(self):

        res = json.loads(res_yaml.get_yaml_data()['get_login_data_res'])
        token = jsonpath(res, '$..token')[0]

        return token

    @property
    def member_id(self):
        """
        从登录响应结果中获取member_id
        :return:  member_id
        """

        res = json.loads(res_yaml.get_yaml_data()['get_login_data_res'])

        return str(jsonpath(res, '$..id')[0])

    @property
    def error_id(self):
        """ 返回非当前登录用户的id(member表中已存在的id) """

        res = json.loads(res_yaml.get_yaml_data()['get_login_data_res'])

        return str(jsonpath(res, '$..id')[0] + 1)

    @property
    def bidding_loan_id(self):
        """ invest接口第2条案例数据:查找数据库中loan表status为2的且不等于当前类loan_id属性值的最大项目id """

        sql = f"select MAX(id) from loan where status=2; "
        sql_result = self.db.query_one(sql)

        return str(sql_result['MAX(id)'])

    @property
    def err_loan_id(self):
        """ 返回数据库loan表中不存在的项目id """

        sql = "SELECT MAX(id) FROM loan;"
        sql_result = self.db.query_one(sql)

        return str(sql_result['MAX(id)'] + 1)

    @property
    def auditting_loan_id(self):
        """ 返回数据库中loan表status为1的最大项目id """

        sql = "SELECT MAX(id) FROM loan WHERE STATUS=1;"
        sql_result = self.db.query_one(sql)

        return str(sql_result["MAX(id)"])

    @property
    def title(self):
        """ 生成项目标题 """

        start_str = random.choice(["博时", "广发", "平安银行", "招商银行", "建设银行", "华夏", "国金"])
        middle_str = random.choice(["货币", "信币", "惠币", "余额宝", "现金宝"])
        end_str = random.choice(["A", "B", "E", "增强"])

        return start_str + middle_str + end_str

    @property
    def max_title(self):
        """ 生成一个长度大于50的字符 """

        my_str = list("abcdefghijklmnopqrstuvwsyz")

        new_str = ""
        for i in range(51):
            new_str += random.choice(my_str)

        return new_str

    @property
    def max_amount(self):
        """ 查询数据库用户余额，返回大于当前余额的金额 """

        res = json.loads(res_yaml.get_yaml_data()['get_login_data_res'])

        sql = f"SELECT leave_amount FROM member WHERE id={res['id']};"

        sql_result = self.db.query_one(sql)

        return str(float(sql_result["leave_amount"]) + 0.1)

    @property
    def mobile_phone(self):
        """ 生成未注册的手机号，手机号在member表查询不到记录则表示未注册 """

        while True:
            # 生成手机号
            phone = self.__make_phone()
            select_sql = f"select * from member where mobile_phone={phone};"

            # member表中查询手机号返回的结果为0时表示手机号未生成，否则将循环生成并判断生成的手机号是否注册
            if self.db.get_count(select_sql) == 0:
                self.db.close()
                return phone

    @property
    def old_phone(self):
        """ 获取数据库中已注册的手机号 """

        sql = f"select * from member where id={1};"
        old_phone = self.db.query_one(sql)
        self.db.close()

        return old_phone["mobile_phone"]

    @property
    def admin(self):
        """ 从配置文件中获取admin区域中的mobile_phone的值（获取普通用户的账号） """

        return conf_data['account']['admin']['mobile_phone']

    @property
    def admin_pwd(self):
        """ 从配置文件中获取admin区域中的pwd的值（获取普通用户的账户密码）"""

        return conf_data['account']['admin']['pwd']

    @property
    def user(self):
        """ 从配置文件中获取user区域中的mobile_phone的值（获取普通用户的账号） """

        return conf_data['account']["user"]['mobile_phone']

    @property
    def user_pwd(self):
        """ 从配置文件中获取user区域中的pwd的值（获取普通用户的账户密码）"""

        return conf_data['account']["user"]['pwd']

    # def replace_data(self, string_data: str):
    #     """
    #     测试数据替换：在源字符串中匹配查找与DataReplace类中属性值一样的字符并进行替换，DateReplace类中不存在的则不进行替换
    #     :param string_data: str类型字符串数据
    #     :return: 返回替换后的结果
    #     """
    #
    #     # 若传递的数据非str类型则将转换为json字符串类型
    #     if not isinstance(string_data, str):
    #         string_data = json.dumps(string_data)
    #
    #     pattern = r'#(.+?)#'
    #
    #     str_data: str = string_data
    #
    #     search_list = list()
    #
    #     # 一次性匹配查到源字符串中所有符合条件的字符并存储到search_list列表中
    #     while re.search(pattern, str_data):
    #
    #         # 查找第一个匹配项作为键值（类属性名）
    #         search_list.append(re.search(pattern, str_data).group(1))
    #
    #         # 将每一次匹配到的字符串替换为空字符（若不进行替换则每次只能匹配同一个字符）
    #         str_data = str_data.replace(f'#{search_list[-1]}#', '', 1)
    #
    #     # 挨个替换能在DataReplace类中匹配到的字符，无法匹配到的则不进行替换
    #     for item in search_list:
    #
    #         # 从Context类的对象中获取key属性的值，若不存在则返回空
    #         value = getattr(self, item, '')
    #
    #         if value:
    #             # 将获取到的value替换相应匹配到的子字符串（注意：每次只替换一次，否则所有以#开头以#结束的子字符串将全部被替换）
    #             # string_data = re.sub(pattern, value, string_data, 1)  # 存在问题：当for循环迭代变量在此类属性中找不到时也被替换成下一个存在的迭代变量对应的属性值
    #             string_data = string_data.replace(f'#{item}#', value, 1)
    #
    #     return string_data

    def replace_data(self, target_string: str, source_string: dict = None):
        """
        测试数据替换： 要替换的数据均是源数据与目标数据中均能查找匹配上的值（任意一方匹配为空时均不进行替换）
        1、从DataReplace类中提取target_string字符串中要进行替换的值，替换target_string字符串中的数据
        2、从source_string字典中提取target_string字符串中要进行替换的值，替换target_string字符串中的数据
        :param source_string: （源）字典
        :param target_string: （目标）字符串：要进行替换的字符串
        :return:
        """

        # 若传递的数据非str类型则将转换为json字符串类型
        if not isinstance(target_string, str):
            target_string = json.dumps(target_string)

        pattern = r'#(.+?)#'

        str_data: str = target_string

        search_list = list()

        # 一次性匹配查到源字符串中所有符合条件的字符并存储到search_list列表中
        while re.search(pattern, str_data):
            # 查找第一个匹配项作为键值（类属性名）
            search_list.append(re.search(pattern, str_data).group(1))

            # 将每一次匹配到的字符串替换为空字符（若不进行替换则每次只能匹配同一个字符）
            str_data = str_data.replace(f'#{search_list[-1]}#', '', 1)

        # 挨个替换能在DataReplace类中匹配到的字符，无法匹配到的则不进行替换
        for item in search_list:

            # 从Context类的对象中获取key属性的值，若不存在则返回空
            if source_string:
                value = jsonpath(source_string, f'$..{item}')
            else:
                value = getattr(self, item, '')

            if value:
                # 将获取到的value替换相应匹配到的子字符串（注意：每次只替换一次，否则所有以#开头以#结束的子字符串将全部被替换）
                # string_data = re.sub(pattern, value, string_data, 1)  # 存在问题：当for循环迭代变量在此类属性中找不到时也被替换成下一个存在的迭代变量对应的属性值
                target_string = target_string.replace(f'#{item}#', value, 1)

        return target_string

    def __make_phone(self):
        """ 生成手机号 """

        fake = Faker(locale='zh_CN')
        phone_number = fake.phone_number()

        return phone_number

    def close_db(self):
        self.db.close()


if __name__ == '__main__':
    from middleware.project_yaml import member_data
    # print(member_data['register'][0]['data'])
    str_data = "ADSFKLJDL #loan_id#"
    con = DataReplace()
    data = con.replace_data(str_data)
    print(data)






