from __init__ import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS
import os

# 從環境變量讀取配置模式
config_mode = os.environ.get('FLASK_ENV', 'development')
print(f"正在啟動應用，配置模式: {config_mode}")

# ❌ 刪掉手動設定那行，不需要！
# os.environ['DATABASE_URL'] = '...'

app = create_app(config_mode)
CORS(app, supports_credentials=True)
Migrate(app, db)

db.app = app

@app.route('/')
def index():
    return 'Flask 後端運行成功！'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)