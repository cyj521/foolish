import unittest
import ddt
import json
from decimal import Decimal
from comment import request_handler
from middle_ware.middle_handler import MiddleHandler,SqlHandler

# 获取配置文件的文件名
yaml_data=MiddleHandler.yaml
# 获取log
logger=MiddleHandler.log
# 获取excel充值页的用例
test_data=MiddleHandler.xls.read_sheet("recharge")

@ddt.ddt
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """登录"""
        cls.token=MiddleHandler().token
        cls.member_id=MiddleHandler().member_id

    def setUp(self) -> None:
        # 连接数据库
        self.db=SqlHandler()

    def tearDown(self) -> None:
        # 断开数据库
        self.db.close_db()

    @ddt.data(*test_data)
    def test_recharge(self,test_info):
        """替换用例数据中的#member_id#"""
        data = test_info["data"]
        data = MiddleHandler().replace_data(data)

        """替换用例headers中的#token#"""
        headers=test_info["headers"]
        headers = MiddleHandler().replace_data(headers)

        # 调用充值接口之前查询数据库中的余额
        money=self.db.get_data("select * from futureloan.member where id={};".format(self.member_id))
        befor_money=money["leave_amount"]

        # 调用充值接口
        data=json.loads(data)
        headers = json.loads(headers)
        res=request_handler.visit(
            method=test_info["method"],
            url=MiddleHandler.yaml["host"]+test_info["url"],
            json=data,
            headers=headers
        )
        # 断言
        try:
            for k, v in eval(test_info["except"]).items():
                self.assertEqual(v, res[k])

            if res["code"]==0:
                # 查询数据库中充值后的金额
                money = self.db.get_data("select * from futureloan.member where id={};".format(self.member_id))
                after_money = money["leave_amount"]
                self.assertTrue(befor_money+Decimal(str(data["amount"]))==after_money)
            # 记录通过的结果
            self.result = "pass"
            # 记录log
            logger.info("第{}条用例通过".format(test_info["case_id"]))

        except Exception as e:
            # 记录失败的结果
            self.result = "fail"
            # 记录log
            logger.error("第{}条用例失败:{}".format(test_info["case_id"], e))
            # 抛出异常
            raise e
        finally:
            MiddleHandler.xls.open_excel()
            MiddleHandler.xls.write_sheet(sheet_name="recharge", row=test_info["case_id"] + 1, colucm=10,
                                          information=self.result)







