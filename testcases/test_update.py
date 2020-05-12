"""
=========================================
Author:薄咊
Time:2020/4/5  12:04
==========================================
"""

import unittest, random
from common.handle_excel import HandleExcel
from common.handle_path import CASE_FILENAME
from common.handle_Base import HandleBase
from library.myddt import data, ddt
from common.handle_config import conf
from requests import request
from common.handle_dbMysql import HandleMysql
from common.handle_logging import log
from common.handle_data import EnvData, replace_data


@ddt
class TestUpdateRegName(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "update")
    cases = excel.read_data()
    db = HandleMysql()

    @classmethod
    def setUpClass(cls):
        phone = 18840468957
        pwd = 12345678
        HandleBase().read_user_info(phone, pwd)

    @data(*cases)
    def test_update_regname(self, case):
        # 1、准备数据
        url = conf.get("env", "base_url") + case["url"]
        # 判断是否有昵称需要替换
        if "#reg_name#" in case["data"]:
            # 随机生成一个昵称
            reg_name = self.random_name()
            # print(reg_name)
            # 将参数中的#reg_name#替换成随机生成的昵称
            case["data"] = replace_data(case["data"])
        # 替换用户id
        data = replace_data(case["data"])
        data = eval(data)
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData, "token")
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 2、发起请求，获取实际结果
        response = request(url=url, method="patch", headers=headers, json=data)
        res = response.json()

        # 3、断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 对需要进行数据库校验的用例进行校验
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                new_regname = self.db.find_one_data(sql)["reg_name"]
                self.assertEqual(reg_name, new_regname)
        except AssertionError as e:
            # 结果写进日志和excel中
            log.error("用例--{}--执行未通过")
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            result = "未通过"
            log.exception(e)
        else:
            log.info("用例--{}--执行通过".format(case["title"]))
            result = "通过"
        finally:
            self.excel.write_data(row=row, column=8, value=result)

    @classmethod
    def random_name(cls):
        """生成一个随机昵称"""
        for i in range(1):
            reg_name = "新昵称"
            r = random.randint(0, 9999999)
            # print(r)
            reg_name += str(r)
            setattr(EnvData, "reg_name", reg_name)
            return reg_name
