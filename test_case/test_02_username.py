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
data=MiddleHandler.case_path.read_sheet("username")

@ddt.ddt
class TestUsername(unittest.TestCase):
    @ddt.data(*data)
    def test_username(self,test_info):
        data_info=test_info["url"]
        # 替换用例data数据中的#pass_username#
        if "#pass_username#" in data_info:
            db=MySqlHandler()
            pass_username=db.get_db("select username from test.auth_user where id=1;")["username"]
            data_info = data_info.replace("#pass_username#",pass_username)
        # 替换用例data数据中的#username#
        if "#username#" in data_info:
            username=random_handler.RandomHandler().username()
            data_info= data_info.replace("#username#", username[0])

        res=request_handler.request_handler(
            url=yaml["url"] + data_info,
            method=test_info["method"],
        ).text
        # 如果预期结果中有#username#,替换生成的username
        if "#username#" in test_info["excepted"]:
            test_info["excepted"] = test_info["excepted"].replace("#username#", (data_info.split("/"))[2])
        # 如果预期结果中有#pass_username#,替换生成的pass_username
        if "#pass_username#" in test_info["excepted"]:
            test_info["excepted"] = test_info["excepted"].replace("#pass_username#", (data_info.split("/"))[2])
        # 断言
        try:
            for k, v in json.loads(test_info["excepted"]).items():
                # 断言预期结果和实际结果是否一样
                self.assertEqual(v,json.loads(res)[k])
            self.result = "pass"
            logger.info('第{}条用例通过'.format(test_info["case_id"]))
        except AssertionError as e:
            self.result = "fail"
            logger.error('第{}条用例失败,失败原因{}'.format(test_info["case_id"], e))
            raise e
        finally:
            MiddleHandler.case_path.open_excel()
            MiddleHandler.case_path.write_excel(sheet_name="username", row=test_info["case_id"] + 1, colucm=8,
                                                information=self.result)


if __name__ == '__main__':
    pass
