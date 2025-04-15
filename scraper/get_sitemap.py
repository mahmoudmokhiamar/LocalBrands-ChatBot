import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
STORE_URL = "https://gonative.eg"
MAIN_SITEMAP = f"{STORE_URL}/sitemap.xml"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Helper functions
def fetch_url(url):
    """Fetch URL with retries and delays"""
    try:
        time.sleep(0.5)  # Respectful delay
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_sitemap(xml_content):
    """Parse XML sitemap and return all URLs"""
    soup = BeautifulSoup(xml_content, 'xml')
    return [loc.text.strip() for loc in soup.find_all('loc') if loc.text.strip()]

def process_sitemap(sitemap_url):
    """Process individual sitemap and categorize URLs"""
    content = fetch_url(sitemap_url)
    if not content:
        return {'products': [], 'collections': [], 'other': []}
    
    urls = parse_sitemap(content)
    result = {
        'products': [],
        'collections': [],
        'other': []
    }
    
    for url in urls:
        if '/products/' in url:
            result['products'].append(url)
        elif '/collections/' in url and not any(x in url for x in ['filter', 'sort_by']):
            result['collections'].append(url)
        else:
            result['other'].append(url)
    
    print(f"Processed {sitemap_url}: {len(urls)} URLs found")
    return result

def get_all_sitemap_urls():
    """Main function to get all categorized URLs"""
    # Step 1: Fetch main sitemap index
    main_sitemap = fetch_url(MAIN_SITEMAP)
    if not main_sitemap:
        return None
    
    # Step 2: Get all sub-sitemaps
    sitemap_urls = parse_sitemap(main_sitemap)
    print(f"Found {len(sitemap_urls)} sub-sitemaps to process")
    
    # Step 3: Process all sitemaps in parallel
    final_results = {
        'products': [],
        'collections': [],
        'other': []
    }
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_sitemap, sitemap_urls))
    
    # Combine results
    for result in results:
        final_results['products'].extend(result['products'])
        final_results['collections'].extend(result['collections'])
        final_results['other'].extend(result['other'])
    
    # Deduplicate
    for key in final_results:
        final_results[key] = list(set(final_results[key]))
    
    return final_results

if __name__ == "__main__":
    print(f"Starting sitemap processing for {STORE_URL}")
    all_urls = get_all_sitemap_urls()
    
    if all_urls:
        print("\nFinal Results:")
        print(f"Total Products: {len(all_urls['products'])}")
        print(f"Total Collections: {len(all_urls['collections'])}")
        print(f"Other URLs: {len(all_urls['other'])}")
        
        # Save to files
        with open('products.txt', 'w') as f:
            f.write("\n".join(all_urls['products']))
        
        with open('collections.txt', 'w') as f:
            f.write("\n".join(all_urls['collections']))
        
        print("\nSample Product URLs:")
        for url in all_urls['products'][:3]:
            print(f"- {url}")
        
        print("\nSample Collection URLs:")
        for url in all_urls['collections'][:3]:
            print(f"- {url}")
    else:
        print("Failed to process sitemaps")