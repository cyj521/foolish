import unittest
import ddt
import json
from comment import request_handler,random_handler
from middle_ware.middle_handler import MiddleHandler,MySqlHandler

# 获取配置文件
yaml=MiddleHandler.yaml
# # 获取log
logger=MiddleHandler.log
# 获取测试数据
data=MiddleHandler.case_path.read_sheet("projects")


@ddt.ddt
class TestProjects(unittest.TestCase):
    # 登录账号
    @classmethod
    def setUpClass(cls) -> None:
        cls.username=MiddleHandler().login()[0]
        cls.token=MiddleHandler().login()[1]

    @ddt.data(*data)
    def test_projects(self,test_info):
        data_info=test_info["data"]
        # 替换data中的#name#
        if "#name#" in data_info:
            name=random_handler.RandomHandler().project_name()
            data_info=data_info.replace("#name#",name[0])
        # 替换data中的#projectname1#
        if "#projectname1#" in data_info:
            name=random_handler.RandomHandler().project_name()
            data_info=data_info.replace("#projectname1#",name[1])
        # 替换data中的#projectname2#
        if "#projectname2#" in data_info:
            name=random_handler.RandomHandler().project_name()
            data_info=data_info.replace("#projectname2#",name[2])
        # 替换data中的#pass_name#
        if "#pass_name#" in data_info:
            name=MySqlHandler().get_db("select name from test.tb_projects where id= 2 limit 1;")["name"]
            data_info=data_info.replace("#pass_name#",name)

        # 替换headers中的#token#
        if "#token#" in test_info["headers"]:
            test_info["headers"]=test_info["headers"].replace("#token#",self.token)
        # 发送请求
        res=request_handler.request_handler(
            url=yaml["url"] + test_info["url"],
            method=test_info["method"],
            headers=json.loads(test_info["headers"]),
            json=json.loads(data_info)
        ).text
        # 替换预期结果中的#id#
        if "#id#" in test_info["excepted"]:
            id=MySqlHandler().get_db("select id from test.tb_projects where name='{}' limit 1;".format(json.loads(data_info)["name"]))
            test_info["excepted"]=test_info["excepted"].replace("#id#",str(id))
        # 替换预期结果中的#name#
        if "#name#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#name#",json.loads(data_info)["name"])
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
            MiddleHandler.case_path.write_excel(sheet_name="projects", row=test_info["case_id"] + 1, colucm=9,
                                                information=self.result)



