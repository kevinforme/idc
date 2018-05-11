import datetime
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'easy to guess string ? no,no,no.'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    START_TIME = datetime.datetime(2018, 5, 8).timestamp()
    NOW_TIME = datetime.datetime.now().timestamp()
    DURATION = (NOW_TIME - START_TIME) / (60 * 60 * 24)

    @staticmethod
    def init_app():
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://root:qwer@localhost:3306/idc_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://root:qwer@localhost:3306/idc_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://root:qwer@localhost:3306/idc_pro'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
