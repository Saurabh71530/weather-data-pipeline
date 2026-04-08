def validate_weather_data(data):
    required_keys = [
        "city", "temperature", "humidity",
        "pressure", "wind_speed", "condition"
    ]

    for key in required_keys:
        if key not in data or data[key] is None:
            return False

    return True


def validate_temperature(temp):
    if temp < -50 or temp > 60:
        return False
    return True