# migrate_data.py
import pymysql
import psycopg2
import logging
from psycopg2.extras import execute_values
import time

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==================== 資料庫連線設定 ====================
# 本地 MySQL 設定
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flask_shop',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Render PostgreSQL 設定
PG_CONN_STRING = "postgresql://e_commerce_db_kdt8_user:TvbLnAr0l4LlUnfsJXm3iIODReMcNf1b@dpg-d6npo7tm5p6s739auhog-a.singapore-postgres.render.com/e_commerce_db_kdt8"

# ==================== 表格定義（依賴順序） ====================
TABLES = [
    {
        'name': 't_role',
        'columns': ['id', 'name', 'desc'],
        'pg_columns': ['id', 'name', '"desc"']  # desc 是關鍵字，需要雙引號
    },
    {
        'name': 't_menus',
        'columns': ['id', 'name', 'path', 'level', 'pid'],
        'pg_columns': ['id', 'name', 'path', 'level', 'pid']
    },
    {
        'name': 't_users',
        'columns': ['id', 'name', 'pwd', 'nick_name', 'phone', 'email', 'role_id'],
        'pg_columns': ['id', 'name', 'pwd', 'nick_name', 'phone', 'email', 'role_id']
    },
    {
        'name': 't_roles_menus',
        'columns': ['role_id', 'menu_id'],
        'pg_columns': ['role_id', 'menu_id']
    },
    {
        'name': 't_category',
        'columns': ['id', 'name', 'level', 'pid'],
        'pg_columns': ['id', 'name', 'level', 'pid']
    },
    {
        'name': 't_attribute',
        'columns': ['id', 'name', 'val', '_type', 'cid'],
        'pg_columns': ['id', 'name', 'val', '_type', 'cid']
    },
    {
        'name': 't_product',
        'columns': ['id', 'name', 'price', 'number', 'introduce', 'big_img', 'small_img', 'state', 'is_promote', 'hot_number', 'weight', 'cid_one', 'cid_two', 'cid_three'],
        'pg_columns': ['id', 'name', 'price', 'number', 'introduce', 'big_img', 'small_img', 'state', 'is_promote', 'hot_number', 'weight', 'cid_one', 'cid_two', 'cid_three']
    }
]

def get_pg_connection():
    return psycopg2.connect(PG_CONN_STRING)

def get_mysql_connection():
    return pymysql.connect(**mysql_config)

def table_exists(pg_cursor, table_name):
    pg_cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """, (table_name,))
    return pg_cursor.fetchone()[0]

def migrate_table(table_info):
    """搬移單一表格"""
    table_name = table_info['name']
    mysql_cols = table_info['columns']
    pg_cols = table_info['pg_columns']
    
    logging.info(f"開始處理表格: {table_name}")
    
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()
    pg_conn = get_pg_connection()
    pg_cursor = pg_conn.cursor()
    
    try:
        # 1. 確保表格存在
        if not table_exists(pg_cursor, table_name):
            logging.warning(f"表格 {table_name} 不存在，跳過搬移（請先用 /init-db 建立表格）")
            return
        
        # 2. 從 MySQL 讀取資料
        mysql_cursor.execute(f"SELECT * FROM {table_name} ORDER BY id")
        rows = mysql_cursor.fetchall()
        logging.info(f"從 MySQL 讀取到 {len(rows)} 筆資料")
        
        if not rows:
            logging.info(f"表格 {table_name} 無資料，跳過")
            return
        
        # 3. 準備 SQL
        pg_cols_str = ','.join(pg_cols)
        placeholders = ','.join(['%s'] * len(mysql_cols))
        insert_sql = f"INSERT INTO {table_name} ({pg_cols_str}) VALUES ({placeholders})"
        
        # 4. 轉換資料格式
        values = []
        for row in rows:
            row_values = []
            for col in mysql_cols:
                # 處理 None 值
                val = row[col] if row[col] is not None else None
                row_values.append(val)
            values.append(row_values)
        
        # 5. 批次寫入 PostgreSQL
        batch_size = 500
        total = len(values)
        for i in range(0, total, batch_size):
            batch = values[i:i+batch_size]
            pg_cursor.executemany(insert_sql, batch)
            pg_conn.commit()
            logging.info(f"✅ 已寫入 {min(i+batch_size, total)}/{total} 筆")
        
        logging.info(f"✅ 表格 {table_name} 搬移完成")
        
    except Exception as e:
        pg_conn.rollback()
        logging.error(f"❌ 搬移 {table_name} 時發生錯誤: {e}")
        raise
    finally:
        mysql_cursor.close()
        mysql_conn.close()
        pg_cursor.close()
        pg_conn.close()

def main():
    logging.info("="*60)
    logging.info("🔥 開始從本地 MySQL 遷移數據到 Render PostgreSQL")
    logging.info("="*60)
    
    # 測試 MySQL 連線
    try:
        conn = get_mysql_connection()
        conn.close()
        logging.info("✅ MySQL 連線成功")
    except Exception as e:
        logging.error(f"❌ MySQL 連線失敗: {e}")
        return
    
    # 測試 PostgreSQL 連線
    try:
        conn = get_pg_connection()
        conn.close()
        logging.info("✅ PostgreSQL 連線成功")
    except Exception as e:
        logging.error(f"❌ PostgreSQL 連線失敗: {e}")
        return
    
    # 開始搬移
    success_count = 0
    fail_count = 0
    
    for table_info in TABLES:
        try:
            migrate_table(table_info)
            success_count += 1
        except Exception as e:
            logging.error(f"❌ 處理表格 {table_info['name']} 失敗，停止後續搬移")
            fail_count += 1
            break
    
    logging.info("="*60)
    logging.info(f"📊 搬移完成：成功 {success_count} 個表格，失敗 {fail_count} 個表格")
    logging.info("="*60)

if __name__ == "__main__":
    main()