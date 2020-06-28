import logging
def log_handeler(
        file_name=None,
        log_name=None,
        log_level="DEBUG",
        stream_level="DEBUG",
        file_level="DEBUG",
        fmt='%(asctime)s--%(filename)s--line:%(lineno)d--%(levelname)s:%(message)s'
):
    """封装日志"""
    # 初始化一个日志接收器
    logger=logging.getLogger(log_name)
    logger.handlers.clear()
    # 设置日志的等级
    logger.setLevel(log_level)
    # 设置日志输出器
    stream_handler=logging.StreamHandler()
    # 设置输出器的级别
    stream_handler.setLevel(stream_level)
    # 把日志接收器和输出器进行关联
    logger.addHandler(stream_handler)
    # 设置日志的格式
    fmt=logging.Formatter(fmt)
    stream_handler.setFormatter(fmt)
    # 输出日志文件

    if file_name:
        # 如果设置的有文件名,则打印日志到txt文件中
        file_handler=logging.FileHandler(file_name,encoding="utf-8")
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)
        file_handler.setFormatter(fmt)
    return logger


if __name__ == '__main__':
    pass
