from src.api_client import fetch_weather
from src.database import get_connection
from config.config import CITIES
from src.monitor import log_info, log_error
from src.validators import validate_weather_data, validate_temperature


def extract():
    log_info("Starting data extraction")
    data = []

    for city in CITIES:
        result = fetch_weather(city)
        data.append(result)

        if result["status"] == "failed":
            log_error(f"API failed for {city}: {result['error']}")

    return data


def transform(raw_data):
    log_info("Starting data transformation")
    clean_data = []

    for item in raw_data:
        if (
            item["status"] == "success"
            and validate_weather_data(item)
            and validate_temperature(item["temperature"])   # ✅ NEW LINE
        ):
            clean_data.append(item)
        else:
            log_error(f"Invalid or failed data for {item['city']}")

    return clean_data


def load_data(data):
    conn = get_connection()
    cursor = conn.cursor()

    for item in data:
        # 🔹 Insert city if not exists
        cursor.execute("""
        INSERT OR IGNORE INTO cities (city_name)
        VALUES (?)
        """, (item["city"],))

        # 🔹 Get city_id
        cursor.execute("""
        SELECT city_id FROM cities WHERE city_name = ?
        """, (item["city"],))

        result = cursor.fetchone()
        if result:
            city_id = result[0]
        else:
            log_error(f"City not found: {item['city']}")
            continue

        # 🔹 Insert weather data
        cursor.execute("""
        INSERT INTO weather_data (
            city_id, timestamp, temperature, humidity, pressure, wind_speed, condition
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            city_id,
            str(item["timestamp"]),
            item["temperature"],
            item["humidity"],
            item["pressure"],
            item["wind_speed"],
            item["condition"]
        ))

    conn.commit()
    conn.close()

    


# ✅ NEW ANALYTICS FUNCTION
def calculate_average_temperature(data):
    temps = [item["temperature"] for item in data if item["status"] == "success"]

    if temps:
        avg_temp = sum(temps) / len(temps)
        log_info(f"Average Temperature: {avg_temp:.2f}°C")
    else:
        log_error("No valid temperature data available")


# ✅ MAIN PIPELINE (THIS WAS YOUR ISSUE)
def run_pipeline():
    log_info("ETL pipeline started")

    try:
        raw_data = extract()  # ✅ DEFINE FIRST
        clean_data = transform(raw_data)

        calculate_average_temperature(clean_data)  # ✅ THEN USE

        load_data(clean_data)

        log_info("ETL pipeline completed successfully")

    except Exception as e:
        log_error(f"Pipeline failed: {str(e)}")


