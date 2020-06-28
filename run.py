"""运行所有的用例"""
import unittest
import os
from config import config
from libs.HTMLTestRunnerNew import HTMLTestRunner
from datetime import  datetime
# 初始化加载用例
loader=unittest.TestLoader()
# 得到测试用例集
suites=loader.discover(config.CASE_PATH)

# 设置测试报告的名称
ts=datetime.now().strftime("%y-%m-%d-%H-%M-%S")
reports_filename="reports-{}.html".format(ts)

# 指定测试报告的路径
reports_file=os.path.join(config.REPORTS_PATH,reports_filename)


#  运行器,运行测试用例
with open(reports_file,mode="wb") as f:
    runner=HTMLTestRunner(f,
                          title="前程贷测试报告",
                          description="测试报告",
                          tester="艳杰"
                          )
    runner.run(suites)



