import json
import urllib.request
from bs4 import BeautifulSoup
import time

project_urls = [
    ("THE BODY SHOP - Campaign", "https://mrpentool.com/the-body-shop-campaign"),
    ("Luxury Cosmetics Logo & Branding", "https://mrpentool.com/luxury-cosmetics-logo-design-and-branding"),
    ("The BodyShop India - The India Edit", "https://mrpentool.com/the-bodyshop-india-the-india-edit"),
    ("Image Retouching & Manipulation for SHAZÉ", "https://mrpentool.com/image-retouching-manipulation-for-shaze"),
    ("CloudPop: Women's Wellness Gummies", "https://mrpentool.com/cloudpop-packaging-design-for-womens-wellness-gummies"),
    ("Sushi Zen – Minimalist Japanese Sushi Brand", "https://mrpentool.com/sushi-zen-minimalist-japanese-sushi-brand-nyc"),
    ("Allagitek: High-End AI Branding", "https://mrpentool.com/allagitek-minimalist-high-end-ai-branding"),
    ("Potapop Chips Canister: Packaging Design", "https://mrpentool.com/potapop-chips-canister-packaging-design"),
    ("Logofolio", "https://mrpentool.com/logofolio"),
    ("Upside Logo Evolution", "https://mrpentool.com/upside-logo-evolution"),
    ("Animated Icons for Tromdel", "https://mrpentool.com/animated-icons-for-tromdel"),
    ("Social Media Posts for Pulsehound", "https://mrpentool.com/social-media-posts-for-pulsehound"),
    ("Vibrant TangyO Cereal Packaging Design", "https://mrpentool.com/vibrant-tangyo-cereal-packaging-design"),
]

all_projects = []

for (proj_name, url) in project_urls:
    print(f"\n=== Scraping: {proj_name} ===")
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read()
    except Exception as e:
        print(f"  Error fetching: {e}")
        all_projects.append({"name": proj_name, "url": url, "images": [], "texts": []})
        continue

    soup = BeautifulSoup(html, 'html.parser')

    # Collect all relevant text blocks (paragraphs, headings with actual content)
    text_blocks = []
    # Target content areas
    content_selectors = ['p', 'h1', 'h2', 'h3', 'h4', 'blockquote']
    seen_texts = set()
    for tag in soup.find_all(content_selectors):
        txt = tag.get_text(separator=' ', strip=True)
        # Filter out nav/footer noise (very short or repeated)
        if len(txt) > 20 and txt not in seen_texts:
            text_blocks.append(txt)
            seen_texts.add(txt)

    # Collect all images (prefer cdn.myportfolio or images.squarespace-cdn)
    images = []
    seen_imgs = set()
    img_tags = soup.find_all('img')
    for img in img_tags:
        src = img.get('data-src') or img.get('src') or ''
        if ('cdn.myportfolio.com' in src or 'images.squarespace-cdn.com' in src or 'static1.squarespace.com' in src):
            # Normalize URL
            if src.startswith('//'):
                src = 'https:' + src
            # Get a reasonable size (replace small size hints)
            src_clean = src.split('?')[0]  # Remove query params that may restrict size
            if src_clean not in seen_imgs:
                images.append(src)
                seen_imgs.add(src_clean)

    print(f"  Found {len(images)} images and {len(text_blocks)} text blocks")
    all_projects.append({
        "name": proj_name,
        "url": url,
        "images": images,
        "texts": text_blocks[:8]  # Take up to 8 text segments
    })

    time.sleep(0.5)  # Be polite

with open('scraped_full_projects.json', 'w') as f:
    json.dump(all_projects, f, indent=2)

print(f"\n\nDone! Saved {len(all_projects)} projects to scraped_full_projects.json")
