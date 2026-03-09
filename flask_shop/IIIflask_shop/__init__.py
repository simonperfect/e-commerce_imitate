#轉移manager配置對象過來
import sys
import os

# 添加上層目錄 (flask_shop) 到 Python 路徑
parent_dir = os.path.dirname(os.path.dirname(__file__))  # 這是 flask_shop 目錄
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask
from flask_migrate import Migrate
from extensions import db

# 現在可以導入 config
from config import config_map









def create_app(config_name):
    app = Flask(__name__)



    #根據config_name 獲取配置類
    Config = config_map.get(config_name)     #config_map裏面的  develop product 或者test
    
    # 將配置類中的設置加載到 Flask 應用
    app.config.from_object(Config)      #如果不適用class config的話 就是app.config[SQLCHEMY_DATABASE_URI] = 'SQLALCHEMY_DATABASE_URI'  
    
    #初始化db
    db.init_app(app)
    
    #獲取藍圖user - 使用 sys.path 添加當前目錄
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from user import user_bp
    #注冊藍圖 第一個table   
    app.register_blueprint(user_bp)


    #第二個table
    from menu import menu_bp
    app.register_blueprint(menu_bp)


    #role character
    from role import role_bp
    app.register_blueprint(role_bp)

    #get category object
    from category import cate_bp
    app.register_blueprint(cate_bp)


    #attribute from category
    from category import attr_bp
    app.register_blueprint(attr_bp)

    #product
    from product import product_bp
    app.register_blueprint(product_bp)

    return app