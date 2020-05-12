"""
=========================================
Author:薄咊
Time:2020/4/5  16:48
==========================================
"""

import unittest,jsonpath
from common.handle_excel import HandleExcel
from common.handle_path import CASE_FILENAME
from common.handle_config import conf
from library.myddt import data, ddt
from common.handle_Base import HandleBase
from requests import request
from common.handle_logging import log
from common.handle_data import replace_data,EnvData


@ddt
class TestFindUserInfo(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "info")
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls):
        """前置条件：用户登录"""
        phone = 18840468957
        pwd = 12345678
        HandleBase().read_user_info(phone, pwd)
    @data(*cases)
    def test_find_userinfo(self, case):
        # 1、准备请求参数
        # 替换url中的会员id
        url = conf.get("env", "base_url") + replace_data(case["url"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData,"token")
        method = case["method"]
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 2、发起请求，获取实际结果
        response = request(url=url, method=method, headers=headers)
        res = response.json()
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(res))

        # 3、断言
        try:
            # 断言预期结果与实际结果是否一致
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
        except AssertionError as e:
            # 将结果写入日志文件和excel中
            log.error("测试用例--{}--未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            result = "未通过"
            raise e
        else:
            log.info("测试用例--{}--通过".format(case["title"]))
            result = "通过"
        finally:
            self.excel.write_data(row=row,column=8,value=result)


