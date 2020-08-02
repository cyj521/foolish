import unittest
import ddt
import json
from comment import random_handler,request_handler
from middle_ware.middle_handler import MiddleHandler,MySqlHandler
# 获取配置文件
yaml=MiddleHandler.yaml
# 获取log
logger=MiddleHandler.log
# 获取测试数据
data=MiddleHandler.case_path.read_sheet("testcases")
@ddt.ddt
class TestCase(unittest.TestCase):
    # 先登录
    @classmethod
    def setUpClass(cls) -> None:
        cls.username = MiddleHandler().login()[0]
        cls.token = MiddleHandler().login()[1]

    def setUp(self) -> None:
        # 每次执行用例前新增项目和接口
        setattr(MiddleHandler, "interfaces_data", MiddleHandler().interfaces())

    @ddt.data(*data)
    def test_testcases(self,test_info):
        data_info=test_info["data"]
        # 替换data中的#testcase#
        if "#testcase#" in data_info:
            testcase_name=random_handler.RandomHandler().testcase()[0]
            data_info=data_info.replace("#testcase#",testcase_name)
        # 替换data中的#testcase1#
        if "#testcase1#" in data_info:
            testcase_name1 = random_handler.RandomHandler().testcase()[1]
            data_info = data_info.replace("#testcase1#", testcase_name1)
        # 替换data中的#testcase2#
        if "#testcase2#" in data_info:
            testcase_name2 = random_handler.RandomHandler().testcase()[2]
            data_info = data_info.replace("#testcase2#", testcase_name2)
        # 替换data中的#pass_testcase#
        if "#pass_testcase#" in data_info:
            name=MySqlHandler().get_db("select name from test.tb_testcases where id= 1 limit 1;")["name"]
            data_info=data_info.replace("#pass_testcase#",name)

        # 替换data中的#pid#
        if "#pid#" in data_info:
            data_info=data_info.replace("#pid#",str(MiddleHandler.interfaces_data[2]))

        # 替换data中的#iid#
        if "#iid#" in data_info:
            data_info=data_info.replace("#iid#",str(MiddleHandler.interfaces_data[0]))

        # 替换headers中的#token#
        if "#token#" in test_info["headers"]:
            test_info["headers"] = test_info["headers"].replace("#token#", self.token)
        # 发送请求
        res=request_handler.request_handler(
            url=yaml["url"] + test_info["url"],
            method=test_info["method"],
            headers=json.loads(test_info["headers"]),
            json=json.loads(data_info)
        ).text
        # 替换预期结果中的#case_name#
        if "#case_name#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#case_name#",json.loads(data_info)["name"])
        # 替换预期结果中的#interfaces_name#
        if "#interfaces_name#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#interfaces_name#",MiddleHandler.interfaces_data[1])
        # 替换预期结果中的#project_name#
        if "#project_name#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#project_name#",MiddleHandler.interfaces_data[3])
        # 断言
        try:
            for k, v in json.loads(test_info["excepted"]).items():
                # 断言预期结果和实际结果是否一样
                self.assertEqual(v, json.loads(res)[k])
            self.result = "pass"
            logger.info('第{}条用例通过'.format(test_info["case_id"]))
        except AssertionError as e:
            self.result = "fail"
            logger.error('第{}条用例失败,失败原因{}'.format(test_info["case_id"],e))
            raise e
        finally:
            MiddleHandler.case_path.open_excel()
            MiddleHandler.case_path.write_excel(sheet_name="testcases", row=test_info["case_id"] + 1, colucm=9,
                                                information=self.result)
