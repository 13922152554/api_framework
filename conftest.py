# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import pytest
from middleware.project_yaml import conf_data
from api.member_api import MemberApi
from common.handle_log import log
from common.handle_mysql import HandleMysql


@pytest.fixture(scope="class")
def conn_db():
    db = HandleMysql(**conf_data['mysql'])
    yield db
    db.close()


@pytest.fixture
def get_login_data():
    login_data = MemberApi().get_login_data()
    yield login_data


@pytest.fixture(scope="class")
def init_account_amount(conn_db):
    """ 将数据库中测试账号余额重置为0.00元 """

    update_sql = f"UPDATE member SET leave_amount=0.00 WHERE mobile_phone={conf_data['account']['user']['mobile_phone']};"
    conn_db.update(update_sql)
    log.info(f"{conf_data['account']['user']['mobile_phone']}账户余额已被重置为0.0元")



