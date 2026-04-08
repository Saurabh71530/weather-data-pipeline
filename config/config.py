import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

DATABASE_PATH = "database/weather_data.db"

CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]