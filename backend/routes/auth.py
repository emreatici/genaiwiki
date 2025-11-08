from flask import Blueprint, request, jsonify
from services import AuthService
from models import User

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(db):
    user_model = User(db)
    auth_service = AuthService(user_model)

    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Kullanıcı girişi"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        user = auth_service.authenticate(username, password)

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.get('is_active'):
            return jsonify({'error': 'Account is disabled'}), 403

        token = auth_service.generate_token(user)

        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        })

    @auth_bp.route('/me', methods=['GET'])
    def get_current_user():
        """Token'dan kullanıcı bilgisi al"""
        from services import token_required

        @token_required
        def _get_user():
            user = user_model.find_by_id(request.current_user['user_id'])
            if not user:
                return jsonify({'error': 'User not found'}), 404

            return jsonify({
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            })

        return _get_user()

    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Yeni kullanıcı kaydı (sadece development için, production'da kapalı olmalı)"""
        data = request.get_json()

        # Kullanıcı zaten var mı?
        if user_model.find_by_username(data.get('username')):
            return jsonify({'error': 'Username already exists'}), 400

        try:
            user = user_model.create({
                'username': data.get('username'),
                'email': data.get('email'),
                'full_name': data.get('full_name'),
                'password': data.get('password'),
                'role': 'editor'
            })

            token = auth_service.generate_token(user)

            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return auth_bp
