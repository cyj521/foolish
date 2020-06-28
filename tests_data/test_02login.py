import json
import unittest
import ddt
from middle_ware.middle_handler import MiddleHandler
from comment import request_handler

# 获取配置文件的文件名
yaml_data = MiddleHandler.yaml
# 获取log
logger = MiddleHandler.log
# 获取Excel注册页的用例
test_data=MiddleHandler.xls.read_sheet("login")

@ddt.ddt
class TestRegidter(unittest.TestCase):
    @ddt.data(*test_data)
    def test_register(self, test_info):
        print(test_info)
        # 访问接口
        resp = request_handler.visit(
            url=MiddleHandler.yaml["host"]+test_info["url"],
            method=test_info["method"],
            json=json.loads(test_info["data"]),
            headers=json.loads(test_info["headers"])
        )
        # 异常处理,用例通过,记录日志;用例失败,抛出异常,记录日志
        try:
            for k, v in eval(test_info["except"]).items():
                self.assertEqual(v, resp[k])
            # 定义通过的结果
            self.result = "pass"
            # 记录日志
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))

        except Exception as e:
            # 定义失败的结果
            self.result = "fail"
            #记录日志
            logger.error("第{}条用例失败：{}".format(test_info["case_id"],e))
            raise e
        finally:
            MiddleHandler.xls.open_excel()
            MiddleHandler.xls.write_sheet(sheet_name="login", row=test_info["case_id"] + 1, colucm=10,
                                        information=self.result)


if __name__ == '__main__':
    pass

