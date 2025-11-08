#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check author_id in main articles
"""

from pymongo import MongoClient

# MongoDB connection
MONGODB_URI = 'mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin'
client = MongoClient(MONGODB_URI)
db = client['genaiwiki']

# Find all main category articles
articles = db.articles.find({'category': 'main'})

print('Main category articles author check:')
print('-' * 80)
for article in articles:
    has_author = 'author_id' in article
    status = '✓ Has author_id' if has_author else '✗ Missing author_id'
    print(f"{status} - {article['title']}")
    if has_author:
        print(f"   Author ID: {article['author_id']}")
        print(f"   Author Name: {article.get('author_name', 'N/A')}")

client.close()
