#!/usr/bin/env python3
"""
Eski media URL'lerini düzelt
http://localhost:9000 -> http://localhost:9000 (aslında aynı ama production için değiştirilebilir)
"""
from pymongo import MongoClient
import os

# MongoDB bağlantısı
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin')
client = MongoClient(MONGODB_URI)
db = client.genaiwiki

# Eski URL pattern'i
OLD_URL_PREFIX = "http://localhost:9000"
NEW_URL_PREFIX = "http://localhost:9000"  # Aynı ama değiştirilebilir

# Tüm media kayıtlarını güncelle
media_collection = db.media
result = media_collection.update_many(
    {"url": {"$regex": "^http://localhost:9000"}},
    [{"$set": {"url": {"$concat": [NEW_URL_PREFIX, {"$substr": ["$url", len(OLD_URL_PREFIX), -1]}]}}}]
)

print(f"✓ {result.matched_count} media kaydı bulundu")
print(f"✓ {result.modified_count} media URL'si güncellendi")

# Tüm kategorilerin featured_image'ını güncelle
categories_collection = db.categories
result = categories_collection.update_many(
    {"featured_image": {"$regex": "^http://localhost:9000"}},
    [{"$set": {"featured_image": {"$concat": [NEW_URL_PREFIX, {"$substr": ["$featured_image", len(OLD_URL_PREFIX), -1]}]}}}]
)

print(f"✓ {result.matched_count} kategori featured_image bulundu")
print(f"✓ {result.modified_count} kategori featured_image güncellendi")

# Tüm makalelerin featured_image'ını güncelle
articles_collection = db.articles
result = articles_collection.update_many(
    {"featured_image": {"$regex": "^http://localhost:9000"}},
    [{"$set": {"featured_image": {"$concat": [NEW_URL_PREFIX, {"$substr": ["$featured_image", len(OLD_URL_PREFIX), -1]}]}}}]
)

print(f"✓ {result.matched_count} makale featured_image bulundu")
print(f"✓ {result.modified_count} makale featured_image güncellendi")

print("\n✅ Tüm URL'ler güncellendi!")
