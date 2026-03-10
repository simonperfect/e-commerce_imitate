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

    # ===== PRIORITY 1: SET DATABASE URI DIRECTLY FROM ENVIRONMENT =====
    import os
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("="*60)
        print("✅ DATABASE URI SET DIRECTLY FROM ENVIRONMENT")
        print(f"📊 Database URI prefix: {database_url[:20]}...")
        print("="*60)
    else:
        print("="*60)
        print("❌ ERROR: DATABASE_URL NOT FOUND IN ENVIRONMENT")
        print("="*60)
    # ==================================================================

    # Get configuration class based on config_name
    Config = config_map.get(config_name)  # config_map contains 'develop', 'product', or 'test'
    
    # Load configuration settings into Flask app
    if Config:
        print(f"🔧 Loading additional config from: {config_name}")
        app.config.from_object(Config)
    
    # Initialize db
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