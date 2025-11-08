from flask import Blueprint, request, jsonify
from bson import ObjectId
from services import token_required, admin_required
from models import Article

articles_bp = Blueprint('articles', __name__)

def serialize_article(article):
    """Article nesnesini JSON'a dönüştür"""
    if article:
        article['_id'] = str(article['_id'])
        if article.get('author_id'):
            article['author_id'] = str(article['author_id'])
    return article

def init_articles_routes(db):
    article_model = Article(db)

    @articles_bp.route('', methods=['GET'])
    def get_articles():
        """Tüm makaleleri listele (public)"""
        status = request.args.get('status', 'published')
        category = request.args.get('category')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit

        if status == 'published':
            articles = article_model.find_published(category=category, skip=skip, limit=limit)
            total = article_model.count({'status': 'published', **(({'category': category}) if category else {})})
        else:
            # Draft ve diğer statuslar için auth gerekli
            @token_required
            def _get_all():
                filters = {}
                if status:
                    filters['status'] = status
                if category:
                    filters['category'] = category

                # Eğer author ise, sadece kendi makalelerini göster
                if request.current_user['role'] == 'author':
                    filters['author_id'] = ObjectId(request.current_user['user_id'])

                articles = article_model.find_all(filters=filters, skip=skip, limit=limit)
                total = article_model.count(filters)

                return jsonify({
                    'articles': [serialize_article(a) for a in articles],
                    'total': total,
                    'page': page,
                    'limit': limit,
                    'pages': (total + limit - 1) // limit
                })

            return _get_all()

        return jsonify({
            'articles': [serialize_article(a) for a in articles],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })

    @articles_bp.route('/<article_id>', methods=['GET'])
    def get_article(article_id):
        """Tek makale getir"""
        try:
            # Slug veya ID ile arama
            if ObjectId.is_valid(article_id):
                article = article_model.find_by_id(article_id)
            else:
                article = article_model.find_by_slug(article_id)

            if not article:
                return jsonify({'error': 'Article not found'}), 404

            # Görüntülenme sayısını artır (published ise)
            if article.get('status') == 'published':
                article_model.increment_views(article['_id'])

            return jsonify(serialize_article(article))

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @articles_bp.route('', methods=['POST'])
    @token_required
    def create_article():
        """Yeni makale oluştur"""
        try:
            data = request.get_json()
            data['author_id'] = request.current_user['user_id']
            data['author_name'] = request.current_user['username']

            # Eğer author ise, status otomatik olarak "draft" yapılır
            if request.current_user['role'] == 'author':
                data['status'] = 'draft'

            article = article_model.create(data)
            return jsonify(serialize_article(article)), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @articles_bp.route('/<article_id>', methods=['PUT'])
    @token_required
    def update_article(article_id):
        """Makale güncelle"""
        try:
            data = request.get_json()

            # Mevcut makaleyi kontrol et
            article = article_model.find_by_id(article_id)
            if not article:
                return jsonify({'error': 'Article not found'}), 404

            # Yazar veya admin kontrolü
            # Eğer author_id yoksa, sadece admin editleyebilir
            if article.get('author_id'):
                if str(article['author_id']) != request.current_user['user_id'] and request.current_user['role'] != 'admin':
                    return jsonify({'error': 'Unauthorized'}), 403
            else:
                # author_id yoksa, sadece admin editleyebilir
                if request.current_user['role'] != 'admin':
                    return jsonify({'error': 'Unauthorized - Only admins can edit articles without author'}), 403

            # Eğer author ise, status değiştiremez (sadece admin değiştirebilir)
            if request.current_user['role'] == 'author' and 'status' in data:
                data.pop('status')  # Status değişikliğini engelle

            success = article_model.update(article_id, data)

            if success:
                updated_article = article_model.find_by_id(article_id)
                return jsonify(serialize_article(updated_article))
            else:
                return jsonify({'error': 'Update failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @articles_bp.route('/<article_id>', methods=['DELETE'])
    @token_required
    def delete_article(article_id):
        """Makale sil"""
        try:
            # Mevcut makaleyi kontrol et
            article = article_model.find_by_id(article_id)
            if not article:
                return jsonify({'error': 'Article not found'}), 404

            # Yazar veya admin kontrolü
            # Eğer author_id yoksa, sadece admin silebilir
            if article.get('author_id'):
                if str(article['author_id']) != request.current_user['user_id'] and request.current_user['role'] != 'admin':
                    return jsonify({'error': 'Unauthorized'}), 403
            else:
                # author_id yoksa, sadece admin silebilir
                if request.current_user['role'] != 'admin':
                    return jsonify({'error': 'Unauthorized - Only admins can delete articles without author'}), 403

            success = article_model.delete(article_id)

            if success:
                return jsonify({'success': True, 'message': 'Article deleted'})
            else:
                return jsonify({'error': 'Delete failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return articles_bp
