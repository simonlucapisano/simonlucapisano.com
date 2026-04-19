import urllib.request
import re
import os
from urllib.parse import urljoin

base_url = "https://simonlucapisano.com"
req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    img_urls = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    os.makedirs('public/assets', exist_ok=True)
    count = 0
    for i, img_url in enumerate(set(img_urls)):
        full_url = urljoin(base_url, img_url)
        # Handle protocol-relative URLs
        if full_url.startswith('//'):
            full_url = 'https:' + full_url
        print(f"Downloading: {full_url}")
        
        try:
            img_req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(img_req).read()
            ext = os.path.splitext(full_url.split('?')[0])[1]
            if not ext:
                ext = '.jpg'
            with open(f'public/assets/image_{i}{ext}', 'wb') as f:
                f.write(img_data)
            count += 1
        except Exception as e:
            print(f"Failed to download {full_url}: {e}")
    print(f"Successfully downloaded {count} images.")
except Exception as e:
    print(f"Error fetching page: {e}")
