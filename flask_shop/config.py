#轉移IIIflask_shop的 config到這裏   

import os

class Config:
    # 從環境變量讀取數據庫配置，如果沒有則用默認值
    MYSQL_DIALECT = os.environ.get('MYSQL_DIALECT', 'mysql')
    MYSQL_DRIVER = os.environ.get('MYSQL_DRIVER', 'pymysql')
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'flask_shop')
    MYSQL_CHARSET = os.environ.get('MYSQL_CHARSET', 'utf8mb4')

    # 確保能輸出中文
    JSON_AS_ASCII = False
    RESTFUL_JSON = {'ensure_ascii': False}

    # 如果設置了 DATABASE_URL，優先使用（Render PostgreSQL 專用）
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # 否則使用 MySQL 配置
        SQLALCHEMY_DATABASE_URI = (
            f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@'
            f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'
        )

    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))

    # 根據環境設置調試模式
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):     #開發版本
    DEBUG = True
    # 開發環境強制使用 MySQL
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://root:root@localhost:3306/flask_shop?charset=utf8mb4'
    )

class ProductionConfig(Config):
    """生產環境配置 - 僅使用 DATABASE_URL"""
    DEBUG = False

    def __init__(self):
        print("="*60)
        print("🏭 正在載入生產環境配置 (ProductionConfig)")

        # 從環境變數獲取 DATABASE_URL
        database_url = os.environ.get('DATABASE_URL')

        # 檢查 DATABASE_URL 是否存在且不為空
        if not database_url:
            error_msg = (
                "\n" + "="*60 + "\n" +
                "❌ 致命錯誤：生產環境配置失敗！\n"
                "環境變數 'DATABASE_URL' 未設定或為空。\n"
                "請在 Render Dashboard 的 Environment 頁面中設定 DATABASE_URL。\n" +
                "="*60
            )
            print(error_msg)
            raise ValueError("DATABASE_URL environment variable not set for production!")

        # 設定數據庫 URI
        self.SQLALCHEMY_DATABASE_URI = database_url
        print(f"✅ 成功讀取 DATABASE_URL")
        print(f"📊 數據庫 URI 前綴: {database_url[:20]}...") # 只打印前綴，避免顯示敏感信息
        print("="*60)

class TestingConfig(Config):      #測試版本
    DEBUG = True
    TESTING = True

config_map = {
    'develop': DevelopmentConfig,    #開發模式
    'product': ProductionConfig,   #生產模式
    'test': TestingConfig      #測試環境
}