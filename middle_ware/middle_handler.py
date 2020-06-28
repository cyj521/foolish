import os
import re
from pymysql.cursors import DictCursor
from comment import yaml_handler,ecxel_handler,log_handler,mysql_handler,request_handler
from config import config
import jsonpath

class MiddleHandler:
    loan_id=None

    # 使用变量接收config对象
    conf = config

    # 获取yaml配置文件
    yaml=yaml_handler.read_yanl(os.path.join(config.CONFIG_PATH,"config.yml"))

    # 获取Excel
    # 先获取excel的名字
    case_file=yaml["excel"]["file"]
    # 再获取Excel的路径
    xls=ecxel_handler.ExcelHandler(os.path.join(config.DATA_PATH,case_file))

    # 获取log
    log=log_handler.log_handeler(
        file_name=os.path.join(config.LOG_PATH,yaml["log"]["file_name"]),
        log_name=yaml["log"]["log_name"],
        log_level=yaml["log"]["log_level"],
        stream_level=yaml["log"]["stream_level"],
        file_level=yaml["log"]["file_level"],
        fmt='%(asctime)s--%(filename)s--line:%(lineno)d--%(levelname)s:%(message)s'
    )

    @property
    def token(self):
        return self.login(self.yaml["user"])["token"]

    @property
    def member_id(self):
        return self.login(self.yaml["user"])["member_id"]

    @property
    def invest_member_id(self):
        return self.login(self.yaml["invest_user"])["member_id"]

    @property
    def invest_token(self):
        return self.login(self.yaml["invest_user"])["token"]

    @property
    def admin_token(self):
        return self.login(self.yaml["admin_user"])["token"]

    def login(self,user):
        # 封装登录函数
        res = request_handler.visit(
            url=MiddleHandler.yaml["host"] + "/member/login",
            method="post",
            headers={"X-Lemonban-Media-Type": "lemonban.v2"},
            json=user
        )
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        token_msg = jsonpath.jsonpath(res, "$..token")[0]
        member_id = jsonpath.jsonpath(res, "$..id")[0]
        token = " ".join([token_type, token_msg])
        return {"member_id": member_id, "token": token}

    def add(self):
        # 封装添加项目函数
        data_res={"member_id": self.member_id,
              "title":"借钱买股票",
              "amount":10000,
              "loan_rate":18.0,
              "loan_term":6,
              "loan_date_type":1,
              "bidding_days":8
              }
        res = request_handler.visit(
            url=MiddleHandler.yaml["host"] + "/loan/add",
            method="post",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data_res
        )
        return res["data"]["id"]

    # 封装审核函数
    def audit(self):
        audit_data={
            "loan_id": self.loan_id,
            "approved_or_not": True
        }
        res=request_handler.visit(
            url=MiddleHandler.yaml["host"]+"/loan/audit",
            method="patch",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.admin_token},
            json=audit_data
        )
        # return self.loan_id

    # 封装充值函数
    def recharge(self):
        recharge_data={"member_id":self.member_id,"amount":500000}
        res=request_handler.visit(
            url=MiddleHandler.yaml["host"]+"/member/recharge",
            method="post",
            headers={"X-Lemonban-Media-Type":"lemonban.v2","Authorization":self.token},
            json=recharge_data
        )

    # 替换用例里面的#..#
    def replace_data(self,data):
        patten=r"#(.*?)#"
        while re.search(patten,data):
            # 得到括号里面的内容
            key=re.search(patten,data).group(1)
            # 得到#(.*?)#的值,self.key,调用MiddleHandler中的属性,没有匹配到的给个默认空值
            value=getattr(self,key,"")
            data=re.sub(patten,str(value),data,1)
        return data




class SqlHandler(mysql_handler.MysqlHandler):
    # 连接数据库
    def __init__(self):
        # 从yaml文件中读取到数据库db的配置项
        db_config = MiddleHandler.yaml["db"]
        # 子类继承父类的方法
        super().__init__(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            charset= db_config["charset"],
            database=db_config["database"],
            cursorclass=DictCursor
        )







if __name__ == '__main__':
    loan_id=MiddleHandler.loan_id
    status=MiddleHandler.status

    pass

