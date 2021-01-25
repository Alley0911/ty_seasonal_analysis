# -*- coding: utf-8 -*-
# File: settings.py
# Author: Alley
# Date  : 2021/1/22
# 用于将配置和程序解耦，避免错误，pycharm有问题，在linux里可以正确运行
class Config:
    ENV = "development"
    DEBUG = True
    # 用户名加密码
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:port/databasename'

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
