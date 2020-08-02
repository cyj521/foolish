import requests


def request_handler(
        url=None,
        method="get",
        data=None,
        params=None,
        json=None,
        **kwargs
        ):
    res=requests.request(
        url=url,
        method=method,
        data=data,
        params=params,
        json=json,
        **kwargs
    )
    return res


if __name__ == '__main__':
    res=request_handler(
        url="http://api.keyou.site:8000/user/register/",
        method="post",
        json={"username":"admin","email":"198@163.com","password":"123456","password_confirm":"123456"},
    )
    print(res)
    pass