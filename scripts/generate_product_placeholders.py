"""
Génère des placeholders pour les produits: product-1 .. product-10
Créera JPEG + WebP en 320/640/1200 dans `images/`.
Usage: python scripts/generate_product_placeholders.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'images')
os.makedirs(OUT_DIR, exist_ok=True)

SIZES = [320, 640, 1200]
NUM = 10
FONT = ImageFont.load_default()
BG_COLORS = [(199,126,93), (141,110,99), (139,154,126), (232,220,196), (93,64,55)]

for i in range(1, NUM+1):
    label = f'Produit {i}'
    bg = BG_COLORS[i % len(BG_COLORS)]
    for w in SIZES:
        h = int(w * 4 / 3)
        img = Image.new('RGB', (w, h), color=bg)
        draw = ImageDraw.Draw(img)
        fontsize = max(12, int(w / 18))
        try:
            font = ImageFont.truetype('arial.ttf', fontsize)
        except Exception:
            font = FONT
        try:
            bbox = draw.textbbox((0,0), label, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w, text_h = font.getsize(label)
        draw.text(((w - text_w) / 2, (h - text_h) / 2), label, fill=(255,255,255), font=font)
        jpg_path = os.path.join(OUT_DIR, f'product-{i}-{w}.jpg')
        webp_path = os.path.join(OUT_DIR, f'product-{i}-{w}.webp')
        img.save(jpg_path, 'JPEG', quality=80)
        img.save(webp_path, 'WEBP', quality=80, method=6)
        print('Wrote', jpg_path)
print('Done')
