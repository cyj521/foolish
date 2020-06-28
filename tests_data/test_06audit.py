import unittest
import ddt
import json
from comment import request_handler
from middle_ware.middle_handler import MiddleHandler,SqlHandler
# 获取配置文件的文件名
yaml_data=MiddleHandler.yaml
# 获取log
logger=MiddleHandler.log

# 获取excel审核项目的测试用例
test_data=MiddleHandler.xls.read_sheet("audit")

@ddt.ddt
class TestAudit(unittest.TestCase):

    # 审核前先登录
    @classmethod
    def setUpClass(cls) -> None:
        # 普通会员登录
        cls.member_id=MiddleHandler().member_id
        cls.token=MiddleHandler().token
        # 超管登录
        cls.admin_token=MiddleHandler().admin_token

    def setUp(self) -> None:
        # 连接数据库
        self.db=SqlHandler()
        # 添加项目
        setattr(MiddleHandler,"loan_id",MiddleHandler().add())

    def tearDown(self) -> None:
        self.db.close_db()

    # 审核
    @ddt.data(*test_data)
    def test_audit(self,test_info):

        data=test_info["data"]
        # 替换data列中的#pass_loan_id#
        if "#pass_loan_id#" in data:
            # 在数据库中生成一个不在审核状态的标
            pass_loan_id = self.db.get_data("select * from futureloan.loan where status!=1 limit 1;")
            data=data.replace("#pass_loan_id#",str(pass_loan_id["id"]))
            data = MiddleHandler().replace_data(data)
        else:
            data = MiddleHandler().replace_data(data)
        # 替换headers列中的#admin_token#
        headers=test_info["headers"]
        headers = MiddleHandler().replace_data(headers)


        # 访问接口
        res=request_handler.visit(
            url=MiddleHandler.yaml["host"]+test_info["url"],
            method=test_info["method"],
            headers=eval(headers),
            json=eval(data)
        )
        # 得到预期结果
        expected = json.loads(test_info["except"])
        # 断言,预期结果和实际结果进行对比
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断数据库中是否多一条审核记录
            if res["code"] == 0:
                loan = self.db.get_data("select * from futureloan.loan where id={};".format(MiddleHandler.loan_id))
                self.assertEqual(expected["status"],loan["status"])
            # 定义用例通过的的结果
            self.result="pass"
            # 记录log
            logger.info("第{}条用例通过".format(test_info["case_id"]))

        except Exception as e:
            # 定义用例失败的结果
            self.result="fail"
        # 记录log
            logger.info("第{}条用例失败".format(test_info["case_id"]))
            raise e
        # 最后不管用例是否通过,都写入结果到excel
        finally:
            MiddleHandler.xls.open_excel()
            MiddleHandler.xls.write_sheet(sheet_name="audit", row=test_info["case_id"] + 1, colucm=9,
                                        information=self.result)






