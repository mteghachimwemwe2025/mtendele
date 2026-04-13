import threading
import time
import requests

def keep_alive():
    url = "https://www.mtenderebaptistchurch.org/"  # your live Render URL
    while True:
        try:
            response = requests.get(url)
            print(f"Keep-alive ping: {response.status_code}")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(600)  # ping every 10 minutes

def start_keep_alive():
    thread = threading.Thread(target=keep_alive)
    thread.daemon = True
    thread.start()
