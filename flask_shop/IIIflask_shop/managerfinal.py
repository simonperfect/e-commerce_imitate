from __init__ import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS
import os

# 從環境變量讀取配置模式，預設為 develop
config_mode = os.environ.get('FLASK_ENV', 'develop')
print(f"正在啟動應用，配置模式: {config_mode}")

app = create_app(config_mode)
CORS(app, supports_credentials=True)
Migrate(app, db)

# 添加這行，把 db 綁定到 app
db.app = app

# 添加根路由，用於健康檢查和訪問
@app.route('/')
def index():
    return 'Flask 後端運行成功！'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)