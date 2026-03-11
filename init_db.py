# init_db.py
from flask import Flask
from extensions import db
from models import Userform, Menu, Role, Category, Attribute, Product
from werkzeug.security import generate_password_hash

def init_database():
    """在 Render 環境中初始化資料庫"""
    print("="*60)
    print("🔥 開始在 Render 上初始化資料庫")
    
    # 導入 Flask 應用
    from managerfinal import app
    
    with app.app_context():
        # 1. 建立所有資料表
        print("📦 正在建立資料表...")
        db.create_all()
        print("✅ 資料表建立完成！")
        
        # 2. 檢查是否需要建立預設管理員
        admin = Userform.query.filter(Userform.name == 'admin').first()
        if not admin:
            print("👤 建立預設管理員帳號...")
            admin = Userform(
                name='admin',
                pwd=generate_password_hash('123456'),
                nick_name='Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ 預設管理員建立成功")
            print("   👤 帳號: admin")
            print("   🔑 密碼: 123456")
        else:
            print("👤 管理員帳號已存在")
        
        # 3. 檢查是否有其他資料需要初始化
        # 你可以在這裡加入更多初始化邏輯
        
    print("="*60)
    print("🎉 Render 資料庫初始化完成！")
    print("="*60)

if __name__ == "__main__":
    init_database()