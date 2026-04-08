import time
from src.etl_pipeline import run_pipeline

def run_scheduler():
    while True:
        run_pipeline()
        time.sleep(3600)  # run every 1 hour