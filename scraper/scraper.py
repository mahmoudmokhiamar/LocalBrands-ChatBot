# scraper.py
import json
import os
from bs4 import BeautifulSoup
from config import BASE_URL, OUTPUT_DIR, OUTPUT_FILE
from utils import fetch_url
from product_parser import extract_product_data

def load_product_urls():
    """Load product URLs from products.txt"""
    with open('products.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scrape_products():
    """Main scraping function"""
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load product URLs
    product_urls = load_product_urls()
    print(f"Loaded {len(product_urls)} product URLs")
    
    products_data = []
    for i, url in enumerate(product_urls, 1):
        print(f"Processing {i}/{len(product_urls)}: {url}")
        
        response = fetch_url(url)
        if not response:
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        product_data = extract_product_data(soup, url)
        
        if product_data:
            products_data.append(product_data)
            print(f"✓ Success: {product_data.get('title')}")
        else:
            print(f"✗ Failed to extract data from {url}")
    
    # Save results
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(products_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nScraping complete. Saved {len(products_data)} products to {output_path}")
    return products_data

if __name__ == "__main__":
    scrape_products()