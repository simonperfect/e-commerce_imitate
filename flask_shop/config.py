#Transfer the config of IIIflask_shop to here

import os

class Config:
    # Read database configuration from environment variables, use default values if not set
    MYSQL_DIALECT = os.environ.get('MYSQL_DIALECT', 'mysql')
    MYSQL_DRIVER = os.environ.get('MYSQL_DRIVER', 'pymysql')
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'flask_shop')
    MYSQL_CHARSET = os.environ.get('MYSQL_CHARSET', 'utf8mb4')

    # Ensure Chinese characters display correctly
    JSON_AS_ASCII = False
    RESTFUL_JSON = {'ensure_ascii': False}

    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))

    # Set debug mode based on environment variable
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):     # Development version
    DEBUG = True
    # Development environment forces using MySQL
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://root:root@localhost:3306/flask_shop?charset=utf8mb4'
    )

class ProductionConfig(Config):
    """Production environment configuration - Uses only DATABASE_URL"""
    DEBUG = False
    
    # Directly set class attribute at definition time
    # This runs when the module is imported, not when Flask loads the config
    _database_url = os.environ.get('DATABASE_URL')
    
    if not _database_url:
        print("="*60)
        print("🏭 Production Configuration")
        print("❌ FATAL ERROR: DATABASE_URL environment variable is not set!")
        print("Please set DATABASE_URL in Render Dashboard's Environment page.")
        print("="*60)
        # This will cause the application to fail at import time
        SQLALCHEMY_DATABASE_URI = None
    else:
        SQLALCHEMY_DATABASE_URI = _database_url
        print("="*60)
        print("🏭 Production Configuration Loaded")
        print(f"✅ DATABASE_URL found")
        print(f"📊 Database URI prefix: {_database_url[:20]}...")
        print("="*60)

class TestingConfig(Config):      # Testing version
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{Config.MYSQL_USERNAME}:{Config.MYSQL_PASSWORD}@'
        f'{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}_test?charset={Config.MYSQL_CHARSET}'
    )

# Configuration mapping
config_map = {
    'develop': DevelopmentConfig,    # Development mode
    'product': ProductionConfig,     # Production mode
    'test': TestingConfig            # Testing environment
}