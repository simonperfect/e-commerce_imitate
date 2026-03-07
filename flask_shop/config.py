#轉移IIIflask_shop的 config到這裏   

import os


class config:

    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_HOST = 'localhost'   #localhost
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'flask_shop'
    MYSQL_CHARSET = 'utf8mb4'

    #確保能輸出中文
    JSON_AS_ASCII = False
    RESTFUL_JSON = {'ensure_ascii':False}

    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'

    SECRET_KEY = os.urandom(16)

    

class DevelopmentConfig(config):     #開發版本
    DEBUG = True

class ProductionConfig(config):   #生產版本 
    DEBUG = False

class TestingConfig(config):      #測試版本
    DEBUG = True

config_map = {
    'develop': DevelopmentConfig,    #開發模式
    'product': ProductionConfig,   #生產模式
    'test': TestingConfig      #測試環境
}