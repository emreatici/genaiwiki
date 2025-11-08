from datetime import datetime
from bson import ObjectId

class Category:
    def __init__(self, db):
        self.collection = db.categories

    def create(self, data):
        """Yeni kategori oluştur"""
        category = {
            'name': data.get('name'),
            'slug': data.get('slug'),
            'description': data.get('description', ''),
            'icon': data.get('icon', ''),
            'featured_image': data.get('featured_image', ''),
            'order': data.get('order', 0),
            'parent_id': data.get('parent_id'),
            'is_main_menu': data.get('is_main_menu', False),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(category)
        category['_id'] = result.inserted_id
        return category

    def find_by_id(self, category_id):
        """ID'ye göre kategori bul"""
        return self.collection.find_one({'_id': ObjectId(category_id)})

    def find_by_slug(self, slug):
        """Slug'a göre kategori bul"""
        return self.collection.find_one({'slug': slug})

    def find_all(self, parent_id=None):
        """Tüm kategorileri listele"""
        query = {}
        if parent_id is not None:
            query['parent_id'] = parent_id
        cursor = self.collection.find(query).sort('order', 1)
        return list(cursor)

    def find_main_menu(self):
        """Ana menü kategorilerini getir"""
        cursor = self.collection.find({'is_main_menu': True}).sort('order', 1)
        return list(cursor)

    def update(self, category_id, data):
        """Kategori güncelle"""
        data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(category_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def delete(self, category_id):
        """Kategori sil"""
        result = self.collection.delete_one({'_id': ObjectId(category_id)})
        return result.deleted_count > 0
