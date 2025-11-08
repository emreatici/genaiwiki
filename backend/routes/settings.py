from flask import Blueprint, request, jsonify
from services import token_required, admin_required
from models import Settings

settings_bp = Blueprint('settings', __name__)

def serialize_settings(settings):
    """Settings nesnesini JSON'a dönüştür"""
    if settings and '_id' in settings:
        settings['_id'] = str(settings['_id'])
    return settings

def init_settings_routes(db):
    settings_model = Settings(db)

    @settings_bp.route('', methods=['GET'])
    def get_settings():
        """Site ayarlarını getir (public)"""
        try:
            settings = settings_model.get()
            return jsonify(serialize_settings(settings))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @settings_bp.route('', methods=['PUT'])
    @admin_required
    def update_settings():
        """Ayarları güncelle (sadece admin)"""
        try:
            data = request.get_json()
            success = settings_model.update(data)

            if success:
                updated_settings = settings_model.get()
                return jsonify(serialize_settings(updated_settings))
            else:
                return jsonify({'error': 'Update failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @settings_bp.route('/reset', methods=['POST'])
    @admin_required
    def reset_settings():
        """Ayarları sıfırla (sadece admin)"""
        try:
            default_settings = settings_model.reset()
            return jsonify(serialize_settings(default_settings))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return settings_bp
