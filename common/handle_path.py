# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe
import os

# 项目根目录路径
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志文件路径
log_path = os.path.join(root_path, "output", "log")

# 配置文件路径
conf_path = os.path.join(root_path, "conf")

# 测试案例路径
test_case_path = os.path.join(root_path, "test_case")

# 测试数据文件路径
test_data_path = os.path.join(root_path, "test_datas")

# 测试报告路径
report_path = os.path.join(root_path, "output", "report")



