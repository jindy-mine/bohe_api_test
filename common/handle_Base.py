"""
=========================================
Author:薄咊
Time:2020/3/30  15:18
==========================================
"""
import jsonpath
from requests import request
from common.handle_config import conf
from common.handle_data import EnvData, replace_data


class HandleBase:
    """封装一个前置条件的类"""

    @classmethod
    def read_user_info(cls, phone, pwd):
        """用例执行的前置条件：登录"""
        # 准备登录的相关数据
        login_url = conf.get("env", "base_url") + "/member/login"
        login_data = {
            "mobile_phone": phone,
            "pwd": pwd
        }
        login_headers = eval(conf.get("env", "headers"))
        login_response = request(url=login_url, method="post", json=login_data, headers=login_headers)
        login_res = login_response.json()

        # 获取登录用户的id和token,用户类型
        member_id = str(jsonpath.jsonpath(login_res, "$..id")[0])
        token = "Bearer" + " " + jsonpath.jsonpath(login_res, "$..token")[0]
        user_type = jsonpath.jsonpath(login_res, "$..type")[0]
        # 如果登录用户为管理员，存储管理员token
        if user_type == 0:
            setattr(EnvData, "admin_token", token)
        # 提取到的普通用户token类属性
        setattr(EnvData, "member_id", member_id)
        setattr(EnvData, "token", token)

    def add_projcet(self):
        """添加一个项目"""
        url = conf.get("env", "base_url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.token
        data = {"member_id": self.member_id,
                "title": "薄咊借钱嗨",
                "amount": 5000,
                "loan_rate": 12.0,
                "loan_term": 3,
                "loan_data_type": 1,
                "bidding_days": 5}
        # 发送请求，添加项目
        response = request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        # print(res)
        # 提取项目的id给审核用例使用
        loan_id = str(jsonpath.jsonpath(res, "$..id")[0])
        return loan_id


if __name__ == '__main__':
    phone = 18851288298
    pwd = 12345678
    member_id = HandleBase().read_user_info(phone, pwd)[0]
    token = HandleBase().read_user_info(phone, pwd)[1]
    loan_id = HandleBase().add_projcet()
    print("登录用户的id是：", member_id)
    print("登录token是：", token)
    print("loan_id是：", loan_id)
