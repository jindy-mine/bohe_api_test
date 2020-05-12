"""
=========================================
Author:薄咊
Time:2020/3/29  23:00
==========================================
"""

import unittest, decimal
from requests import request
from common.handle_excel import HandleExcel
from common.handle_path import CASE_FILENAME
from library.myddt import data, ddt
from common.handle_config import conf
from common.handle_logging import log
from common.handle_dbMysql import HandleMysql
from common.handle_Base import HandleBase
from common.handle_data import EnvData, replace_data


@ddt
class TestWithdraw(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "withdraw")
    cases = excel.read_data()
    db = HandleMysql()

    """提现的前置条件：用户登录,获取登录用户的id和token"""

    @classmethod
    def setUpClass(cls):
        phone = 18851288298
        pwd = 12345678
        HandleBase().read_user_info(phone, pwd)

    @data(*cases)
    def test_withdraw(self, case):
        # 1、准备用例数据
        url = conf.get("env", "base_url") + case["url"]
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        # 准备请求头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData, "token")
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 判断用例是否需要数据库校验，获取提现之前的账户余额
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_money = self.db.find_one_data(sql)["leave_amount"]
            print("提现前得余额：", start_money)

        # 2、发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果:", res)
        # 判断用例是否需要数据库校验，获取提现之后的账户余额
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            end_money = self.db.find_one_data(sql)["leave_amount"]
            print("提现后得余额：", end_money)

        # 3、断言预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要进行sql校验
            if case["check_sql"]:
                # 将提现金额转换为decimal类型（因为数据库中的金额是decimal类型的）
                recharge_money = decimal.Decimal(str(data["amount"]))
                self.assertEqual(recharge_money, start_money - end_money)

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
