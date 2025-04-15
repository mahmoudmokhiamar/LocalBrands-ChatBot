# utils.py
import time
import random
import requests
from config import HEADERS, REQUEST_DELAY, MAX_RETRIES,REQUEST_DELAY

def fetch_url(url, retries=0):
    """Fetch URL with retries and delays"""
    try:
        time.sleep(REQUEST_DELAY + random.uniform(0, 0.5))  # Random delay
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        if retries < MAX_RETRIES:
            print(f"Retrying {url} ({retries+1}/{MAX_RETRIES})...")
            return fetch_url(url, retries+1)
        print(f"Failed to fetch {url}: {e}")
        return None