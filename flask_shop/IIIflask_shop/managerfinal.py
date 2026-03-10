from __init__ import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS
import os

# 直接強制使用 production，不看環境變數
config_mode = 'production'
print(f"正在啟動應用，配置模式: {config_mode}")

# 手動設定 DATABASE_URL 環境變數（用你的實際連接字串）
os.environ['DATABASE_URL'] = 'postgresql://e_commerce_db_kdt8_user:TvblnAr0141UnfsJXm3iI0DReMcNf1b@dpg-d6npo7tm5p6s739auhog-a.oregon-postgres.render.com/e_commerce_db_kdt8'

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