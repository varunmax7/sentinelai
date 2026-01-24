# check_columns.py
import sqlite3
import os
from app import app

def check_columns():
    db_path = os.path.join(app.instance_path, 'site.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(user)")
    columns = cursor.fetchall()
    
    print("📊 Current user table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    with app.app_context():
        check_columns()