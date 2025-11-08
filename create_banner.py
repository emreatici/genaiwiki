#!/usr/bin/env python3
"""
1200x300 boyutunda örnek banner oluştur
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 1200x300 boyutunda bir resim oluştur
width = 1200
height = 300
image = Image.new('RGB', (width, height), color='#667eea')

# Gradient efekti
draw = ImageDraw.Draw(image)
for i in range(height):
    # Gradient: #667eea -> #764ba2
    r = int(102 + (118 - 102) * i / height)
    g = int(126 + (75 - 126) * i / height)
    b = int(234 + (162 - 234) * i / height)
    draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))

# Metin ekle
try:
    # Büyük font
    font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 72)
    font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 36)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Ana metin
text_main = "Yapay Zeka ile Geleceği Keşfedin"
text_sub = "En güncel AI teknolojileri ve uygulamaları"

# Metni ortala
draw.text((width//2, height//2 - 30), text_main, fill='white',
          font=font_large, anchor='mm')
draw.text((width//2, height//2 + 40), text_sub, fill=(230, 230, 230),
          font=font_small, anchor='mm')

# Kaydet
output_path = '/Users/onuremreatici/workspace/genaiwiki/middle_banner_1200x300.png'
image.save(output_path, 'PNG')
print(f"✅ Banner oluşturuldu: {output_path}")
print(f"📐 Boyut: {width}x{height} piksel")
