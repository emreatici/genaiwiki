#!/bin/bash

# GenAI Wiki - Production Setup Script
# Harici MongoDB ve S3 servisleri için

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "\n${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║      GenAI Wiki - Production Kurulum Scripti             ║"
echo "║      (Harici MongoDB ve S3 Servisleri için)              ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 1. Docker Kontrolü
print_step "Docker kontrol ediliyor..."

if ! command -v docker &> /dev/null; then
    print_error "Docker kurulu değil!"
    echo "Docker'ı kurmak için: https://docs.docker.com/engine/install/ubuntu/"
    exit 1
fi
print_success "Docker kurulu: $(docker --version)"

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose kurulu değil!"
    exit 1
fi
print_success "Docker Compose kurulu"

# 2. .env.production Kontrolü
print_step ".env.production dosyası kontrol ediliyor..."

if [ ! -f .env.production ]; then
    print_warning ".env.production dosyası bulunamadı"

    if [ -f .env.production.example ]; then
        print_step ".env.production dosyası oluşturuluyor..."
        cp .env.production.example .env.production

        # Güvenlik anahtarları oluştur
        SECRET_KEY=$(openssl rand -hex 32)
        JWT_SECRET_KEY=$(openssl rand -hex 32)

        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env.production
        sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET_KEY/" .env.production

        print_warning "UYARI: .env.production dosyasını düzenleyin!"
        echo ""
        echo "Lütfen aşağıdaki bilgileri .env.production dosyasına girin:"
        echo "  - MONGODB_URI: Harici MongoDB bağlantı string'i"
        echo "  - S3_ENDPOINT: Harici S3 endpoint URL'i"
        echo "  - S3_PUBLIC_URL: S3 public URL'i"
        echo "  - S3_ACCESS_KEY: S3 access key"
        echo "  - S3_SECRET_KEY: S3 secret key"
        echo ""
        read -p "Düzenlemeyi tamamladınız mı? (e/h): " CONFIRM

        if [ "$CONFIRM" != "e" ]; then
            print_error "Kurulum iptal edildi. .env.production dosyasını düzenleyip tekrar çalıştırın."
            exit 1
        fi
    else
        print_error ".env.production.example dosyası bulunamadı!"
        exit 1
    fi
else
    print_success ".env.production dosyası mevcut"
fi

# .env.production dosyasını oku
source .env.production

# 3. MongoDB Bağlantı Testi
print_step "MongoDB bağlantısı test ediliyor..."

if [ -z "$MONGODB_URI" ] || [ "$MONGODB_URI" = "mongodb://admin:password@your-mongo-host:27017/genaiwiki?authSource=admin" ]; then
    print_error "MONGODB_URI yapılandırılmamış!"
    echo "Lütfen .env.production dosyasında MONGODB_URI değişkenini ayarlayın."
    exit 1
fi

# MongoDB bağlantı testini Python ile yap (mongosh kurulu olmayabilir)
cat > /tmp/test_mongo.py << 'EOF'
from pymongo import MongoClient
import os
import sys

try:
    client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=5000)
    client.server_info()
    print("OK")
    client.close()
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
EOF

if command -v python3 &> /dev/null; then
    MONGO_TEST=$(python3 -c "
from pymongo import MongoClient
import os
import sys
try:
    client = MongoClient('$MONGODB_URI', serverSelectionTimeoutMS=5000)
    client.server_info()
    print('OK')
    client.close()
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)

    if echo "$MONGO_TEST" | grep -q "OK"; then
        print_success "MongoDB bağlantısı başarılı"
    else
        print_error "MongoDB bağlantısı başarısız!"
        echo "$MONGO_TEST"
        exit 1
    fi
else
    print_warning "Python3 bulunamadı, MongoDB testi atlanıyor (container başladıktan sonra test edilecek)"
fi

# 4. S3 Bağlantı Testi
print_step "S3 bağlantısı test ediliyor..."

if [ -z "$S3_ENDPOINT" ] || [ "$S3_ENDPOINT" = "http://your-s3-host:9000" ]; then
    print_error "S3_ENDPOINT yapılandırılmamış!"
    echo "Lütfen .env.production dosyasında S3_ENDPOINT değişkenini ayarlayın."
    exit 1
fi

# S3 endpoint'e HTTP isteği at
S3_TEST=$(curl -s -o /dev/null -w "%{http_code}" "$S3_ENDPOINT" || echo "000")

if [ "$S3_TEST" != "000" ]; then
    print_success "S3 endpoint erişilebilir (HTTP $S3_TEST)"
else
    print_error "S3 endpoint erişilemiyor: $S3_ENDPOINT"
    echo "Lütfen S3_ENDPOINT değişkenini kontrol edin."
    exit 1
fi

# 5. Eski Container'ları Temizle
print_step "Eski container'lar temizleniyor..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
print_success "Eski container'lar temizlendi"

# 6. Backend ve Frontend Container'larını Başlat
print_step "Backend ve Frontend container'ları başlatılıyor..."
docker-compose -f docker-compose.prod.yml up -d --build

print_success "Container'lar başlatıldı"

# 7. Backend'in Hazır Olmasını Bekle
print_step "Backend hazır olana kadar bekleniyor..."
MAX_TRIES=60
COUNTER=0

while [ $COUNTER -lt $MAX_TRIES ]; do
    if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
        print_success "Backend hazır!"
        break
    fi

    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_TRIES ]; then
        print_error "Backend başlatılamadı (timeout)"
        docker-compose -f docker-compose.prod.yml logs backend
        exit 1
    fi

    echo -n "."
    sleep 2
done

# 8. MongoDB Bağlantı Testi (Backend üzerinden)
print_step "Backend üzerinden MongoDB bağlantısı test ediliyor..."

HEALTH_CHECK=$(curl -s http://localhost:5001/api/health)
if echo "$HEALTH_CHECK" | grep -q '"database":"connected"'; then
    print_success "Backend MongoDB bağlantısı başarılı"
else
    print_error "Backend MongoDB bağlantısı başarısız!"
    echo "$HEALTH_CHECK"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

# 9. S3 Bucket Kontrolü ve Oluşturma
print_step "S3 bucket kontrol ediliyor..."

# Python ile S3 bucket kontrolü
cat > /tmp/check_s3_bucket.py << EOF
import boto3
from botocore.client import Config
import os
import sys

try:
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT'),
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
        config=Config(signature_version='s3v4')
    )

    bucket_name = os.getenv('S3_BUCKET')

    # Bucket var mı kontrol et
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"MEVCUT: Bucket '{bucket_name}' mevcut")
    except:
        # Bucket oluştur
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"OLUŞTURULDU: Bucket '{bucket_name}' oluşturuldu")

        # Public read policy ekle
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        import json
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
        print(f"POLICY: Public read policy eklendi")

except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
EOF

docker-compose -f docker-compose.prod.yml exec -T backend python /tmp/check_s3_bucket.py || print_warning "S3 bucket kontrolü yapılamadı (manuel kontrol gerekebilir)"

# 10. İlk Admin Kullanıcısını Oluştur
print_step "İlk admin kullanıcısı oluşturuluyor..."

echo ""
read -p "Admin kullanıcı adı (varsayılan: admin): " ADMIN_USERNAME
ADMIN_USERNAME=${ADMIN_USERNAME:-admin}

read -p "Admin email (varsayılan: admin@example.com): " ADMIN_EMAIL
ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}

read -p "Admin tam adı (varsayılan: Admin User): " ADMIN_FULLNAME
ADMIN_FULLNAME=${ADMIN_FULLNAME:-Admin User}

while true; do
    read -sp "Admin şifresi (varsayılan: admin123): " ADMIN_PASSWORD
    echo
    ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin123}

    read -sp "Şifreyi tekrar girin: " ADMIN_PASSWORD2
    echo
    ADMIN_PASSWORD2=${ADMIN_PASSWORD2:-admin123}

    if [ "$ADMIN_PASSWORD" = "$ADMIN_PASSWORD2" ]; then
        break
    else
        print_error "Şifreler eşleşmiyor, tekrar deneyin."
    fi
done

cat > /tmp/create_admin.py << EOF
from pymongo import MongoClient
import bcrypt
import os
from datetime import datetime

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.genaiwiki

existing_user = db.users.find_one({'username': '$ADMIN_USERNAME'})

if existing_user:
    print("MEVCUT: Admin kullanıcısı zaten mevcut")
else:
    password_hash = bcrypt.hashpw('$ADMIN_PASSWORD'.encode('utf-8'), bcrypt.gensalt())

    user = {
        'username': '$ADMIN_USERNAME',
        'email': '$ADMIN_EMAIL',
        'full_name': '$ADMIN_FULLNAME',
        'password_hash': password_hash,
        'role': 'admin',
        'is_active': True,
        'created_at': datetime.utcnow(),
        'last_login': None,
        'ad_groups': []
    }

    db.users.insert_one(user)
    print("BAŞARILI: Admin kullanıcısı oluşturuldu")

client.close()
EOF

RESULT=$(docker-compose -f docker-compose.prod.yml exec -T backend python /tmp/create_admin.py 2>&1)

if echo "$RESULT" | grep -q "BAŞARILI"; then
    print_success "Admin kullanıcısı oluşturuldu: $ADMIN_USERNAME"
elif echo "$RESULT" | grep -q "MEVCUT"; then
    print_warning "Admin kullanıcısı zaten mevcut: $ADMIN_USERNAME"
else
    print_error "Admin kullanıcısı oluşturulamadı"
    echo "$RESULT"
fi

rm -f /tmp/create_admin.py

# 11. Frontend'in Hazır Olmasını Bekle
print_step "Frontend hazır olana kadar bekleniyor..."
COUNTER=0

while [ $COUNTER -lt $MAX_TRIES ]; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend hazır!"
        break
    fi

    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_TRIES ]; then
        print_warning "Frontend hazır olmadı (arka planda build devam ediyor olabilir)"
        break
    fi

    echo -n "."
    sleep 2
done

# 12. Özet
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            PRODUCTION KURULUM TAMAMLANDI! 🎉             ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Erişim Bilgileri:${NC}"
echo ""
echo -e "  ${GREEN}Frontend:${NC}      http://localhost:3000"
echo -e "  ${GREEN}Backend API:${NC}   http://localhost:5001"
echo ""
echo -e "${BLUE}👤 Admin Kullanıcı:${NC}"
echo ""
echo -e "  ${GREEN}Kullanıcı Adı:${NC} $ADMIN_USERNAME"
echo -e "  ${GREEN}Email:${NC}         $ADMIN_EMAIL"
echo -e "  ${GREEN}Şifre:${NC}         [girdiğiniz şifre]"
echo ""
echo -e "${BLUE}🔗 Harici Servisler:${NC}"
echo ""
echo -e "  ${GREEN}MongoDB:${NC}       ${MONGODB_URI%%@*}@..."
echo -e "  ${GREEN}S3 Endpoint:${NC}   $S3_ENDPOINT"
echo -e "  ${GREEN}S3 Bucket:${NC}     $S3_BUCKET"
echo ""
echo -e "${YELLOW}💡 İpuçları:${NC}"
echo ""
echo -e "  • Logları görmek için:     ${GREEN}docker-compose -f docker-compose.prod.yml logs -f${NC}"
echo -e "  • Container'ları durdurmak: ${GREEN}docker-compose -f docker-compose.prod.yml down${NC}"
echo -e "  • Yeniden başlatmak:       ${GREEN}docker-compose -f docker-compose.prod.yml restart${NC}"
echo ""
echo -e "${BLUE}🚀 Şimdi http://localhost:3000/login adresine gidip giriş yapabilirsiniz!${NC}"
echo ""
