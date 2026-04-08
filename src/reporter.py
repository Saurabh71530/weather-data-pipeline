from src.database import get_connection



def generate_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(temperature) FROM weather_data")
    avg_temp = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM weather_data")
    total_records = cursor.fetchone()[0]

    print("\n📊 WEATHER REPORT")
    print("====================")
    print(f"Average Temperature: {avg_temp:.2f}°C")
    print(f"Total Records: {total_records}")

    def save_summary(avg_temp, total_records):
     conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO weather_summary (avg_temperature, total_records)
    VALUES (?, ?)
    """, (avg_temp, total_records))

    conn.commit()
    conn.close()

    conn.close()   # ✅ close AFTER everything

def top_hottest_city():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.city_name, AVG(w.temperature) as avg_temp
    FROM weather_data w
    JOIN cities c ON w.city_id = c.city_id
    GROUP BY c.city_name
    ORDER BY avg_temp DESC
    LIMIT 1
    """)

    result = cursor.fetchone()

    print("\n🔥 HOTTEST CITY")
    print("====================")
    print(f"{result[0]} with {result[1]:.2f}°C")

    conn.close()

def generate_alerts():
    conn = get_connection()   # ✅ NEW connection
    cursor = conn.cursor()

    cursor.execute("""
    SELECT temperature FROM weather_data
    WHERE temperature > 30
    """)

    alerts = cursor.fetchall()

    print("\n⚠️ ALERTS")
    print("====================")

    if alerts:
        for alert in alerts:
            print(f"High temperature detected: {alert[0]}°C")
    else:
        print("No alerts")

    conn.close()   # ✅ separate close