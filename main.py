import requests
import schedule
import time

# List of URLs to ping
urls = ["https://stp-advance.onrender.com"]

def ping_urls():
    for url in urls:
        try:
            response = requests.get(url)
            print(f"URL: {url}, Status Code: {response.status_code}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to reach {url}. Reason: {e}")

# Schedule the ping function to run every 50 seconds
schedule.every(50).seconds.do(ping_urls)

if __name__ == "__main__":
    print("Starting URL ping service...")
    while True:
        schedule.run_pending()
        time.sleep(1)
