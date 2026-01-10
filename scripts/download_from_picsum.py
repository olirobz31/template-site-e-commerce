"""
Télécharge des images depuis picsum.photos pour les utiliser localement.
Génère fichiers JPEG et WebP pour les tailles 320, 640, 1200.
Usage:
  pip install requests pillow
  python scripts/download_from_picsum.py
"""
import os
import io
import requests
from PIL import Image

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
os.makedirs(OUT_DIR, exist_ok=True)

IMAGES = {
    'hero': (1200, 800),
    'collection': (1200, 800),
    'about_forest': (800, 600),
    'about_hands': (800, 600),
    'timeline_1': (600, 400),
    'timeline_2': (600, 400),
    'timeline_3': (600, 400),
    'timeline_4': (600, 400),
    'contact_hero': (1200, 800),
    'contact_team': (600, 400),
}

SIZES = [320, 640, 1200]

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; PicsumDownloader/1.0)'}


def download_raw(w, h):
    url = f'https://picsum.photos/{w}/{h}'
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert('RGB')


if __name__ == '__main__':
    print('Téléchargement depuis picsum.photos...')
    for name, (base_w, base_h) in IMAGES.items():
        for w in SIZES:
            # compute height keeping aspect ratio of base
            h = int(w * base_h / base_w)
            try:
                img = download_raw(w, h)
                jpg_path = os.path.join(OUT_DIR, f"{name}-{w}.jpg")
                webp_path = os.path.join(OUT_DIR, f"{name}-{w}.webp")
                img.save(jpg_path, 'JPEG', quality=85)
                img.save(webp_path, 'WEBP', quality=85, method=6)
                print('Wrote', jpg_path)
            except Exception as e:
                print('Erreur pour', name, w, e)
    print('Terminé.')
