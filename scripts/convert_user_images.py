"""
Convertit les 10 images PNG fournies en JPEG + WebP pour 320/640/1200,
et les nomme product-1 à product-10 en remplaçant les anciennes.
Usage:
  python scripts/convert_user_images.py
"""
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'images')

PNG_FILES = [
    'Planche à Découper Bambou.png',
    'Support Ordinateur Portable.png',
    'Set de 3 Bols en Bois.png',
    'Organisateur de Bureau.png',
    'Support Téléphone Écologique.png',
    'Plateau de Service Artisanal.png',
    'Set d\'Ustensiles en Bois.png',
    'Support Pot de Plante Moderne.png',
    'Set de 4 Sous-verres.png',
    'Étagère Murale avec Crochets.png'
]

SIZES = [320, 640, 1200]

print('Conversion des images PNG en JPEG + WebP...')
for idx, png_file in enumerate(PNG_FILES, 1):
    png_path = os.path.join(OUT_DIR, png_file)
    if not os.path.exists(png_path):
        print(f'Fichier manquant: {png_file}')
        continue
    try:
        img = Image.open(png_path).convert('RGB')
        orig_w, orig_h = img.size
        aspect_ratio = orig_h / orig_w
        for w in SIZES:
            h = int(w * aspect_ratio)
            resized = img.resize((w, h), Image.LANCZOS)
            jpg_path = os.path.join(OUT_DIR, f'product-{idx}-{w}.jpg')
            webp_path = os.path.join(OUT_DIR, f'product-{idx}-{w}.webp')
            resized.save(jpg_path, 'JPEG', quality=85)
            resized.save(webp_path, 'WEBP', quality=85, method=6)
            print(f'Saved {jpg_path}')
    except Exception as e:
        print(f'Erreur pour {png_file}: {e}')
print('Terminé.')
