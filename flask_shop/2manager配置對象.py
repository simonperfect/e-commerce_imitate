# terminal pip install flask_sqlalchmy==3.0.2
#同步操作mysql 要migrate  pip install flask-migrate==4.0.0

#告訴電腦運行哪個flask文件 我們需要告訴他是managerfinal
#terminal  env:FLASK_APP="managerfinal"

#生成同步數據庫文件
#terminal   flask db init
#執行到這裏后會生成一個migrations文件夾

#pip install pymysql==1.0.2

#檢測當前應用的所有模型
#flask db migrate 

#同步數據庫table
#flask db upgrade


from flask import Flask
import os        
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)



class config:

    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_HOST = 'localhost'   #localhost
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'flask_shop'
    MYSQL_CHARSET = 'utf8mb4'

    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'

    SECRET_KEY = os.urandom(26)

    DEBUG = True



app.config.from_object(config)   

#創建SQLAlchemy實例
db = SQLAlchemy(app)



@app.route('/')
def index():
    return 'Hello123'



#同步數據庫的對象
Migrate(app,db)




#啓動服務
if __name__ == '__main__':
    app.run()

