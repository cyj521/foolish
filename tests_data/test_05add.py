import unittest
import ddt
import json
from comment import request_handler
from middle_ware.middle_handler import MiddleHandler,SqlHandler

# 获取配置文件的文件名
yaml_data=MiddleHandler.yaml
# 获取log
logger=MiddleHandler.log
# 获取excel添加项目页的用例
test_data=MiddleHandler.xls.read_sheet("add")


@ddt.ddt
class TestAdd(unittest.TestCase):

    # 登录
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
    def test_add(self,test_info):
        # 替换用例data列的#member_id#
        data = test_info["data"]
        data = MiddleHandler().replace_data(data)

        # 替换用例headers列的#token#
        headers = test_info["headers"]
        headers = MiddleHandler().replace_data(headers)

        # 添加项目之前查询数据库
        coun = self.db.get_data("select id from futureloan.loan where member_id={};".format(self.member_id),one=False)
        before_count=len(coun)
        # 调用添加接口
        res=request_handler.visit(
            url=MiddleHandler.yaml["host"]+test_info["url"],
            method=test_info["method"],
            headers=json.loads(headers),
            json=json.loads(data)
        )
        # 断言
        try:
            for k, v in eval(test_info["except"]).items():
                self.assertEqual(v, res[k])
                # 判断数据库中是否多一条添加记录
                if res["code"]==0:
                    coun = self.db.get_data("select id from futureloan.loan where member_id={};".format(self.member_id),one=False)
                    after_count = len(coun)
                    self.assertEqual(before_count+1,after_count)
            # 定义用例通过的的结果
            self.result = "pass"
            # 记录log
            logger.info("第{}条用例通过".format(test_info["case_id"]))
        except Exception as e:
            # 定义用例失败的结果
            self.result = "fail"
            # 记录log
            logger.error("第{}条用例失败:{}".format(test_info["case_id"], e))
            # 抛出异常
            raise e
        finally:
            # 最后不管用例是否通过,都写入结果到excel
            MiddleHandler.xls.open_excel()
            MiddleHandler.xls.write_sheet(sheet_name="add", row=test_info["case_id"] + 1, colucm=10,
                                          information=self.result)

