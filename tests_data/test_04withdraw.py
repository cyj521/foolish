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
test_data=MiddleHandler.xls.read_sheet("withdraw")

@ddt.ddt
class TestWithdraw(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.member_id=MiddleHandler().member_id
        cls.token=MiddleHandler().token
    # 连接数据库

    def setUp(self) -> None:
        self.db=SqlHandler()
    # 关闭数据库

    def tearDown(self) -> None:
        self.db.close_db()



    @ddt.data(*test_data)
    def test_withdraw(self,test_info):

        # 替换用例data列的#member_id#
        data=test_info["data"]
        data = MiddleHandler().replace_data(data)

        # 替换用例headers列的#token#
        headers=test_info["headers"]
        headers = MiddleHandler().replace_data(headers)

        # 调用提现之前先查询数据库中的余额
        money=self.db.get_data("select leave_amount from futureloan.member where id={};".format(self.member_id))
        before_money=money["leave_amount"]
        # 调用提现接口

        data = json.loads(data)
        headers = json.loads(headers)
        res=request_handler.visit(
            url=MiddleHandler.yaml["host"]+test_info["url"],
            method=test_info["method"],
            headers=headers,
            json=data
        )

        # 断言
        try:
            for k, v in eval(test_info["except"]).items():
                self.assertEqual(v, res[k])
            if res["code"] == 0:
                # 查询数据库中提现后的金额
                money = self.db.get_data("select * from futureloan.member where id={};".format(self.member_id))
                after_money=money["leave_amount"]
                self.assertTrue(after_money + Decimal(str(data["amount"])) == before_money)
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
            MiddleHandler.xls.write_sheet(sheet_name="withdraw", row=test_info["case_id"] + 1, colucm=10,
                                          information=self.result)









