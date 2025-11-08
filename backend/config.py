import os
from datetime import timedelta

class Config:
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin')

    # S3/MinIO
    S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'http://localhost:9000')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', 'minioadmin')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', 'minioadmin123')
    S3_BUCKET = os.getenv('S3_BUCKET', 'genaiwiki-media')

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # AD/LDAP Configuration (Opsiyonel - varsayılan değerler)
    LDAP_HOST = os.getenv('LDAP_HOST', 'ldap://your-ad-server.com')
    LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'DC=example,DC=com')
    LDAP_USER_DN = os.getenv('LDAP_USER_DN', 'CN=Users')
    LDAP_GROUP_DN = os.getenv('LDAP_GROUP_DN', 'CN=Groups')
    LDAP_BIND_USER = os.getenv('LDAP_BIND_USER', '')
    LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD', '')
    LDAP_REQUIRED_GROUP = os.getenv('LDAP_REQUIRED_GROUP', 'ContentEditors')

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'pdf'}
