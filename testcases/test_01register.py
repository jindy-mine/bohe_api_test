"""
=========================================
Author:薄咊
Time:2020/3/25  18:57
==========================================
"""

import unittest, random
from common.handle_excel import HandleExcel
from library.myddt import data, ddt
from common.handle_config import conf
from requests import request
from common.handle_logging import log
from common.handle_path import CASE_FILENAME
from common.handle_dbMysql import HandleMysql


@ddt
class RegisterTestCase(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "register")
    cases = excel.read_data()
    db =HandleMysql()

    @data(*cases)
    def test_register(self, case):
        # 1、准备用例数据
        # 请求方法
        method = case["method"]
        # 请求地址
        url = case["url"]
        # 请求参数
        # 判断是否有手机号码需要替换
        if "#phone#" in case["data"]:
            # 随机生成一个手机号码
            phone = self.random_phone()
            # 将参数中的#phone#替换成随机生成的手机号码
            case["data"] = case["data"].replace("#phone#",phone)
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 预期结果
        expected = eval(case["expected"])
        # 用例所在行
        row = case["case_id"] + 1
        # 2、发送请求获取实际结果
        response = request(method=method, url=url, json=data, headers=headers)
        # 获取实际结果
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)
        # 3、断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要进行sql校验
            if case["check_sql"]:
                sql = case["check_sql"].replace("#phone#",data["mobile_phone"])
                res = self.db.find_data_count(sql)
                self.assertEqual(1, res)
        except AssertionError as e:
            # 结果回写excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
    @classmethod
    def random_phone(cls):
        """生成一个数据库中未注册的手机号"""
        while True:
            phone = "188"
            for i in range(8):
                r = random.randint(0, 9)
                phone += str(r)
            sql = "select * from futureloan.member WHERE mobile_phone={}".format(phone)
            res =cls.db.find_data_count(sql)
            if res == 0:
                return phone
