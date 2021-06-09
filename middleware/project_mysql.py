# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

from common.handle_mysql import HandleMysql
from middleware.project_yaml import conf_data


class ProjectMysql(HandleMysql):

    conn_info = conf_data['mysql']

    def __init__(self, **kwargs):
        super().__init__(**conf_data['mysql'], **kwargs)


if __name__ == '__main__':
    db = ProjectMysql()
    sql = "SELECT leave_amount FROM member WHERE mobile_phone=18965655822;"
    print(db.query_one(sql)['leave_amount'])