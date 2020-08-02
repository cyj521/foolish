import unittest
import ddt
import json
from comment import request_handler
from middle_ware.middle_handler import MiddleHandler,MySqlHandler

# 获取配置文件
yaml=MiddleHandler.yaml
# # 获取log
logger=MiddleHandler.log
# 获取测试数据
data=MiddleHandler.case_path.read_sheet("login")


@ddt.ddt
class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.username=MiddleHandler().register()

    @ddt.data(*data)
    def test_login(self,test_info):
        data_info=test_info["data"]
        # 替换data中的#username#
        if "#username#" in data_info:
            data_info=data_info.replace("#username#",self.username)
        # 替换data中的#password#
        if "#password#" in data_info:
            data_info=data_info.replace("#password#",yaml["password"])
        # 发送请求
        res=request_handler.request_handler(
            url=yaml["url"]+test_info["url"],
            method=test_info["method"],
            json=json.loads(data_info)
        ).text
        # 如果预期结果中有#id#,查询数据库中的id并替换
        if "#id#" in test_info["excepted"]:
            db = MySqlHandler()
            id = db.get_db("select id from test.auth_user where username='{}';".format(json.loads(data_info)["username"]))["id"]
            test_info["excepted"] = test_info["excepted"].replace("#id#", str(id))

        # 如果预期结果中有#username#,替换data中的username
        if "#username#" in test_info["excepted"]:
            test_info["excepted"] = test_info["excepted"].replace("#username#", json.loads(data_info)["username"])
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
            MiddleHandler.case_path.write_excel(sheet_name="login", row=test_info["case_id"] + 1, colucm=8,
                                                information=self.result)


if __name__ == '__main__':
    pass
