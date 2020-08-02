import unittest
import ddt
import json
from comment import request_handler,random_handler
from middle_ware.middle_handler import MySqlHandler,MiddleHandler

# 获取配置文件
yaml=MiddleHandler.yaml
# 获取log
logger=MiddleHandler.log
# 获取测试数据
data=MiddleHandler.case_path.read_sheet("interfaces")


@ddt.ddt
class TestInterfaces(unittest.TestCase):
    # 先登录
    @classmethod
    def setUpClass(cls) -> None:
        cls.username = MiddleHandler().login()[0]
        cls.token = MiddleHandler().login()[1]
    # 每次添加接口前都添加一个项目
    def setUp(self) -> None:
        # self.project_id=MiddleHandler().projects()
        # self.project_name=MiddleHandler().projects()[1]
        setattr(MiddleHandler,"project_data",MiddleHandler().projects())

    @ddt.data(*data)
    def test_interfaces(self,test_info):
        data_info=test_info["data"]
        # 替换data中的#interfaces_name#
        if "#interfaces_name#" in data_info:
            interfaces_name=random_handler.RandomHandler().interfaces_name()[0]
            data_info=data_info.replace("#interfaces_name#",interfaces_name)
        # 替换data中的#interfaces_name#
        if "#interfaces_name1#" in data_info:
            interfaces_name1=random_handler.RandomHandler().interfaces_name()[1]
            data_info=data_info.replace("#interfaces_name1#",interfaces_name1)
        # 替换data中的#interfaces_name#
        if "#interfaces_name2#" in data_info:
            interfaces_name2=random_handler.RandomHandler().interfaces_name()[2]
            data_info=data_info.replace("#interfaces_name2#",interfaces_name2)

        # 替换data中的#pass_interfaces_name#
        if "#pass_interfaces_name#" in data_info:
            name=MySqlHandler().get_db("select name from test.tb_interfaces where id= 1 limit 1;")["name"]
            data_info=data_info.replace("#pass_interfaces_name#",name)

        # 替换data中的#project_id#
        if "#project_id#" in data_info:
            data_info=data_info.replace("#project_id#",str((MiddleHandler.project_data)[0]))
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
        # 替换预期结果中的#interfaces_name#
        if "#interfaces_name#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#interfaces_name#",json.loads(data_info)["name"])
        # 替换预期结果中的#project_id#
        if "#project_id#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#project_id#",str((MiddleHandler.project_data)[0]))
        # 替换预期结果中的"#project_name#"
        if "#project_name#" in test_info["excepted"]:
            test_info["excepted"] = test_info["excepted"].replace("#project_name#",(MiddleHandler.project_data)[1])
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
            MiddleHandler.case_path.write_excel(sheet_name="interfaces", row=test_info["case_id"] + 1, colucm=9,
                                                information=self.result)
