"""
=========================================
Author:薄咊
Time:2020/3/25  23:37
==========================================
"""
import os, datetime

# 获取项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用例模块所在的目录路径
CASE_DIR = os.path.join(BASE_DIR, "testcases")

# 用例数据所在的目录路径
DATA_DIR = os.path.join(BASE_DIR, "data")
CASE_FILENAME = os.path.join(DATA_DIR, "cases.xlsx")

# 配置文件所在的目录路径
CONF_DIR = os.path.join(BASE_DIR, "conf")
CONF_FILENAME = os.path.join(CONF_DIR, "config.ini")
# 测试报告所在的目录路径
s = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
REPORT_FILENAME = os.path.join(REPORT_DIR, "report.html")
# REPORT_FILENAME = os.path.join(REPORT_DIR, "report" + s + ".html")

# 日志文件的绝对路径
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILENAME = os.path.join(LOG_DIR, "test.log")
