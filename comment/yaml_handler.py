import yaml
def read_yanl(yaml_path):
    """封装读取yaml格式的函数"""
    with open(yaml_path,encoding="utf-8") as f:
        couf = yaml.load(f,Loader=yaml.SafeLoader)
        return couf


if __name__ == '__main__':
    pass