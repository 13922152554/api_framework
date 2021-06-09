# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import os
# import yaml
import json
from ruamel import yaml
from common.handle_path import conf_path, test_data_path
from common.handle_log import log


class HandleYaml(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def get_yaml_data(self):
        """
        读取yaml文件获取所有数据并返回
        :return: yaml文件中所有数据
        """

        try:
            with open(self.file_name, encoding="utf-8") as f:
                all_data = yaml.safe_load(f)
        except Exception as e:
            log.error(f"yaml文件读取失败，文件名称：{self.file_name}")
            raise e

        return all_data

    def write_data_to_yaml(self, data):
        """
        向yaml写入数据，如果文件不存在则表示可直接写入，若文件存在则表示已追加模式写入则需要先写入空行
        :param data: 要写入的数据（注意：要写入的数据必须是字典且只有一个键值对，且value是str类型）
        :return: None
        """

        with open(self.file_name, mode='w', encoding="utf-8") as f:
            yaml.dump(data=data, stream=f, Dumper=yaml.RoundTripDumper)

    def clear_yaml_data(self):
        """
        清空yaml文件所有数据
        :return: None
        """
        with open(self.file_name, mode='w', encoding="utf-8") as f:
            f.truncate()


conf_data = HandleYaml(os.path.join(conf_path, "conf.yaml")).get_yaml_data()
# member_data = HandleYaml(os.path.join(test_data_path, "member_case_data.yaml")).get_yaml_data()
# a = HandleYaml(os.path.join(conf_path, "res.yaml"))
# res = a.get_yaml_data()


if __name__ == '__main__':
    print(conf_data)
    # conf_data = HandleYaml("replace_data.yaml").get_yaml_data()
    # HandleYaml("replace_data.yaml").write_data_to_yaml({"login": json.dumps(member_data['login'])})
    # print({"login": member_data['login']})
    # a.clear_yaml_data()
    # data = {"enen": '123'}
    # a.write_data_to_yaml(data)
    # print(conf_data)
    # pass

