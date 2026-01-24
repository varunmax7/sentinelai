# add_language_column.py
import sqlite3
import os
from app import app

def add_missing_columns():
    print("🔧 Adding missing columns to database...")
    
    # Connect to your SQLite database
    db_path = os.path.join(app.instance_path, 'site.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check what columns already exist in user table
        cursor.execute("PRAGMA table_info(user)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Existing columns: {existing_columns}")
        
        # Add missing columns one by one (if they don't exist)
        columns_to_add = [
            ('language', 'VARCHAR(10) DEFAULT "en"'),
            ('push_token', 'VARCHAR(255)'),
            ('home_latitude', 'FLOAT'),
            ('home_longitude', 'FLOAT'),
            ('alert_preferences', 'TEXT')
        ]
        
        for column_name, column_type in columns_to_add:
            if column_name not in existing_columns:
                sql = f"ALTER TABLE user ADD COLUMN {column_name} {column_type}"
                cursor.execute(sql)
                print(f"✅ Added column: {column_name}")
            else:
                print(f"✅ Column already exists: {column_name}")
        
        conn.commit()
        print("🎉 Database updated successfully! All missing columns added.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    with app.app_context():
        add_missing_columns()