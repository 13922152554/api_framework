# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import os
import pytest
import shutil
from common.handle_path import report_path

# 将上一次的html报告放到history文件中
history_dir = os.path.join(report_path, "history")
html_dir = os.path.join(report_path, "html")
for file in os.listdir(html_dir):
    if file.endswith(".html"):
        # 拼接html报告现在的路径
        now_path = os.path.join(html_dir, file)
        # 拼接html报告要移动到的目标路径
        target_path = os.path.join(history_dir, file)
        # 移动html报告
        shutil.move(now_path, target_path)


if __name__ == "__main__":
    pytest.main(['-s', '-n', 'auto', r"--alluredir=output/report", "--clean-alluredir"])
    os.system('allure generate output/report/ -o output/report/html -c')
