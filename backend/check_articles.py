#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check articles and their images
"""

from pymongo import MongoClient

# MongoDB connection
MONGODB_URI = 'mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin'
client = MongoClient(MONGODB_URI)
db = client['genaiwiki']

# Find all main category articles
articles = db.articles.find({'category': 'main'})

print('Main category articles:')
print('-' * 80)
for article in articles:
    image_status = '✓' if article.get('featured_image') else '✗'
    print(f"{image_status} {article['title']} (slug: {article['slug']})")
    if not article.get('featured_image'):
        print(f"   -> Missing image!")
    else:
        print(f"   -> {article['featured_image']}")

client.close()
