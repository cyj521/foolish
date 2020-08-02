import pymysql
from pymysql.cursors import DictCursor


class MySqlHandler:
    def __init__(self,
                 host=None,
                 port=13306,
                 user=None,
                 password=None,
                 charset="utf8",
                 database="futureloan",
                 cursorclass=DictCursor
                 ):
        # 连接数据库
        self.conn=pymysql.connect(
            host=host,
            port=port ,
            user=user,
            password=password,
            charset=charset,
            database=database,
            cursorclass=cursorclass
        )
        # 初始化游标
        self.course=self.conn.cursor()
    # 查询数据库

    def get_db(self,sql,one=True):
        # 提交事务
        self.conn.commit()
        # 查询数据库
        self.course.execute(sql)
        if one:
            return self.course.fetchone()
        return self.course.fetchall()
    # 关闭数据库

    def close_db(self):
        # 关闭游标对象
        self.course.close()
        # 关闭数据库连接
        self.conn.close()


if __name__ == '__main__':

    db=MySqlHandler(host="www.keyou.site",
                    port=13306,
                    user="lemon520",
                    password="123456",
                    charset="utf8",
                    database="test",
                    cursorclass=DictCursor)
    db_data=db.get_db("select * from test.auth_user where id=1;")
    pass