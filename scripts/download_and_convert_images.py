"""
Script pour télécharger des images depuis Unsplash (endpoints source.unsplash.com)
et générer des variantes JPEG + WebP (320, 640, 1200 px).

Usage:
1. Installer dépendances:
   pip install requests pillow
2. Lancer depuis le dossier du projet:
   python scripts/download_and_convert_images.py

Les images seront créées dans le dossier `images/`.

Remarque: source.unsplash.com renvoie une image aléatoire correspondant aux tags.
"""
import os
import io
import requests
from PIL import Image

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
os.makedirs(OUT_DIR, exist_ok=True)

# Définir les images à récupérer : clé -> (query, preferred_aspect)
IMAGES = {
    'hero': ('wood,craft,artisan', (1200, 800)),
    'collection': ('wood,product,handmade', (1200, 800)),
    'about_forest': ('forest,sustainable,trees', (800, 600)),
    'about_hands': ('hands,woodworking,artisan', (800, 600)),
    'timeline_1': ('timber,forest', (600, 400)),
    'timeline_2': ('carpenter,woodworking', (600, 400)),
    'timeline_3': ('wood-finish,oil,beeswax', (600, 400)),
    'timeline_4': ('quality-control,inspection', (600, 400)),
    'contact_hero': ('customer-service,helpdesk', (1200, 800)),
    'contact_team': ('office,team,contact', (600, 400)),
}

# tailles en largeur à générer
SIZES = [320, 640, 1200]

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; ImageFetcher/1.0)'}


def download_image(query, width, height):
    # Utilise endpoint source.unsplash.com pour dimensions
    url = f'https://source.unsplash.com/{width}x{height}/?{query}'
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert('RGB')


def save_variants(img, base_name):
    for w in SIZES:
        # calculer height en conservant ratio approximatif
        ratio = img.width / img.height
        h = int(w / ratio)
        resized = img.resize((w, h), Image.LANCZOS)
        jpg_path = os.path.join(OUT_DIR, f"{base_name}-{w}.jpg")
        webp_path = os.path.join(OUT_DIR, f"{base_name}-{w}.webp")
        resized.save(jpg_path, 'JPEG', quality=80, optimize=True)
        resized.save(webp_path, 'WEBP', quality=80, method=6)
        print(f'Saved {jpg_path} and {webp_path}')


if __name__ == '__main__':
    print('Début du téléchargement et conversion des images...')
    for name, (query, aspect) in IMAGES.items():
        try:
            # Télécharger une grande version proche de la plus grande taille
            target_w = max(SIZES)
            target_h = int(target_w * aspect[1] / aspect[0])
            img = download_image(query, target_w, target_h)
            save_variants(img, name)
        except Exception as e:
            print(f'Erreur pour {name} ({query}):', e)
    print('Terminé. Les fichiers sont dans ./images/')
