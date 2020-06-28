import pymysql
from pymysql.cursors import DictCursor


class MysqlHandler:
    def __init__(self,
                 host = None,
                 port = 3306,
                 user = None,
                 password = None,
                 charset = "utf8",
                 database = "futureloan",
                 cursorclass = DictCursor
                 ):
        # 连接数据库
        self.conn=pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            database=database,
            cursorclass=cursorclass
        )
        # 初始化游标
        self.course=self.conn.cursor()

    def get_data(self,sql,one=True):
        # 提交事务,更新数据库
        self.conn.commit()
        # 获取数据
        self.course.execute(sql)
        if one:
            return self.course.fetchone()
        return self.course.fetchall()

    def close_db(self):
        # 关闭连接
        self.course.close()
        self.conn.close()


if __name__ == '__main__':
    pass


