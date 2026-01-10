"""
Génère des images placeholder JPEG + WebP en plusieurs tailles pour le site.
Usage:
  python scripts/generate_placeholders.py
Les images seront écrites dans le dossier `images/`.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'images')
os.makedirs(OUT_DIR, exist_ok=True)

IMAGES = {
    'hero': ('Atelier d\'artisan', (1200, 800)),
    'collection': ('Objets en bois', (1200, 800)),
    'about_forest': ('Forêt durable', (800, 600)),
    'about_hands': ('Mains d\'artisan', (800, 600)),
    'timeline_1': ('Sélection du bois', (600, 400)),
    'timeline_2': ('Façonnage artisanal', (600, 400)),
    'timeline_3': ('Finition naturelle', (600, 400)),
    'timeline_4': ('Contrôle qualité', (600, 400)),
    'contact_hero': ('Service client', (1200, 800)),
    'contact_team': ('Équipe', (600, 400)),
}

SIZES = [320, 640, 1200]

FONT = ImageFont.load_default()

BG_COLORS = [(199,126,93), (141,110,99), (139,154,126), (232,220,196), (93,64,55)]

print('Génération des placeholders...')
for i, (name, (label, aspect)) in enumerate(IMAGES.items()):
    bg = BG_COLORS[i % len(BG_COLORS)]
    for w in SIZES:
        # compute height preserving aspect ratio
        ar_w, ar_h = aspect
        h = int(w * ar_h / ar_w)
        img = Image.new('RGB', (w, h), color=bg)
        draw = ImageDraw.Draw(img)
        # draw label centered
        text = label
        # choose font size relative
        fontsize = max(12, int(w / 20))
        try:
            from PIL import ImageFont
            font = ImageFont.truetype('arial.ttf', fontsize)
        except Exception:
            font = FONT
        # textsize deprecated in some Pillow versions; use textbbox
        try:
            bbox = draw.textbbox((0,0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w, text_h = font.getsize(text)
        draw.text(((w - text_w) / 2, (h - text_h) / 2), text, fill=(255,255,255), font=font)
        jpg_path = os.path.join(OUT_DIR, f"{name}-{w}.jpg")
        webp_path = os.path.join(OUT_DIR, f"{name}-{w}.webp")
        img.save(jpg_path, 'JPEG', quality=80)
        img.save(webp_path, 'WEBP', quality=80)
        print('Wrote', jpg_path, webp_path)

print('Terminé. Fichiers écrits dans', OUT_DIR)
