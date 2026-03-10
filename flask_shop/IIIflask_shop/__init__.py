#Transfer manager configuration object here
import sys
import os

# Add upper directory (flask_shop) to Python path
parent_dir = os.path.dirname(os.path.dirname(__file__))  # This is flask_shop directory
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask
from flask_migrate import Migrate
from extensions import db

# Now we can import config
from config import config_map

def create_app(config_name):
    app = Flask(__name__)

    # 獲取配置類
    Config = config_map.get(config_name)
    print(f"🔍 Config class: {Config}")
    
    if Config is None:
        raise ValueError(f"❌ Invalid config name: {config_name}. Available: {list(config_map.keys())}")
    
    # 載入配置
    print(f"🔍 Loading config from: {Config.__name__}")
    app.config.from_object(Config)
    
    # 立即檢查
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    print(f"🔍 After from_object, SQLALCHEMY_DATABASE_URI = {db_uri}")
    
    # 如果是生產環境且沒有URI，從環境變數直接讀取
    if config_name == 'production' and db_uri is None:
        print("⚠️ Production mode but no URI found, checking DATABASE_URL...")
        db_uri = os.environ.get('DATABASE_URL')
        if db_uri:
            app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
            print(f"✅ Manually set from DATABASE_URL: {db_uri[:20]}...")
        else:
            print("❌ DATABASE_URL not found in environment!")
    
    # 最終確認
    final_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    print(f"🔍 Final SQLALCHEMY_DATABASE_URI = {final_uri}")
    
    # 初始化db
    if final_uri is None:
        raise RuntimeError("❌ SQLALCHEMY_DATABASE_URI is still None before db.init_app!")
    
    db.init_app(app)
    
    # Get user blueprint - use sys.path to add current directory
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from user import user_bp
    # Register blueprint - first table
    app.register_blueprint(user_bp)

    # Second table
    from menu import menu_bp
    app.register_blueprint(menu_bp)

    # Role character
    from role import role_bp
    app.register_blueprint(role_bp)

    # Get category object
    from category import cate_bp
    app.register_blueprint(cate_bp)

    # Attribute from category
    from category import attr_bp
    app.register_blueprint(attr_bp)

    # Product
    from product import product_bp
    app.register_blueprint(product_bp)

    return app