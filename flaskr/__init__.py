from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    """
    创建应用的方法
    :param config_name:
    :return:
    """
    # 初始化应用及配置
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app()

    # 初始化拓展
    db.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
