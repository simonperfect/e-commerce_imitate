from IIIflask_shop import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS
from flask import request  # 加上這行
import os
from models import Userform

# 從環境變量讀取配置模式，預設為 'develop'（注意這裡是 develop，不是 development）
config_mode = os.environ.get('FLASK_ENV', 'develop')
print(f"正在啟動應用，配置模式: {config_mode}")

app = create_app(config_mode)
CORS(app, supports_credentials=True)
Migrate(app, db)

db.app = app

@app.route('/')
def index():
    return 'Flask 後端運行成功！'

@app.route('/init-db', methods=['GET'])
def init_db_route():
    """初始化資料庫的路由（只允許內部使用）"""
    from werkzeug.security import generate_password_hash
    
    
    auth_key = request.args.get('key')
    if auth_key != 'my_secret_init_key_2026':
        return {'error': 'Unauthorized'}, 403
    
    try:
        with app.app_context():
            db.create_all()
            admin = Userform.query.filter(Userform.name == 'admin').first()
            if not admin:
                admin = Userform(
                    name='admin',
                    pwd=generate_password_hash('123456'),
                    nick_name='Administrator'
                )
                db.session.add(admin)
                db.session.commit()
                return {'message': '資料庫初始化成功！管理員帳號已建立'}
            else:
                return {'message': '資料庫已存在，無需初始化'}
    except Exception as e:
        return {'error': str(e)}, 500
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)