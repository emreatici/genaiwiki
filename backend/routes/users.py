from flask import Blueprint, jsonify, request
from models.user import User
from services import token_required
from bson import ObjectId

users_bp = Blueprint('users', __name__)

def init_users_routes(db):
    user_model = User(db)

    def serialize_user(user):
        """Kullanıcı objesini JSON'a çevir"""
        if user:
            user['_id'] = str(user['_id'])
            # Hassas bilgileri çıkar
            user.pop('password_hash', None)
            return user
        return None

    @users_bp.route('', methods=['GET'])
    @token_required
    def get_users():
        """Tüm kullanıcıları listele (sadece admin)"""
        # Sadece admin erişebilir
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        try:
            users = user_model.find_all()
            return jsonify([serialize_user(user) for user in users])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @users_bp.route('', methods=['POST'])
    @token_required
    def create_user():
        """Yeni kullanıcı oluştur (sadece admin)"""
        # Sadece admin oluşturabilir
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        try:
            data = request.get_json()

            # Gerekli alanlar
            required_fields = ['username', 'email', 'password', 'full_name', 'role']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            # Kullanıcı adı ve email kontrolü
            if user_model.find_by_username(data['username']):
                return jsonify({'error': 'Username already exists'}), 400

            if user_model.find_by_email(data['email']):
                return jsonify({'error': 'Email already exists'}), 400

            # Role kontrolü
            if data['role'] not in ['admin', 'author']:
                return jsonify({'error': 'Invalid role. Must be admin or author'}), 400

            # Kullanıcı oluştur
            user_id = user_model.create({
                'username': data['username'],
                'email': data['email'],
                'password': data['password'],
                'full_name': data['full_name'],
                'role': data['role']
            })

            if user_id:
                new_user = user_model.find_by_id(user_id)
                return jsonify(serialize_user(new_user)), 201
            else:
                return jsonify({'error': 'User creation failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @users_bp.route('/<user_id>', methods=['GET'])
    @token_required
    def get_user(user_id):
        """Tek kullanıcı getir"""
        # Sadece admin veya kendi profilini görebilir
        if request.current_user['role'] != 'admin' and str(request.current_user['user_id']) != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        try:
            user = user_model.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify(serialize_user(user))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @users_bp.route('/<user_id>', methods=['PUT'])
    @token_required
    def update_user(user_id):
        """Kullanıcı güncelle"""
        # Sadece admin güncelleyebilir
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        try:
            data = request.get_json()

            # Kullanıcıyı kontrol et
            user = user_model.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Kullanılabilir güncellenebilir alanlar
            update_data = {}
            if 'username' in data:
                update_data['username'] = data['username']
            if 'email' in data:
                update_data['email'] = data['email']
            if 'full_name' in data:
                update_data['full_name'] = data['full_name']
            if 'role' in data:
                update_data['role'] = data['role']
            if 'is_active' in data:
                update_data['is_active'] = data['is_active']
            if 'password' in data:
                update_data['password'] = data['password']

            success = user_model.update(user_id, update_data)

            if success:
                updated_user = user_model.find_by_id(user_id)
                return jsonify(serialize_user(updated_user))
            else:
                return jsonify({'error': 'Update failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @users_bp.route('/<user_id>', methods=['DELETE'])
    @token_required
    def delete_user(user_id):
        """Kullanıcı sil (sadece admin)"""
        # Sadece admin silebilir
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        try:
            # Kendi hesabını silmeyi engelle
            if str(request.current_user['user_id']) == user_id:
                return jsonify({'error': 'Cannot delete your own account'}), 400

            user = user_model.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            success = user_model.delete(user_id)

            if success:
                return jsonify({'success': True, 'message': 'User deleted'})
            else:
                return jsonify({'error': 'Delete failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return users_bp
