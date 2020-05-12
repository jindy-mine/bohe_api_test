"""
=========================================
Author:薄咊
Time:2020/3/25  22:50
==========================================
"""

import unittest
import pymysql
from common.handle_excel import HandleExcel
from library.myddt import data, ddt
from common.handle_config import conf
from requests import request
from common.handle_logging import log
from common.handle_path import CASE_FILENAME



@ddt
class LoginTestCase(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "login")
    cases = excel.read_data()

    @data(*cases)
    def test_login(self, case):
        # 1、准备用例数据
        # 请求方法
        method = case["method"]
        # 请求地址
        url = case["url"]
        # 请求参数
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
        except AssertionError as e:
            # 记录日志
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            result = "未通过"
            log.exception(e)
            raise e
        else:
            log.info("用例--{}--执行通过".format(case["title"]))
            result = "通过"
        finally:
            # 结果回写excel中
            self.excel.write_data(row=row, column=8, value=result)
