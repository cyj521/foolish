import requests

# 定义一个访问接口的函数
def visit(url,
          method='get',
          params=None,
          data=None,
          json=None,
          **kwargs):
    res=requests.request(method,
                         url,
                         params=params,
                         data=data,
                         json=json,
                         **kwargs)
    # 异常处理,如果返回的是json数据,则返回res.json(),如果不是,抛出异常,返回None
    try:
        return res.json()
    except Exception as e:
        print('返回数据不为json格式:{}'.format(e))
        return None


if __name__ == '__main__':
    pass
