import unittest
from datetime import datetime
import os
from HTMLTestRunnerNew import HTMLTestRunner
from config import config_path
# 初始化一个用例加载器
loader=unittest.TestLoader()
# 得到测试用例集
suites=loader.discover(config_path.CASE_DATA)
# 设置测试报告的名称
ts=datetime.now().strftime("%y-%m-%d-%H-%M-%S")
reports_filename="reports-{}.html".format(ts)
# 指定测试报告的路径
report_path=os.path.join(config_path.REPORT_PATH,reports_filename)
# 运行测试用例,生成报告
with open(report_path,mode="wb") as f:
    runner = HTMLTestRunner(f,
                            title="测开平台测试报告",
                            description="这是测试报告",
                            tester="天空"
                            )
    runner.run(suites)
