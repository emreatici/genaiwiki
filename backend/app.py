from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from routes import (
    init_auth_routes,
    init_articles_routes,
    init_categories_routes,
    init_media_routes,
    init_settings_routes,
    init_users_routes
)

# Flask app oluştur
app = Flask(__name__)
app.config.from_object(Config)

# CORS ayarları
CORS(app, resources={
    r"/api/*": {
        "origins": Config.CORS_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# MongoDB bağlantısı
try:
    mongo_client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Bağlantıyı test et
    mongo_client.server_info()
    db = mongo_client.genaiwiki
    print("✓ MongoDB bağlantısı başarılı")
except Exception as e:
    print(f"✗ MongoDB bağlantı hatası: {e}")
    db = None

# Route'ları kaydet
if db is not None:
    app.register_blueprint(init_auth_routes(db), url_prefix='/api/auth')
    app.register_blueprint(init_articles_routes(db), url_prefix='/api/articles')
    app.register_blueprint(init_categories_routes(db), url_prefix='/api/categories')
    app.register_blueprint(init_media_routes(db), url_prefix='/api/media')
    app.register_blueprint(init_settings_routes(db), url_prefix='/api/settings')
    app.register_blueprint(init_users_routes(db), url_prefix='/api/users')

# Sağlık kontrolü endpoint'i
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'GenAI Wiki Backend',
        'database': 'connected' if db is not None else 'disconnected'
    })

# Ana sayfa
@app.route('/')
def index():
    return jsonify({
        'message': 'GenAI Wiki API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'articles': '/api/articles',
            'categories': '/api/categories',
            'media': '/api/media',
            'health': '/api/health'
        }
    })

# Hata yakalayıcılar
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
