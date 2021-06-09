# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import os
import json
from ruamel import yaml
from common.handle_yaml import HandleYaml
from common.handle_path import conf_path, test_data_path
from common.handle_log import log


class ProjectYaml(HandleYaml):

    def __init__(self, file_name):
        super().__init__(file_name)


conf_data = ProjectYaml(os.path.join(conf_path, "conf.yaml")).get_yaml_data()
member_data = ProjectYaml(os.path.join(test_data_path, "member_case_data.yaml")).get_yaml_data()
loan_data = ProjectYaml(os.path.join(test_data_path, "loan_case_data.yaml")).get_yaml_data()
res_yaml = ProjectYaml(os.path.join(conf_path, "res.yaml"))

if __name__ == '__main__':
    print(res_yaml)
    # conf_data = HandleYaml(os.path.join(conf_path, "res.yaml")).get_yaml_data()
    # write_yaml.write_data_to_yaml({"name": 1111})
    # print({"login": member_data['login']})
    # print(conf_data)
    # pass

