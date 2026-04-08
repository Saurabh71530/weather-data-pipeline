from src.monitor import log_error
import requests
import time
from datetime import datetime
from config import config
API_KEY = config.API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city, retries=3, delay=2):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    for attempt in range(retries):
        start_time = time.time()

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()

                return {
                    "city": city,
                    "timestamp": datetime.now(),
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "condition": data["weather"][0]["description"],
                    "status": "success",
                    "response_time": response_time,
                    "error": None
                }

            else:
                error_msg = f"HTTP {response.status_code}"

        except requests.exceptions.RequestException as e:
            response_time = None
            error_msg = str(e)

        # ✅ retry logic
        if attempt < retries - 1:
            log_error(f"Retry {attempt+1} for {city}: {error_msg}")
            time.sleep(delay)
        else:
            return {
                "city": city,
                "status": "failed",
                "response_time": response_time,
                "error": error_msg
            }