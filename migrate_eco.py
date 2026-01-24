\from app import app, db
from models import Badge

def migrate_eco_tables():
    with app.app_context():
        try:
            print("🔄 Starting Eco Tracker migration...")
            
            # Create the tables using SQL directly
            db.engine.execute('''
                CREATE TABLE IF NOT EXISTS plastic_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    plastic_type VARCHAR(100) NOT NULL,
                    quantity FLOAT NOT NULL,
                    unit VARCHAR(20) DEFAULT 'pieces',
                    image_proof VARCHAR(200),
                    description TEXT,
                    verified BOOLEAN DEFAULT FALSE,
                    verification_score FLOAT DEFAULT 0.0,
                    points_earned INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')
            print("✅ Created plastic_usage table")
            
            db.engine.execute('''
                CREATE TABLE IF NOT EXISTS carbon_savings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    activity_type VARCHAR(100) NOT NULL,
                    carbon_saved FLOAT NOT NULL,
                    description TEXT,
                    proof_type VARCHAR(50),
                    proof_file VARCHAR(200),
                    verified BOOLEAN DEFAULT FALSE,
                    points_earned INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')
            print("✅ Created carbon_savings table")
            
            # Add eco badges
            eco_badges = [
                ('plastic_warrior', 'Reduced 1kg of plastic', '♻️', 0),
                ('carbon_neutral', 'Saved 100kg of CO2', '🌱', 0),
                ('eco_champion', 'Earned 500 eco points', '🏆', 500),
                ('green_commuter', 'Used eco transport 10 times', '🚲', 0),
            ]
            
            for name, description, icon, points in eco_badges:
                # Check if badge exists using SQL
                result = db.engine.execute(
                    "SELECT id FROM badge WHERE name = ?", (name,)
                ).fetchone()
                
                if not result:
                    db.engine.execute(
                        "INSERT INTO badge (name, description, icon, points_required) VALUES (?, ?, ?, ?)",
                        (name, description, icon, points)
                    )
                    print(f"✅ Added badge: {name}")
                else:
                    print(f"ℹ️  Badge already exists: {name}")
            
            db.session.commit()
            print("🎉 Eco Tracker migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_eco_tables()