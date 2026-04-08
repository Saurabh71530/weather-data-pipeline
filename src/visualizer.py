import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def plot_temperature_trend():
    conn = sqlite3.connect("weather_data.db")

    # ✅ Step 1: Load data
    df = pd.read_sql_query(
        "SELECT timestamp, temperature FROM weather_data", conn
    )

    # ✅ Step 2: Convert + sort
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")

    # ✅ Step 3: Group by date (THIS FIXES MESSY GRAPH)
    df["date"] = df["timestamp"].dt.date
    daily_avg = df.groupby("date")["temperature"].mean().reset_index()

    # ✅ Step 4: BAR CHART (clean & safe)
    plt.figure(figsize=(10, 5))

    plt.bar(daily_avg["date"], daily_avg["temperature"])

    plt.title("Average Temperature per Day", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Temperature (°C)", fontsize=12)

    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


    # ✅ Step 5: ADD HISTOGRAM HERE (👇 RIGHT HERE)
    plt.figure(figsize=(8, 5))

    plt.hist(df["temperature"], bins=10)

    plt.title("Temperature Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Temperature (°C)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
        
    conn.close()

    # ✅ CALL FUNCTION
plot_temperature_trend()