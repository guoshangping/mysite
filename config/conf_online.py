#!/usr/bin/python
# -*- coding:utf-8 -*-


from __future__ import unicode_literals
from tools.pm_sqlconn import SqlConn


class Config(object):
    """
        配置文件类
    """
    CONFIG_NAME = "conf_offline"

    """---------------mysql数据库------------------"""
    # mysql (91 端口)
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    # 用户名
    MYSQL_TB_USER = "root"
    MYSQL_PASSWD = "qwer1234"
    # 数据库
    MYSQL_DB = "mysite"
    MYSQL_CHARSET = "utf8"
    MYSQL_CONN_OBJ = SqlConn(host=MYSQL_HOST, port=MYSQL_PORT)
