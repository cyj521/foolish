import os
import json
from config import config_path
from comment import excel_handler,log_handler,random_handler,request_handler,yaml_handler,sql_handler
from pymysql.cursors import DictCursor


class MiddleHandler:
    # 给添加项目的id和project_name一个空值,以便添加接口的时候不会重复调用
    project_data=None
    interfaces_data=None
    # 把配置文件赋值给变量
    config=config_path

    # 获取yaml配置文件
    yaml=yaml_handler.read_yaml(os.path.join(config.CONFIG_PATH,"config.yaml"))

    # 获取测试用例的路径
    case_file=yaml["case"]["case_file"]
    case_path=excel_handler.ExcelHandler(os.path.join(config.CASE_PATH,case_file))

    # 获取log
    log=log_handler.log_handler(
        file_name=os.path.join(config.LOG_PATH,yaml["log"]["file_name"]),
        log_name="my_log",
        log_level="DEBUG",
        stream_level="DEBUG",
        file_level="DEBUG",
        fmt="%(asctime)s--%(filename)s--line:%(lineno)d--%(levelname)s:%(message)s"
    )

    # 封装注册函数
    def register(self):
        username=(random_handler.RandomHandler().username())[0]
        email=random_handler.RandomHandler().email()
        data={
            "username":username,
            "email":email,
            "password":"123456",
            "password_confirm":"123456"
            }
        res=request_handler.request_handler(
            url=MiddleHandler.yaml["url"] + "/user/register/",
            method="post",
            json=data
        ).text
        return json.loads(res)["username"]

    # 封装登录函数
    def login(self):
        username=self.register()
        data = {
            "username": username,
            "password": "123456",
        }
        res=request_handler.request_handler(
            url=MiddleHandler.yaml["url"] + "/user/login/",
            method="post",
            json=data
        ).text
        username=json.loads(res)["username"]
        token_data=json.loads(res)["token"]
        token=" ".join(["JWT",token_data])
        return [username,token]

    # 封装添加项目函数
    def projects(self):
        name = (random_handler.RandomHandler().project_name())[0]
        data={
            "name": name,
            "leader": "天空",
            "tester": "sky",
            "programmer": "haha",
            "publish_app": "天空是富婆",
            "desc": "当我的笑灿烂像阳光"
        }
        res=request_handler.request_handler(
            url=MiddleHandler.yaml["url"] + "/projects/",
            method="post",
            headers={"Authorization":self.login()[1]},
            json=data
        ).text
        project_id=json.loads(res)["id"]
        project_name=json.loads(res)["name"]
        return [project_id,project_name]

    def interfaces(self):
        interfaces_name = (random_handler.RandomHandler().interfaces_name())[0]
        project=self.projects()
        project_id=project[0]
        project_name=project[1]
        interfaces_data = {
            "name":interfaces_name,
            "tester":"天空",
            "project_id":project_id,
            "desc":"这是一个接口"
        }
        interfaces_res = request_handler.request_handler(
            url=MiddleHandler.yaml["url"] + "/interfaces/",
            method="post",
            headers={"Authorization": self.login()[1]},
            json=interfaces_data
        ).text
        interfaces_id = json.loads(interfaces_res)["id"]
        interfaces_name = json.loads(interfaces_res)["name"]
        return [interfaces_id,interfaces_name,project_id,project_name]

    def replace_data(self,data):
        import re
        patten=r"#(.+?)#"
        while re.search(patten,data):
            key=re.search(patten,data,1).group(1)
            value=getattr(self,key,"")
            data=re.sub(patten,str(value),data,1)
            return data


class MySqlHandler(sql_handler.MySqlHandler):
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
                charset=db_config["charset"],
                database=db_config["database"],
                cursorclass=DictCursor
            )


if __name__ == '__main__':
    a=MiddleHandler().interfaces()
    print(a)
    pass
