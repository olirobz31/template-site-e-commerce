"""
Télécharge des images réelles pour les produits depuis picsum.photos en utilisant des seeds
et génère JPEG + WebP pour 320/640/1200.
Usage:
  pip install requests pillow
  python scripts/download_real_product_images.py
"""
import os
import io
import requests
from PIL import Image

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
os.makedirs(OUT_DIR, exist_ok=True)

PRODUCTS = [f'product-{i}' for i in range(1, 11)]
SIZES = [320, 640, 1200]
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; PicsumProductDownloader/1.0)'}


def download_seed(seed, w, h):
    url = f'https://picsum.photos/seed/{seed}/{w}/{h}'
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert('RGB')


if __name__ == '__main__':
    print('Téléchargement des images produits depuis picsum.photos (seed)...')
    for prod in PRODUCTS:
        seed = prod  # ex: product-1
        for w in SIZES:
            h = int(w * 3 / 4)
            try:
                img = download_seed(seed, w, h)
                jpg_path = os.path.join(OUT_DIR, f"{prod}-{w}.jpg")
                webp_path = os.path.join(OUT_DIR, f"{prod}-{w}.webp")
                img.save(jpg_path, 'JPEG', quality=85)
                img.save(webp_path, 'WEBP', quality=85, method=6)
                print('Saved', jpg_path)
            except Exception as e:
                print('Erreur pour', prod, w, e)
    print('Terminé.')
