from datetime import datetime
from bson import ObjectId

class Article:
    def __init__(self, db):
        self.collection = db.articles

    def create(self, data):
        """Yeni makale oluştur"""
        article = {
            'title': data.get('title'),
            'slug': data.get('slug'),
            'content': data.get('content'),
            'excerpt': data.get('excerpt', ''),
            'author_id': data.get('author_id'),
            'author_name': data.get('author_name'),
            'category': data.get('category'),
            'tags': data.get('tags', []),
            'keywords': data.get('keywords', []),
            'featured_image': data.get('featured_image'),
            'media': data.get('media', []),
            'status': data.get('status', 'draft'),  # draft, published
            'menu_order': data.get('menu_order', 0),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'published_at': datetime.utcnow() if data.get('status') == 'published' else None,
            'views': 0
        }
        result = self.collection.insert_one(article)
        article['_id'] = result.inserted_id
        return article

    def find_by_id(self, article_id):
        """ID'ye göre makale bul"""
        return self.collection.find_one({'_id': ObjectId(article_id)})

    def find_by_slug(self, slug):
        """Slug'a göre makale bul"""
        return self.collection.find_one({'slug': slug})

    def find_all(self, filters=None, skip=0, limit=20, sort_by='created_at', sort_order=-1):
        """Tüm makaleleri listele"""
        query = filters or {}
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        return list(cursor)

    def find_published(self, category=None, skip=0, limit=20):
        """Yayınlanmış makaleleri listele"""
        query = {'status': 'published'}
        if category:
            query['category'] = category
        cursor = self.collection.find(query).sort('published_at', -1).skip(skip).limit(limit)
        return list(cursor)

    def update(self, article_id, data):
        """Makale güncelle"""
        data['updated_at'] = datetime.utcnow()
        if data.get('status') == 'published' and not self.find_by_id(article_id).get('published_at'):
            data['published_at'] = datetime.utcnow()

        result = self.collection.update_one(
            {'_id': ObjectId(article_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def delete(self, article_id):
        """Makale sil"""
        result = self.collection.delete_one({'_id': ObjectId(article_id)})
        return result.deleted_count > 0

    def increment_views(self, article_id):
        """Görüntülenme sayısını artır"""
        self.collection.update_one(
            {'_id': ObjectId(article_id)},
            {'$inc': {'views': 1}}
        )

    def count(self, filters=None):
        """Makale sayısını döndür"""
        query = filters or {}
        return self.collection.count_documents(query)
