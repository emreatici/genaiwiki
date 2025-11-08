#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix missing featured image in Görüntü Üretme article
"""

from pymongo import MongoClient

# MongoDB connection
MONGODB_URI = 'mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin'
client = MongoClient(MONGODB_URI)
db = client['genaiwiki']

# Update article
result = db.articles.update_one(
    {'slug': 'goruntu-uretme'},
    {'$set': {'featured_image': 'https://images.unsplash.com/photo-1686191128892-c842fff96f9a?w=800'}}
)

if result.modified_count > 0:
    print('✓ Görüntü Üretme makalesine resim eklendi')
else:
    print('! Makale bulunamadı veya zaten güncel')

client.close()
