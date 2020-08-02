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
data=MiddleHandler.case_path.read_sheet("register")


@ddt.ddt
class TestRegister(unittest.TestCase):

    @ddt.data(*data)
    def test_register(self,test_info):
        # 替换用例中data的#username#
        data=test_info["data"]
        if "#username#" in data:
            username=random_handler.RandomHandler().username()
            data=data.replace("#username#",username[0])
        # 替换用例中data的#username1#
        if "#username1#" in data:
            username = random_handler.RandomHandler().username()
            data = data.replace("#username1#", username[1])
        # 替换用例中data的#username1#
        if "#username2#" in data:
            username = random_handler.RandomHandler().username()
            data = data.replace("#username2#", username[2])
        # 替换用例data中的#pass_username#
        # 从数据库中提取一个已存在的用户名
        if "#pass_username#" in data:
            db = MySqlHandler()
            pass_username = db.get_db("select username from test.auth_user where id=1;")["username"]
            data = data.replace("#pass_username#", pass_username)
        # 替换用例中data的#email#
        if "#email#" in data:
            email=random_handler.RandomHandler().email()
            data=data.replace("#email#",email)
        # 替换用例data中的#pass_email#
        # 从数据库中提取一个已存在的用email
        if "#pass_email#" in data:
            db = MySqlHandler()
            pass_email = db.get_db("select email from test.auth_user where id=1;")["email"]
            data = data.replace("#pass_email#", pass_email)

        res=request_handler.request_handler(
            url=yaml["url"]+test_info["url"],
            method=test_info["method"],
            json=json.loads(data)
        ).text
        # 如果预期结果中有#username#,替换生成的username
        if "#username#" in test_info["excepted"]:
            test_info["excepted"]=test_info["excepted"].replace("#username#",json.loads(data)["username"])
        # 如果预期结果中有#id#,查询数据库,替换#id#
            if "#id#" in test_info["excepted"]:
                db=MySqlHandler()
                id=db.get_db("select id from test.auth_user where username='{}';".format(json.loads(data)["username"]))["id"]
                test_info["excepted"] = test_info["excepted"].replace("#id#", str(id))
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
            MiddleHandler.case_path.write_excel(sheet_name="register", row=test_info["case_id"] + 1, colucm=8,
                                                information=self.result)


if __name__ == '__main__':
    pass
