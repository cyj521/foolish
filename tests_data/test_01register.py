import unittest
import ddt
import json
from comment import request_handler
import random
from middle_ware.middle_handler import MiddleHandler,SqlHandler

# 获取配置文件的文件名
yaml_data = MiddleHandler.yaml
# 获取log
logger = MiddleHandler.log
# 获取Excel注册页的用例
test_data=MiddleHandler.xls.read_sheet("register")


@ddt.ddt
class TestRegister(unittest.TestCase):
    @ddt.data(*test_data)
    def test_register(self, test_info):
        # 查询用例中是否有"#phone#",如果有,则用动态生成的手机号替换
        if "#phone#" in test_info["data"]:
            # 调用rand_phone函数获取到动态生成的手机号
            phone=self.rand_phone()
            # 完成替换
            test_info["data"]=test_info["data"].replace("#phone#",phone)
        # 调用request_handler的函数访问接口
        resp = request_handler.visit(
            url=MiddleHandler.yaml["host"]+test_info["url"],
            method=test_info["method"],
            json=json.loads(test_info["data"]),
            headers=json.loads(test_info["headers"]),
        )
        # 异常处理
        try:
            # 循环预期结果的code,msg
            for k, v in json.loads(test_info["except"]).items():
                # 断言预期结果和实际结果的code,msg是否一样
                self.assertEqual(v, resp[k])
            if resp["code"]==0:
                conn=SqlHandler()
                data=conn.get_data("select * from futureloan.member where mobile_phone={};".format(
                    json.loads(test_info["data"])["mobile_phone"]))
                self.assertTrue(data)
            # 记录通过的结果
            self.result="pass"
            # 用例通过,记录日志
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))
        # 用例失败,抛出异常,记录日志
        except Exception as e:
            # 记录失败的结果
            self.result = "fail"
            logger.error("第{}条用例失败：{}".format(test_info["case_id"],e))
            raise e
        finally:
            MiddleHandler.xls.open_excel()
            MiddleHandler.xls.write_sheet(sheet_name="register", row=test_info["case_id"] + 1, colucm=10,
                                          information=self.result)

    # 定义动态生成手机号的函数
    def rand_phone(self):
        # 设置死循环,如果生成的手机号不在数据库中,则退出循环,返回手机号,若存在数据库中,则继续循环,生成手机号
        while True:
            # 定义前两位手机号
            phone = "1" + random.choice(["5", "3"])
            # 定义后面9位手机号
            for i in range(9):
                # 定义手机号的范围为0-9
                num=random.randint(0,9)
                phone = phone + str(num)
            # 连接数据库
            conn = SqlHandler()
            # 查询数据库中是否存在动态生成的手机号
            res=conn.get_data("select * from futureloan.member where mobile_phone={}; ".format(phone))
            # 如果不存在,返回phone
            if not res:
                return phone
            # 查询完关闭数据库
            conn.close_db()


if __name__ == '__main__':
    pass






