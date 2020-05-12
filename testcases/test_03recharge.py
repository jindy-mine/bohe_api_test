"""
=========================================
Author:薄咊
Time:2020/3/29  19:41
==========================================
"""

import unittest
import decimal
from library.myddt import data, ddt
from common.handle_excel import HandleExcel
from common.handle_path import CASE_FILENAME
from common.handle_config import conf
from common.handle_logging import log
from requests import request
from common.handle_dbMysql import HandleMysql
from common.handle_Base import HandleBase
from common.handle_data import EnvData,replace_data

@ddt
class TestRecharge(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "recharge")
    cases = excel.read_data()
    db = HandleMysql()
    """充值的前置条件：用户登录,获取登录用户的id和token"""

    @classmethod
    def setUpClass(cls):
        phone = 18851288298
        pwd = 12345678
        HandleBase().read_user_info(phone, pwd)

    @data(*cases)
    def test_recharge(self, case):
        # 1、准备用例数据
        url = conf.get("env", "base_url") + case["url"]
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        case["data"] = replace_data(case["data"])
        # 转换为字典
        data = eval(case["data"])
        # 准备请求头
        headers = eval(conf.get("env", "headers"))
        # 请求头中加入token:往字典中添加键值对
        headers["Authorization"] = getattr(EnvData,"token")
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 判断用例是否需要数据库校验，获取充值之前的账户余额
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_money = self.db.find_one_data(sql)["leave_amount"]
            print("充值之前的金额：", start_money)
        # 2、发送请求，获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        # 判断用例是否需要数据库校验，获取充值之后的账户余额
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            end_money = self.db.find_one_data(sql)["leave_amount"]
            print("充值之后的金额：", end_money)

        # 3、断言预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要进行sql校验
            if case["check_sql"]:
                # 将充值金额转换为decimal类型（因为数据库中的金额是decimal类型的）
                recharge_money = decimal.Decimal(str(data["amount"]))
                self.assertEqual(recharge_money, end_money - start_money)
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
