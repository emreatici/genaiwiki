from flask import Blueprint, request, jsonify
from bson import ObjectId
from services import token_required
from models import Category

categories_bp = Blueprint('categories', __name__)

def serialize_category(category):
    """Category nesnesini JSON'a dönüştür"""
    if category:
        category['_id'] = str(category['_id'])
        if category.get('parent_id'):
            category['parent_id'] = str(category['parent_id'])
    return category

def init_categories_routes(db):
    category_model = Category(db)

    @categories_bp.route('', methods=['GET'])
    def get_categories():
        """Tüm kategorileri listele"""
        parent_id = request.args.get('parent_id')
        main_menu = request.args.get('main_menu', 'false').lower() == 'true'

        if main_menu:
            categories = category_model.find_main_menu()
        else:
            categories = category_model.find_all(parent_id=parent_id)

        return jsonify([serialize_category(c) for c in categories])

    @categories_bp.route('/<category_id>', methods=['GET'])
    def get_category(category_id):
        """Tek kategori getir"""
        try:
            # Slug veya ID ile arama
            if ObjectId.is_valid(category_id):
                category = category_model.find_by_id(category_id)
            else:
                category = category_model.find_by_slug(category_id)

            if not category:
                return jsonify({'error': 'Category not found'}), 404

            return jsonify(serialize_category(category))

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @categories_bp.route('', methods=['POST'])
    @token_required
    def create_category():
        """Yeni kategori oluştur"""
        try:
            data = request.get_json()
            category = category_model.create(data)
            return jsonify(serialize_category(category)), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @categories_bp.route('/<category_id>', methods=['PUT'])
    @token_required
    def update_category(category_id):
        """Kategori güncelle"""
        try:
            data = request.get_json()
            success = category_model.update(category_id, data)

            if success:
                updated_category = category_model.find_by_id(category_id)
                return jsonify(serialize_category(updated_category))
            else:
                return jsonify({'error': 'Update failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @categories_bp.route('/<category_id>', methods=['DELETE'])
    @token_required
    def delete_category(category_id):
        """Kategori sil"""
        try:
            success = category_model.delete(category_id)

            if success:
                return jsonify({'success': True, 'message': 'Category deleted'})
            else:
                return jsonify({'error': 'Delete failed'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return categories_bp
