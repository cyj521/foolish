##接口文档

##接口概述
主要定义接口的一些通用的规则,是后端工程师指定

##路径问题
-可以放到配置文件,因为项目运行过程当中不会发生变化,但是对于不同的项目有可能会变
-不放到yaml中,放到一个python模块当中

##日期格式和字符串之间的转换strftime()

##请求数据 的格式转换
-headers
-data
-要从Excel读取的字符串转换成字典的形式,用eval

#断言
-全量断言(所有的数据都要进行比对,要一字不差)
-部分断言(挑选出来一部分进行比较,code,msg)

##yaml配置文件
-编写和读取

##登录
-注意登录成功的手机号和密码可以提前准备测试账号
-直接放到excel当中
-放入yaml配置文件,excel数据使用#mobile#,#pwd#

##充值
-需要用到member_id,可以直接放到yaml配置文件
-接口依赖:一个接口的的测试需要另一个接口作为前置条件,充值接口需要登录接口:1.获取token;2.获取member_id
-域名可以放到yaml当中,从yaml中读取,与接口进行拼接

##正则表达式
-通常在匹配方式前加一个r
-正则表达式当中不要随便加空格
-match:在最开始的地方匹配,返回的是字符串
-search:可以在任意地方匹配一次,返回的是字符串,用的最多
find_all:匹配到所有的,得到的值一个列表


