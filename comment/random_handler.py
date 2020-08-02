import random
import middle_ware.middle_handler


class RandomHandler:
    def username(self):
        while True:
            # 定义username的取值范围
            username="admin"+random.choice(["1", "2", "3", "4", "5", "6"])
            for i in range(5):
                num=random.randint(1,9)
                username=username+str(num)
            username1=''.join(random.sample("abcdefghijklmnopqrestuvwxyz",20))
            username2 = ''.join(random.sample("abcdefghijklmnopqrestuvwxyz", 6))
            # 查询数据库中是否有这个username
            db=middle_ware.middle_handler.MySqlHandler()
            res=db.get_db("select * from test.auth_user where username='{}';".format(self.username))
            if not res:
                return [username,username1,username2]
            db.close_db()

    def email(self):
        while True:
            # 定义username的取值范围
            email = str(random.choice(["1", "2", "3", "4", "5", "6"]))+"@163.com"
            for i in range(5):
                num = random.randint(1,9)
                email = str(num)+email
            # 查询数据库中是否有这个email
            db = middle_ware.middle_handler.MySqlHandler()
            res = db.get_db("select * from test.auth_user where email='{}';".format(self.email))
            if not res:
                return email
            db.close_db()

    def project_name(self):
        while True:
            # 定义username的取值范围
            project="project"+random.choice(["1", "2", "3", "4", "5", "6"])
            for i in range(3):
                num=random.randint(1,9)
                project=project+str(num)
            project1 = ''.join(random.sample("abcdefghijklmnopqrestuvwxyz1234567890",1))
            project2 = ''.join(random.sample("abcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyz", 200))
            # 查询数据库中是否有这个username
            db=middle_ware.middle_handler.MySqlHandler()
            res=db.get_db("select * from test.tb_projects where name='{}';".format(project))
            if not res:
                return [project,project1,project2]
            db.close_db()

    def interfaces_name(self):
        while True:
            # 定义username的取值范围
            interfaces_name = "interfaces" + random.choice(["1", "2", "3", "4", "5", "6","7","8","9"])
            for i in range(3):
                num = random.randint(1, 9)
                interfaces_name = interfaces_name + str(num)
            interfaces_name1 = ''.join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrestuvwxyz1234567890", 1))
            interfaces_name2 = ''.join(random.sample(
                "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyz",
                200))
            # 查询数据库中是否有这个username
            db = middle_ware.middle_handler.MySqlHandler()
            res = db.get_db("select * from test.tb_interfaces where name='{}';".format(interfaces_name))
            if not res:
                return [interfaces_name, interfaces_name1, interfaces_name2]
            db.close_db()

    def testcase(self):
        while True:
            # 定义username的取值范围
            testcase = "testcase" + random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
            for i in range(3):
                num = random.randint(1, 9)
                testcase = testcase + str(num)
            testcase1 = ''.join(
                random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrestuvwxyz1234567890", 1))
            testcase2 = ''.join(random.sample(
                "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyzabcdefghijklmnopqrestuvwxyz",
                50))
            # 查询数据库中是否有这个username
            db = middle_ware.middle_handler.MySqlHandler()
            res = db.get_db("select * from test.tb_interfaces where name='{}';".format(testcase))
            if not res:
                return [testcase, testcase1, testcase2]
            db.close_db()


if __name__ == '__main__':
    a=RandomHandler()
    username=a.username()
    project=a.project_name()
    email=a.email()
    print(username)
    print(email)
    print(project)
    pass
