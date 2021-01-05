#!/usr/bin/python
# -*- coding:utf-8 -*-
import MySQLdb


class SqlConn(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def mysql_conn(self):
        try:
            from config.conf import Config
            db_conn_mysql = MySQLdb.connect(host=self.host, port=self.port, user=Config.MYSQL_TB_USER,
                                            passwd=Config.MYSQL_PASSWD,
                                            db=Config.MYSQL_DB, charset=Config.MYSQL_CHARSET)
        except Exception as e:
            print ("MySql数据库连接失败 ,e" % e)
            return None
        finally:
            return db_conn_mysql

