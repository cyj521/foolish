import yaml
import os
def read_yaml(yami_path):
    with open(yami_path,"r",encoding="utf-8") as f:
        confi=yaml.load(f,Loader=yaml.SafeLoader)
        return confi


if __name__ == '__main__':
    dir_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path=os.path.join(dir_path,"config\config.yaml")
    confi=read_yaml(yaml_path)
    print(confi)
    pass
