from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services import token_required, S3Service
from models import Media
import os

media_bp = Blueprint('media', __name__)

def serialize_media(media):
    """Media nesnesini JSON'a dönüştür"""
    if media:
        media['_id'] = str(media['_id'])
        if media.get('uploaded_by'):
            media['uploaded_by'] = str(media['uploaded_by'])
    return media

def init_media_routes(db):
    media_model = Media(db)
    s3_service = S3Service()

    @media_bp.route('', methods=['GET'])
    def get_media_list():
        """Tüm medyaları listele"""
        file_type = request.args.get('type')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        skip = (page - 1) * limit

        media_list = media_model.find_all(file_type=file_type, skip=skip, limit=limit)
        total = media_model.count(file_type=file_type)

        return jsonify({
            'media': [serialize_media(m) for m in media_list],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })

    @media_bp.route('/<media_id>', methods=['GET'])
    def get_media(media_id):
        """Tek medya getir"""
        media = media_model.find_by_id(media_id)
        if not media:
            return jsonify({'error': 'Media not found'}), 404

        return jsonify(serialize_media(media))

    @media_bp.route('/upload', methods=['POST'])
    @token_required
    def upload_media():
        """Medya yükle"""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400

            file = request.files['file']

            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            if not s3_service.allowed_file(file.filename):
                return jsonify({'error': 'File type not allowed'}), 400

            # Dosyayı S3'e yükle
            original_filename = secure_filename(file.filename)
            result = s3_service.upload_file(file, original_filename)

            if not result.get('success'):
                return jsonify({'error': result.get('error', 'Upload failed')}), 500

            # Dosya tipini belirle
            ext = os.path.splitext(original_filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                file_type = 'image'
            elif ext in ['.mp4', '.webm']:
                file_type = 'video'
            else:
                file_type = 'document'

            # Medya kaydı oluştur
            media = media_model.create({
                'filename': result['filename'],
                'original_filename': original_filename,
                'file_type': file_type,
                'mime_type': result['content_type'],
                'size': request.content_length,
                'url': result['url'],
                's3_key': result['s3_key'],
                'alt_text': request.form.get('alt_text', ''),
                'caption': request.form.get('caption', ''),
                'uploaded_by': request.current_user['user_id']
            })

            return jsonify(serialize_media(media)), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @media_bp.route('/<media_id>', methods=['PUT'])
    @token_required
    def update_media(media_id):
        """Medya bilgilerini güncelle"""
        try:
            data = request.get_json()

            # Sadece alt_text ve caption güncellenebilir
            update_data = {}
            if 'alt_text' in data:
                update_data['alt_text'] = data['alt_text']
            if 'caption' in data:
                update_data['caption'] = data['caption']

            success = media_model.update(media_id, update_data)

            if success:
                updated_media = media_model.find_by_id(media_id)
                return jsonify(serialize_media(updated_media))
            else:
                return jsonify({'error': 'Update failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @media_bp.route('/<media_id>', methods=['DELETE'])
    @token_required
    def delete_media(media_id):
        """Medya sil"""
        try:
            media = media_model.find_by_id(media_id)
            if not media:
                return jsonify({'error': 'Media not found'}), 404

            # S3'ten sil
            s3_result = s3_service.delete_file(media['s3_key'])
            if not s3_result.get('success'):
                return jsonify({'error': 'Failed to delete file from storage'}), 500

            # Veritabanından sil
            success = media_model.delete(media_id)

            if success:
                return jsonify({'success': True, 'message': 'Media deleted'})
            else:
                return jsonify({'error': 'Delete failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return media_bp
