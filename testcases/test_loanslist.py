"""
=========================================
Author:薄咊
Time:2020/4/5  18:23
==========================================
"""

import unittest
from common.handle_excel import HandleExcel
from common.handle_path import CASE_FILENAME
from library.myddt import data, ddt
from common.handle_config import conf
from requests import request
from common.handle_logging import log
from common.handle_data import replace_data

@ddt
class TestLoansList(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "loans")
    cases = excel.read_data()

    @data(*cases)
    def test_loans_list(self, case):
        # 1、准备用例数据
        url = conf.get("env", "base_url") + case["url"]
        method = case["method"]
        data = eval(replace_data(case["data"]))
        headers = eval(conf.get("env", "headers"))
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 2、发起请求，获取实际结果
        response = request(url=url, method=method, params=data, headers=headers)
        res = response.json()
        print(response.url)
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(res))

        # 3、断言
        try:
            # 校验预期结果与实际结果是否一致
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 断言返回的数据的条数
            self.assertEqual(expected["len"], len(res["data"]))
        except AssertionError as e:
            # 将结果输出到日志和excel中
            log.error("测试用例--{}--未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            result = "未通过"
        else:
            log.info("测试用例--{}--通过".format(case["title"]))
            result = "通过"
        finally:
            self.excel.write_data(row=row, column=8, value=result)
