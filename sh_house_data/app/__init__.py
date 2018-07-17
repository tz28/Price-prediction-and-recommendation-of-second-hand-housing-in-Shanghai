#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from sh_house_data.config import config_dict

# db
# db = SQLAlchemy()

# login


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # 初始化
    # db.init_app(app)

    # 蓝图
    from .views import main

    app.register_blueprint(main)

    # 其他

    # 日志
    handler = TimedRotatingFileHandler('app.log', when='D', backupCount=7, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    return app
