import sqlite3
import os

def get_connection():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "weather_data.db")
    print(f"📂 Using DB at: {db_path}")   # 👈 ADD THIS LINE

    return sqlite3.connect(db_path)

def setup_database():
    conn = get_connection()   # ✅ MUST use SAME function
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    timestamp TEXT,
    temperature REAL,
    humidity INTEGER,
    pressure REAL,
    wind_speed REAL,
    condition TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_summary (
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    avg_temperature REAL,
    total_records INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

    conn.commit()
    conn.close()

    print("✅ Tables created successfully")