"""
=========================================
Author:薄咊
Time:2020/4/1  18:54
==========================================
"""

import unittest
from common.handle_excel import HandleExcel
from common.handle_path import CASE_FILENAME
from common.handle_Base import HandleBase
from library.myddt import data, ddt
from common.handle_config import conf
from requests import request
from common.handle_logging import log
from common.handle_dbMysql import HandleMysql
from common.handle_data import EnvData,replace_data

@ddt
class testAdd(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "add")
    cases = excel.read_data()
    db = HandleMysql()

    """添加项目的前置条件：用户登录,获取登录用户的id和token"""

    @classmethod
    def setUpClass(cls):
        phone = 18851288298
        pwd = 12345678
        HandleBase().read_user_info(phone, pwd)

    @data(*cases)
    def test_add(self, case):
        # 1、准备用例数据
        url = conf.get("env", "base_url") + case["url"]
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        # 准备请求头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData,"token")
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 加标之前，查询数据库中该用户标的数量
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_count = self.db.find_data_count(sql)

        # 2、发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果:", res)

        # 3、断言预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要进行sql校验
            if case["check_sql"]:
                # 加标之后
                sql = replace_data(case["check_sql"])
                end_count = self.db.find_data_count(sql)
                self.assertEqual(1, end_count - start_count)
        except AssertionError as e:
            # 将结果写入日志中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            result = "未通过"
            raise e
        else:
            # 结果写到日志
            log.info("用例--{}--执行通过".format(case["title"]))
            result = "通过"
        finally:
            # 将结果写入到excel中
            self.excel.write_data(row=row, column=8, value=result)
