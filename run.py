# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import os
import pytest


if __name__ == "__main__":
    pytest.main(['-s', r"--alluredir=output/report", "--clean-alluredir"])
    os.system('allure generate output/report/ -o output/report/html -c')
