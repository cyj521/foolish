import logging


def log_handler(
        file_name=None,
        log_name=None,
        log_level="DEBUG",
        stream_level="DEBUG",
        file_level="DEBUG",
        fmt='%(asctime)s--%(filename)s--line:%(lineno)d--%(levelname)s:%(message)s'
):
    # 初始化一个log加载器
    logger=logging.getLogger(log_name)
    logger.handlers.clear()
    # 设置log的等级
    logger.setLevel(log_level)
    # 设置日志输出器
    stream_handler=logging.StreamHandler()
    # 设置日志输出器的等级
    stream_handler.setLevel(stream_level)
    # 把log加载器和日志输出器进行关联
    logger.addHandler(stream_handler)
    # 设置日志的格式
    fmt=logging.Formatter(fmt)
    stream_handler.setFormatter(fmt)
    if file_name:
        # 如果设置的有文件名,则打印日志到txt文件中
        file_handler = logging.FileHandler(file_name, encoding="utf-8")
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)
        file_handler.setFormatter(fmt)
    return logger


if __name__ == '__main__':
    pass



