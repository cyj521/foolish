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
# 获取excel投资的测试用例
test_data=MiddleHandler.xls.read_sheet("invest")


@ddt.ddt
class TestInvest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.invest_member_id=MiddleHandler().invest_member_id
        cls.invest_token=MiddleHandler().invest_token

    def setUp(self) -> None:
        self.db=SqlHandler()
        # 动态获取loan_id的值,调用add方法,把返回的loan_id赋值给MiddleHandler.loan_id
        setattr(MiddleHandler,"loan_id",MiddleHandler().add())
        MiddleHandler().audit()
        MiddleHandler().recharge()

    def tearDown(self) -> None:
        self.db.close_db()

    @ddt.data(*test_data)
    def test_invest(self,test_info):

        data = test_info["data"]
        # 在数据库中找到一个不在已审核状态的标
        pass_loan_id=self.db.get_data("select * from futureloan.loan where status!=2 limit 1;")
        if "#1_loan_id#" in data:
            data=data.replace("#1_loan_id#",str(pass_loan_id["id"]))
            data = MiddleHandler().replace_data(data)
        else:
            data=MiddleHandler().replace_data(data)
        headers=test_info["headers"]
        headers=MiddleHandler().replace_data(headers)

        # 发送投资请求之前先查询数据库中总的投资记录
        before_count=self.db.get_data("select id from futureloan.invest where member_id={};".format(self.invest_member_id),one=False)
        # 发送投资请求之前查询账户所剩资金
        money=self.db.get_data("select * from futureloan.member where id={};".format(self.invest_member_id))
        before_money=money["leave_amount"]

        # 调用接口
        res=request_handler.visit(
            url=MiddleHandler.yaml["host"]+test_info["url"],
            method=test_info["method"],
            headers=json.loads(headers),
            json=json.loads(data)
        )
        excepted=json.loads(test_info["except"])
        # 断言
        try:
            self.assertEqual(excepted["code"],res["code"])
            self.assertEqual(excepted["msg"], res["msg"])
            if res["code"]==0:
                if "status" in res:
                    loan = self.db.get_data("select * from futureloan.loan where id={};".format(MiddleHandler.loan_id))
                    self.assertEqual(excepted["status"], loan["status"])
                else:
                    # 断言用户余额是否减少
                    amount=eval(data)["amount"]
                    money = self.db.get_data("select * from futureloan.member where id={};".format(self.invest_member_id))
                    after_money = money["leave_amount"]
                    self.assertEqual(after_money+Decimal(str(amount)),before_money)
                    # 断言投资表中新增一条记录
                    after_count = self.db.get_data("select id from futureloan.invest where member_id={};".format(self.invest_member_id), one=False)
                    self.assertEqual(len(before_count)+1,len(after_count))
            # 定义用例通过的的结果
            self.result = "pass"
            # 记录log
            logger.info("第{}条用例通过".format(test_info["case_id"]))
        except Exception as e:
            # 定义用例失败的结果
            logger.info("正在写入fail")
            # 记录log
            logger.info("第{}条用例失败".format(test_info["case_id"]))
            raise e
            # 最后不管用例是否通过,都写入结果到excel
        finally:
            MiddleHandler.xls.open_excel()
            MiddleHandler.xls.write_sheet(sheet_name="invest", row=test_info["case_id"] + 1, colucm=9,
                                          information=self.result)
