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

    # Base class should not set SQLALCHEMY_DATABASE_URI, it will be set by subclasses
    SQLALCHEMY_DATABASE_URI = None

    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))

    # Set debug mode based on environment variable
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):     # Development version
    DEBUG = True
    
    def __init__(self):
        # Development environment forces using MySQL
        self.SQLALCHEMY_DATABASE_URI = (
            f'mysql+pymysql://root:root@localhost:3306/flask_shop?charset=utf8mb4'
        )
        print("="*60)
        print("🔧 Development Configuration Loaded")
        print(f"📊 Database: {self.SQLALCHEMY_DATABASE_URI}")
        print(f"🐛 Debug mode: {self.DEBUG}")
        print("="*60)

class ProductionConfig(Config):
    """Production environment configuration - Uses only DATABASE_URL"""
    DEBUG = False

    def __init__(self):
        print("="*60)
        print("🏭 Loading Production Configuration")

        # Get DATABASE_URL from environment variables
        database_url = os.environ.get('DATABASE_URL')

        # Check if DATABASE_URL exists and is not empty
        if not database_url:
            error_msg = (
                "\n" + "="*60 + "\n" +
                "❌ FATAL ERROR: Production configuration failed!\n"
                "Environment variable 'DATABASE_URL' is not set or is empty.\n"
                "Please set DATABASE_URL in Render Dashboard's Environment page.\n" +
                "="*60
            )
            print(error_msg)
            raise ValueError("DATABASE_URL environment variable not set for production!")

        # Set database URI
        self.SQLALCHEMY_DATABASE_URI = database_url
        print(f"✅ Successfully read DATABASE_URL")
        # Only print prefix to avoid exposing sensitive information
        print(f"📊 Database URI prefix: {database_url[:20]}...")
        
        # Ensure parent class configurations are properly inherited
        self.SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))
        print("="*60)

class TestingConfig(Config):      # Testing version
    DEBUG = True
    TESTING = True
    
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = (
            f'mysql+pymysql://{self.MYSQL_USERNAME}:{self.MYSQL_PASSWORD}@'
            f'{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}_test?charset={self.MYSQL_CHARSET}'
        )
        print("="*60)
        print("🧪 Testing Configuration Loaded")
        print(f"📊 Database: {self.SQLALCHEMY_DATABASE_URI}")
        print("="*60)

# Configuration mapping
config_map = {
    'develop': DevelopmentConfig,    # Development mode
    'product': ProductionConfig,     # Production mode
    'test': TestingConfig            # Testing environment
}