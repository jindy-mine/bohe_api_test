"""
=========================================
Author:薄咊
Time:2020/3/27  19:24
==========================================
"""

import pymysql
from common.handle_config import conf


class HandleMysql:

    def __init__(self):
        """
        初始化方法中连接数据库，创建一个游标对象,执行SQL语句
        """
        # 连接数据库
        self.con = pymysql.connect(host=conf.get("mysql", "host"),
                                   port=conf.getint("mysql", "port"),
                                   user=conf.get("mysql", "user"),
                                   password=conf.get("mysql", "password"),
                                   charset="utf8",
                                   # 游标类型改为字典
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        # 创建一个游标对象
        self.cur = self.con.cursor()

    def find_all_data(self, sql):
        """
        查询sql语句返回的所有数据
        :param sql:查询的sql
        :return: 返回查询到的所有数据
        """
        # 执行SQL之前先提交事务
        self.con.commit()
        # 执行sql语句
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one_data(self, sql):
        """
        查询sql语句返回的第一条数据
        :param sql: 查询的sql
        :return: sql语句查询到的第一条数据
        """
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_data_count(self, sql):
        """
        sql语句查询到的数据条数
        :param sql: 查询的sql
        :return:查询到的数据条数
        """
        self.con.commit()
        res_count = self.cur.execute(sql)
        return res_count

    def update_data(self, sql):
        """
        增删改操作的方法
        :param sql: 增删改的sql语句
        :return:
        """
        self.cur.execute(sql)
        self.con.commit()

    def close_con(self):
        """断开游标，关闭连接"""
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    sql = "select * from futureloan.member where mobile_phone='18859298579'"
    # sql = "update futureloan.member set leave_amount = 666 where mobile_phone='13059298579'"
    s=HandleMysql()
    # print("查询所有数据：", s.find_all_data(sql))
    print("查询一条数据：", s.find_one_data(sql))
    # print("查询数据条数：",s.find_data_count(sql))
    # print("更改一条数据：",s.update_data(sql))
