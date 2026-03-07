#pip install flask==2.2.2
from flask import Flask
import os        #用於下面自動生成secret_key

#創建一個falsk實例
app = Flask(__name__)

class config:
    #設置參數
    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'flask_shop'
    MYSQL_CHARSET = 'utf8mb4'

    #數據庫連接flask 字符串 uri
    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'

    #數據鹽
    SECRET_KEY = os.urandom(26)

    #DEBUG模式
    DEBUG = True


#根據類來加載配置信息
app.config.from_object(config)    #如果不適用class config的話 就是app.config[SQLCHEMY_DATABASE_URI] = 'SQLALCHEMY_DATABASE_URI'  
  




#創建路由與函數的映射
@app.route('/')
def index():
    return 'Hello123'

#啓動服務
if __name__ == '__main__':
    app.run()

