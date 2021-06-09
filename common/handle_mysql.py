# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import pymysql
from common.handle_log import log


class HandleMysql:

    def __init__(self, **kwargs):
        """

        :param host: 数据库主机地址
        :param user: 数据库登录用户名
        :param password: 数据库登录密码
        :param port: 数据库端口
        :param database: 数据库名称
        :param charset: 编码格式（若要正常显示中文则使用utf8编码）
        :param kw: 其它参数
        """

        try:
            # 1、建立数据库连接
            self.connect = pymysql.connect(charset='utf8', **kwargs)

            # 2、创建游标(数据库的所有增删改查操作都是针对游标来进行的)
            # pymysql.cursors.DictCursor：指定游标类型为字典类型（使用游标执行sql语句后近回的数据类型）
            self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)
        except Exception:
            log.exception("数据库连接失败！")
            raise

    def get_count(self, sql, args=None):
        """
        获取查询结果的个数
        :param sql: sql语句
        :param args: sql语句中要替换的参数，必须是一个元组或列表
        :return: 返回查询结果的个数
        """
        # 提交（每次提交都会同步更新数据，若上一次查询后中间有更新，提交后则下一次查询到的是最新的数据）
        self.connect.commit()

        return self.cursor.execute(sql, args)

    def query_one(self, sql, args=None) -> dict:
        """
        查询一条语句

        :param sql: sql语句
        :param args: sql语句中要替换的参数，必须是一个元组或列表
        :return: 返回一行数据（返回的数据是字典格式）
        """

        # 提交（每次提交都会同步更新数据，若上一次查询后中间有更新，提交后则下一次查询到的是最新的数据）
        self.connect.commit()

        # 执行sql语句
        self.cursor.execute(sql, args=args)

        # 从执行的结果集中返回第一行数据
        return self.cursor.fetchone()

    def query_all(self, sql, args=None):
        """
        查询所有语句

        :param sql: sql语句
        :param args: sql语句中要替换的参数，必须是一个元组或列表
        :return: 返回多行语句，返回的数据是一个列表嵌套字典格式的数据
        """

        # 提交（每次提交都会同步更新数据，若上一次查询后中间有更新，提交后则下一次查询到的是最新的数据）
        self.connect.commit()

        # 执行sql语句
        self.cursor.execute(sql, args=args)

        # 从执行的结果集中返回所有数据
        return self.cursor.fetchall()

    def update(self, sql, args=None):
        """
        更新数据库
        :param sql: sql语句
        :param args: sql语句中要替换的参数，必须是一个元组或列表
        :return: None
        """

        # 执行sql语句：执行成功则提交，否则将回滚
        try:
            # 执行sql语句
            self.cursor.execute(sql, args=args)
            # 提交到数据库
            self.connect.commit()
        except Exception:
            # 回滚
            self.connect.rollback()

    def close(self):
        """ 关闭游标与连接（必须先关闭游标再关闭连接） """
        self.cursor.close()
        self.connect.close()



