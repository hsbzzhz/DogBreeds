import os


class BaseConfig(object):
    """Base Configuration"""

    # 工程根路径
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))

    # 日志文件
    LOGGING_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "logs"))


class DBConfig(object):
    """db info"""
    SECRET_KEY = '123456'
    DATABASE_URI = 'mysql://user:password@localhost/demodatabase'
