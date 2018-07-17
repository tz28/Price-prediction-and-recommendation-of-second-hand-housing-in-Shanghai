#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Flask配置基础类
    """
    SECRET_KEY = 'SECRET'


class DevelopmentConfig(BaseConfig):
    """
    Flask开发配置
    """
    DEBUG = True
    SERVER_NAME = '127.0.0.1:8080'
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """
    Flask线上配置
    """


# Flask配置字典
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
