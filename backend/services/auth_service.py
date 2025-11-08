from ldap3 import Server, Connection, ALL, NTLM
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config

class AuthService:
    def __init__(self, user_model):
        self.user_model = user_model
        self.ldap_enabled = bool(Config.LDAP_HOST and Config.LDAP_HOST != 'ldap://your-ad-server.com')

    def authenticate_ldap(self, username, password):
        """AD/LDAP ile kimlik doğrulama"""
        if not self.ldap_enabled:
            return None

        try:
            server = Server(Config.LDAP_HOST, get_info=ALL)
            user_dn = f"{username}@{Config.LDAP_HOST.replace('ldap://', '').replace('ldaps://', '')}"

            # Kullanıcı bağlantısı
            conn = Connection(server, user=user_dn, password=password, authentication=NTLM)

            if not conn.bind():
                return None

            # Kullanıcı bilgilerini al
            search_filter = f"(sAMAccountName={username})"
            conn.search(
                Config.LDAP_BASE_DN,
                search_filter,
                attributes=['memberOf', 'displayName', 'mail']
            )

            if not conn.entries:
                return None

            entry = conn.entries[0]
            groups = [g.split(',')[0].replace('CN=', '') for g in entry.memberOf.values]

            # Gerekli grup kontrolü
            if Config.LDAP_REQUIRED_GROUP and Config.LDAP_REQUIRED_GROUP not in groups:
                return None

            # Kullanıcıyı DB'de bul veya oluştur
            user = self.user_model.find_by_username(username)
            if not user:
                user = self.user_model.create({
                    'username': username,
                    'email': entry.mail.value if hasattr(entry, 'mail') else f"{username}@example.com",
                    'full_name': entry.displayName.value if hasattr(entry, 'displayName') else username,
                    'ad_groups': groups,
                    'role': 'admin' if 'Admins' in groups else 'editor'
                })
            else:
                # AD gruplarını güncelle
                self.user_model.update(user['_id'], {'ad_groups': groups})

            conn.unbind()
            return user

        except Exception as e:
            print(f"LDAP authentication error: {e}")
            return None

    def authenticate_local(self, username, password):
        """Yerel kimlik doğrulama (AD olmadığında)"""
        user = self.user_model.find_by_username(username)
        if not user:
            return None

        if not self.user_model.verify_password(user, password):
            return None

        return user

    def authenticate(self, username, password):
        """Kimlik doğrulama (önce LDAP, sonra local)"""
        # LDAP etkinse önce onu dene
        if self.ldap_enabled:
            user = self.authenticate_ldap(username, password)
            if user:
                self.user_model.update_last_login(user['_id'])
                return user

        # LDAP başarısız veya devre dışıysa local'i dene
        user = self.authenticate_local(username, password)
        if user:
            self.user_model.update_last_login(user['_id'])
            return user

        return None

    def generate_token(self, user):
        """JWT token oluştur"""
        payload = {
            'user_id': str(user['_id']),
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }
        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
        return token

    def verify_token(self, token):
        """JWT token doğrula"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def token_required(f):
    """Decorator: Token gerektiren endpoint'ler için"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        auth_service = AuthService(None)
        payload = auth_service.verify_token(token)

        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        request.current_user = payload
        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    """Decorator: Admin yetkisi gerektiren endpoint'ler için"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)

    return decorated
