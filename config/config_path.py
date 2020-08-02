import os
# 获取配置文件的路径
CONFIG_PATH=os.path.dirname(os.path.abspath(__file__))

# 获取整个项目的路径
ROOT_PATH=os.path.dirname(CONFIG_PATH)

# 获取用例路径
CASE_PATH=os.path.join(ROOT_PATH,"test_data")

# 获取测试数据的路径
CASE_DATA=os.path.join(ROOT_PATH,"test_case")

# 获取log路径
LOG_PATH=os.path.join(ROOT_PATH,"logs")

# 获取report的路径
REPORT_PATH=os.path.join(ROOT_PATH,"report")
