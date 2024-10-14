import schedule
import time
import threading
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("url_hit_log.log"),
        logging.StreamHandler()
    ]
)

# List of URLs to hit every 1 minute
URLS = [
    "https://baseboilerflaskadvanceapi.onrender.com",
    "https://sotrueplay.onrender.com"
]

def hit_urls():
    for url in URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info(f"Successfully hit URL: {url}, Status Code: {response.status_code}")
            else:
                logging.warning(f"Failed to hit URL: {url}, Status Code: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Error occurred while hitting {url}: {e}")

def run_scheduler():
    schedule.every(1).minutes.do(hit_urls)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Run the scheduler in a separate thread to avoid blocking the main process
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Keep the server alive
    while True:
        pass
