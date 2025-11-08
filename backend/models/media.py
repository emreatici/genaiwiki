from datetime import datetime
from bson import ObjectId

class Media:
    def __init__(self, db):
        self.collection = db.media

    def create(self, data):
        """Yeni medya kaydı oluştur"""
        media = {
            'filename': data.get('filename'),
            'original_filename': data.get('original_filename'),
            'file_type': data.get('file_type'),  # image, video, document
            'mime_type': data.get('mime_type'),
            'size': data.get('size'),  # bytes
            'url': data.get('url'),
            's3_key': data.get('s3_key'),
            'alt_text': data.get('alt_text', ''),
            'caption': data.get('caption', ''),
            'uploaded_by': data.get('uploaded_by'),
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(media)
        media['_id'] = result.inserted_id
        return media

    def find_by_id(self, media_id):
        """ID'ye göre medya bul"""
        return self.collection.find_one({'_id': ObjectId(media_id)})

    def find_all(self, file_type=None, skip=0, limit=50):
        """Tüm medyaları listele"""
        query = {}
        if file_type:
            query['file_type'] = file_type
        cursor = self.collection.find(query).sort('created_at', -1).skip(skip).limit(limit)
        return list(cursor)

    def update(self, media_id, data):
        """Medya bilgilerini güncelle"""
        result = self.collection.update_one(
            {'_id': ObjectId(media_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def delete(self, media_id):
        """Medya kaydını sil"""
        result = self.collection.delete_one({'_id': ObjectId(media_id)})
        return result.deleted_count > 0

    def count(self, file_type=None):
        """Medya sayısını döndür"""
        query = {}
        if file_type:
            query['file_type'] = file_type
        return self.collection.count_documents(query)
