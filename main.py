from src.database import setup_database
from src.etl_pipeline import run_pipeline
from src.reporter import generate_report, generate_alerts, top_hottest_city
from src.house_analysis import analyze_house_prices
from src.visualizer import plot_temperature_trend

if __name__ == "__main__":
    setup_database()
    run_pipeline()

    generate_report()
    generate_alerts()
    top_hottest_city()
    analyze_house_prices()

    plot_temperature_trend()