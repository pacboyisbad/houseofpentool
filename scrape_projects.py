import json
import urllib.request
from bs4 import BeautifulSoup

project_urls = [
    "https://mrpentool.com/the-body-shop-campaign",
    "https://mrpentool.com/luxury-cosmetics-logo-design-and-branding",
    "https://mrpentool.com/the-bodyshop-india-the-india-edit",
    "https://mrpentool.com/image-retouching-manipulation-for-shaze",
    "https://mrpentool.com/cloudpop-packaging-design-for-womens-wellness-gummies",
    "https://mrpentool.com/sushi-zen-minimalist-japanese-sushi-brand-nyc",
    "https://mrpentool.com/allagitek-minimalist-high-end-ai-branding",
    "https://mrpentool.com/potapop-chips-canister-packaging-design",
    "https://mrpentool.com/logofolio",
    "https://mrpentool.com/upside-logo-evolution",
    "https://mrpentool.com/animated-icons-for-tromdel",
    "https://mrpentool.com/social-media-posts-for-pulsehound",
    "https://mrpentool.com/vibrant-tangyo-cereal-packaging-design"
]

projects_data = []

req = urllib.request.Request("https://mrpentool.com/work", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # In squarespace/standard portfolio sites, usually they are in a grid
        # Let's try to extract img src and titles directly from the work page first, 
        # as it's faster than visiting every single URL if it's a gallery
        
        links = soup.find_all('a')
        for link in links:
            href = link.get('href', '')
            if any(p.replace('https://mrpentool.com', '') in href for p in project_urls) and href != '/work':
                title = link.text.strip()
                img = link.find('img')
                # Try to get the high res square space image if dataset is there
                img_src = ""
                if img:
                    img_src = img.get('data-src') or img.get('src')
                
                # We need clean titles, often they are empty if inside an image wrapper
                if not title:
                    img_alt = img.get('alt') if img else ""
                    title = img_alt
                    
                # Format URL
                if href.startswith('/'):
                    href = "https://mrpentool.com" + href
                
                if title and img_src:
                    # check dupes
                    if not any(d['url'] == href for d in projects_data):
                        projects_data.append({
                            "title": title,
                            "url": href,
                            "image": img_src
                        })

except Exception as e:
    print(f"Error fetching: {e}")

# If we didn't get perfect data from the gallery alone, we might have to scrape individual pages
if len(projects_data) < 5:
    print("Gallery scrape didn't find enough structured data. Attempting individual pages...")
    projects_data = [] # Reset
    for url in project_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                
                title = soup.title.string.strip() if soup.title else url.split('/')[-1].replace('-', ' ').title()
                
                # Find first good representative image
                img_src = ""
                images = soup.find_all('img')
                for img in images:
                    src = img.get('data-src') or img.get('src')
                    if src and ('images.squarespace-cdn.com' in src or 'format=' in src):
                        img_src = src
                        break
                        
                projects_data.append({
                    "title": title.replace(" — Udbhav Midha", "").replace("Udbhav Midha - ", ""),
                    "url": url,
                    "image": img_src
                })
                print(f"Scraped {title}")
        except Exception as e:
            print(f"Error on {url}: {e}")

with open('scraped_projects.json', 'w') as f:
    json.dump(projects_data, f, indent=2)

print(f"Successfully exported {len(projects_data)} projects to scraped_projects.json")
