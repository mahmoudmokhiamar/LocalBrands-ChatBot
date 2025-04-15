# product_parser.py
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
from config import BASE_URL

def extract_product_data(soup, url):
    """Extract structured product data from HTML"""
    # Try JSON-LD data first
    script = soup.find('script', type='application/ld+json')
    if script:
        try:
            data = json.loads(script.string)
            product = {
                'title': data.get('name'),
                'description': clean_description(data.get('description')),
                'price': data.get('offers', {}).get('price'),
                'image': data.get('image', {}).get('url'),
                'url': url,
                'brand': data.get('brand', {}).get('name'),
                'sku': data.get('sku'),
                'materials': extract_materials(data.get('description', ''))
            }
            return product
        except json.JSONDecodeError:
            pass

    # Fallback to HTML parsing
    product = {
        'title': get_text(soup, 'h1.product-title, h1.product__title'),
        'description': clean_description(get_text(soup, '.product-description, [data-product-description]')),
        'price': get_text(soup, '.price-item, .product__price'),
        'image': get_attr(soup, '.product-gallery img, .product-single__photo img', 'src'),
        'url': url,
        'materials': extract_materials(get_text(soup, '.product-description, [data-product-description]'))
    }
    
    return {k: v for k, v in product.items() if v}  # Remove empty values

def clean_description(desc):
    """Clean product description text"""
    if not desc:
        return None
    return ' '.join(desc.strip().split())

def extract_materials(text):
    """Extract materials information from text"""
    if not text:
        return []
    
    materials = []
    # Cotton percentage
    cotton_match = re.search(r'(\d+%)?\s*cotton', text, re.IGNORECASE)
    if cotton_match:
        materials.append(cotton_match.group(0).strip())
    
    # Other common materials
    for material in ['polyester', 'wool', 'spandex', 'elastane', 'linen']:
        if material in text.lower():
            materials.append(material)
    
    return materials

def get_text(soup, selector):
    """Safe selector for text extraction"""
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else None

def get_attr(soup, selector, attr):
    """Safe selector for attribute extraction"""
    element = soup.select_one(selector)
    return element.get(attr) if element else None