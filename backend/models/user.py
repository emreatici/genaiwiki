from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    def __init__(self, db):
        self.collection = db.users

    def create(self, data):
        """Yeni kullanıcı oluştur"""
        user = {
            'username': data.get('username'),
            'email': data.get('email'),
            'full_name': data.get('full_name'),
            'role': data.get('role', 'editor'),  # admin, editor, viewer
            'is_active': data.get('is_active', True),
            'created_at': datetime.utcnow(),
            'last_login': None,
            'ad_groups': data.get('ad_groups', [])
        }

        # Eğer password varsa hash'le (AD kullanmıyorsak)
        if data.get('password'):
            user['password_hash'] = bcrypt.hashpw(
                data.get('password').encode('utf-8'),
                bcrypt.gensalt()
            )

        result = self.collection.insert_one(user)
        user['_id'] = result.inserted_id
        return user

    def find_by_id(self, user_id):
        """ID'ye göre kullanıcı bul"""
        return self.collection.find_one({'_id': ObjectId(user_id)})

    def find_by_username(self, username):
        """Kullanıcı adına göre bul"""
        return self.collection.find_one({'username': username})

    def find_by_email(self, email):
        """Email'e göre bul"""
        return self.collection.find_one({'email': email})

    def verify_password(self, user, password):
        """Şifre doğrula"""
        if not user.get('password_hash'):
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'),
            user['password_hash']
        )

    def update_last_login(self, user_id):
        """Son giriş zamanını güncelle"""
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'last_login': datetime.utcnow()}}
        )

    def update(self, user_id, data):
        """Kullanıcı güncelle"""
        if data.get('password'):
            data['password_hash'] = bcrypt.hashpw(
                data.get('password').encode('utf-8'),
                bcrypt.gensalt()
            )
            del data['password']

        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def find_all(self):
        """Tüm kullanıcıları listele"""
        return list(self.collection.find())

    def delete(self, user_id):
        """Kullanıcı sil"""
        result = self.collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0
