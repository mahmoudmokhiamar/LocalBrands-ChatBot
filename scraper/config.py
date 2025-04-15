# config.py
BASE_URL = "https://gonative.eg"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
REQUEST_DELAY = 1  # seconds between requests
MAX_RETRIES = 3
OUTPUT_DIR = "../data"
OUTPUT_FILE = "products_full.json"