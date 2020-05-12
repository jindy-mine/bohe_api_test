"""
=========================================
Author:薄咊
Time:2020/4/1  19:41
==========================================
"""

"""
审核的前置条件：
    1、管理员登录；
    2、有待审核的项目：每个审核用例执行之前，去添加一个项目（普通用户需要登陆）
"""
import unittest, jsonpath
from common.handle_Base import HandleBase
from common.handle_config import conf
from common.handle_excel import HandleExcel
from library.myddt import ddt, data
from requests import request
from common.handle_path import CASE_FILENAME
from common.handle_logging import log
from common.handle_data import EnvData, replace_data


@ddt
class TestAudit(unittest.TestCase):
    excel = HandleExcel(CASE_FILENAME, "audit")
    cases = excel.read_data()
    """审核的前置条件"""

    @classmethod
    def setUpClass(cls):
        """该用例类所有用例执行之前的前置条件：管理员要登录，普通用户要登录"""
        # 管理员信息
        admin_phone = 15800000001
        admin_pwd = 12345678
        # 管理员的token
        HandleBase().read_user_info(admin_phone, admin_pwd)
        # 普通用户信息
        phone = 18851288298
        pwd = 12345678
        HandleBase().read_user_info(phone, pwd)

    def setUp(self):
        """每条用例执行之前的前置条件：添加一个新项目"""
        url = conf.get("env", "base_url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData, "token")
        data = {"member_id": getattr(EnvData, "member_id"),
                "title": "薄咊借钱学习",
                "amount": 5000,
                "loan_rate": 12.0,
                "loan_term": 3,
                "loan_date_type": 1,
                "bidding_days": 5}
        # 发送请求，添加项目
        response = request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        print(res)
        # 提取项目的id给审核用例使用
        loan_id = str(jsonpath.jsonpath(res, "$..id")[0])
        setattr(EnvData, "loan_id", loan_id)

    @data(*cases)
    def test_audit(self, case):
        # 1、准备用例数据
        url = conf.get("env", "base_url") + case["url"]
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        # 判读是否需要要替换审核通过的标id
        if "#pass_loan_id#" in case["data"]:
            # 将之前保存的审核通过的id，替换到该用例中
            case["data"] = case["data"].replace("#pass_loan_id#", self.pass_loan_id)

        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        # 准备请求头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData, "admin_token")
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 2、发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果:", res)
        # 判断是否是审核通的用例，并且审核成功
        if case["title"] == "审核通过" and res["msg"] == "OK":
            # 将执行通过的标id保存为类属性
            TestAudit.pass_loan_id = str(data["loan_id"])

        # 3、断言预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
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
