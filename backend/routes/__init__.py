from .auth import init_auth_routes
from .articles import init_articles_routes
from .categories import init_categories_routes
from .media import init_media_routes
from .settings import init_settings_routes
from .users import init_users_routes

__all__ = ['init_auth_routes', 'init_articles_routes', 'init_categories_routes', 'init_media_routes', 'init_settings_routes', 'init_users_routes']
