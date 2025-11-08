import boto3
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError
import os
from uuid import uuid4
from datetime import datetime
from config import Config

class S3Service:
    def __init__(self):
        # MinIO/S3 client oluştur
        self.s3_client = boto3.client(
            's3',
            endpoint_url=Config.S3_ENDPOINT,
            aws_access_key_id=Config.S3_ACCESS_KEY,
            aws_secret_access_key=Config.S3_SECRET_KEY,
            config=BotoConfig(signature_version='s3v4'),
            region_name='us-east-1'
        )
        self.bucket_name = Config.S3_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Bucket'ın var olduğundan emin ol, yoksa oluştur"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                # Public read policy ekle
                bucket_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PublicRead",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                        }
                    ]
                }
                self.s3_client.put_bucket_policy(
                    Bucket=self.bucket_name,
                    Policy=str(bucket_policy).replace("'", '"')
                )
            except ClientError as e:
                print(f"Error creating bucket: {e}")

    def upload_file(self, file_obj, filename, content_type=None):
        """Dosya yükle"""
        try:
            # Benzersiz dosya adı oluştur
            ext = os.path.splitext(filename)[1]
            unique_filename = f"{datetime.now().strftime('%Y/%m/%d')}/{uuid4().hex}{ext}"

            # Content type belirle
            if not content_type:
                content_type = self._get_content_type(ext)

            # S3'e yükle
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                unique_filename,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'
                }
            )

            # URL oluştur
            url = f"{Config.S3_ENDPOINT}/{self.bucket_name}/{unique_filename}"

            return {
                'success': True,
                'url': url,
                's3_key': unique_filename,
                'filename': unique_filename,
                'content_type': content_type
            }

        except ClientError as e:
            print(f"Upload error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def delete_file(self, s3_key):
        """Dosya sil"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return {'success': True}
        except ClientError as e:
            print(f"Delete error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_file_url(self, s3_key):
        """Dosya URL'sini döndür"""
        return f"{Config.S3_ENDPOINT}/{self.bucket_name}/{s3_key}"

    def _get_content_type(self, ext):
        """Dosya uzantısından content type belirle"""
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.pdf': 'application/pdf',
            '.svg': 'image/svg+xml'
        }
        return content_types.get(ext.lower(), 'application/octet-stream')

    def allowed_file(self, filename):
        """Dosya uzantısının izinli olup olmadığını kontrol et"""
        ext = os.path.splitext(filename)[1].lstrip('.')
        return ext.lower() in Config.ALLOWED_EXTENSIONS
