from datetime import datetime

class Settings:
    def __init__(self, db):
        self.collection = db.settings

    def get(self):
        """Site ayarlarını getir (tek doküman)"""
        settings = self.collection.find_one({})
        if not settings:
            # Varsayılan ayarları oluştur
            settings = self._create_default()
        return settings

    def _create_default(self):
        """Varsayılan ayarları oluştur"""
        default_settings = {
            'site_title': 'GenAI Wiki',
            'site_logo': '',
            'site_description': 'Üretken Yapay Zeka Bilgi Bankası',
            'show_logo': True,
            'show_title': True,
            'show_section_titles': True,
            'show_main_section_title': True,
            'homepage_articles_count': 20,
            'banner': {
                'enabled': True,
                'title': 'Üretken yapay zeka dünyasına hoşgeldiniz',
                'subtitle': 'AI teknolojileri hakkında kapsamlı bilgi ve rehberlik',
                'background_image': '',
                'text_color': '#ffffff',
                'overlay_opacity': 0.5
            },
            'menu': {
                'items': []
            },
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(default_settings)
        default_settings['_id'] = result.inserted_id
        return default_settings

    def update(self, data):
        """Ayarları güncelle"""
        settings = self.get()

        # _id ve diğer immutable alanları kaldır
        update_data = {k: v for k, v in data.items() if k not in ['_id', 'created_at']}

        # Güncelleme zamanını ekle
        update_data['updated_at'] = datetime.utcnow()

        # İç içe alanları birleştir
        if 'banner' in update_data and isinstance(update_data['banner'], dict):
            settings['banner'] = {**settings.get('banner', {}), **update_data['banner']}
            update_data['banner'] = settings['banner']

        if 'menu' in update_data and isinstance(update_data['menu'], dict):
            settings['menu'] = {**settings.get('menu', {}), **update_data['menu']}
            update_data['menu'] = settings['menu']

        result = self.collection.update_one(
            {'_id': settings['_id']},
            {'$set': update_data}
        )
        return result.modified_count > 0 or result.matched_count > 0

    def reset(self):
        """Ayarları sıfırla (fabrika ayarlarına dön)"""
        self.collection.delete_many({})
        return self._create_default()
