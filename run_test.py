"""
=========================================
Author:薄咊
Time:2020/3/18  20:08
==========================================
"""

import unittest, datetime
from library.HTMLTestRunnerNew import HTMLTestRunner
from BeautifulReport import BeautifulReport
from common.handle_logging import log
from common.handle_path import CASE_DIR, REPORT_DIR, REPORT_FILENAME
from testcases import test_loanslist
log.info("--------------------测试用例开始执行--------------------")
# 创建测试套件
suite = unittest.TestSuite()

# 加载用例到套件
loader = unittest.TestLoader()
# 执行所有测试用例类
suite.addTest(loader.discover(CASE_DIR))
# 执行单个测试用例模块
# suite.addTest(loader.loadTestsFromModule(test_loanslist))

# 执行用例生成报告
# bf = BeautifulReport(suite)
# s = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
# bf.report("接口测试报告", filename="FutureloanTestReport" + s + ".html", report_dir=REPORT_DIR)

runner = HTMLTestRunner(stream=open(REPORT_FILENAME, "wb"),
                        title="接口测试报告",
                        tester="bohe",
                        description="前程贷接口测试"
                        )
runner.run(suite)

log.info("--------------------测试用例执行结束--------------------")

