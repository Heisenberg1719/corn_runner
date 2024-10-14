import schedule
import time
import threading
import requests
import logging
from flask import Flask, jsonify
from waitress import serve

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

app = Flask(__name__)
log_messages = []  # Store log messages for review

# Function to hit URLs
def hit_urls():
    while True:
        for url in URLS:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    log_msg = f"Successfully hit URL: {url}, Status Code: {response.status_code}"
                    logging.info(log_msg)
                else:
                    log_msg = f"Failed to hit URL: {url}, Status Code: {response.status_code}"
                    logging.warning(log_msg)
                log_messages.append(log_msg)
            except requests.RequestException as e:
                log_msg = f"Error occurred while hitting {url}: {e}"
                logging.error(log_msg)
                log_messages.append(log_msg)
        time.sleep(45)  

# API to review logs in a traditional, non-real-time manner
@app.route('/', methods=['GET'])
def get_logs():
    return jsonify({"logs": log_messages[-20:]})  

def run_flask_app():
    # Run the Flask app using Waitress in production
    serve(app, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Start the scheduler in a separate thread to hit URLs periodically
    scheduler_thread = threading.Thread(target=hit_urls, daemon=True)
    scheduler_thread.start()

    # Run the Flask app using Waitress in the main thread
    run_flask_app()
