# -*- coding: utf-8 -*-
# File: __init__.py.py
# Author: Alley
# Date  : 2021/1/22
from flask import Flask
import settings
from apps.index.views import index_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.ProductionConfig)
    app.register_blueprint(index_bp)
    return app