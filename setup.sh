#!/bin/bash

# GenAI Wiki - Otomatik Kurulum ve Başlatma Scripti
# Ubuntu için tasarlanmıştır

set -e  # Hata durumunda scripti durdur

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logo
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              GenAI Wiki - Kurulum Scripti                ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Fonksiyonlar
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

# 1. Sistem Gereksinimleri Kontrolü
print_step "Sistem gereksinimleri kontrol ediliyor..."

# Docker kontrolü
if ! command -v docker &> /dev/null; then
    print_error "Docker kurulu değil!"
    echo "Docker'ı kurmak için: https://docs.docker.com/engine/install/ubuntu/"
    exit 1
fi
print_success "Docker kurulu: $(docker --version)"

# Docker Compose kontrolü
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose kurulu değil!"
    echo "Docker Compose'u kurmak için: https://docs.docker.com/compose/install/"
    exit 1
fi
print_success "Docker Compose kurulu"

# 2. .env Dosyası Kontrolü ve Oluşturma
print_step ".env dosyası kontrol ediliyor..."

if [ ! -f .env ]; then
    print_warning ".env dosyası bulunamadı, oluşturuluyor..."

    if [ -f .env.example ]; then
        cp .env.example .env
        print_success ".env dosyası .env.example'dan oluşturuldu"

        # Güvenli rastgele anahtarlar oluştur
        print_step "Güvenlik anahtarları oluşturuluyor..."
        SECRET_KEY=$(openssl rand -hex 32)
        JWT_SECRET_KEY=$(openssl rand -hex 32)
        MONGO_PASSWORD=$(openssl rand -hex 16)
        MINIO_PASSWORD=$(openssl rand -hex 16)

        # .env dosyasını güncelle
        sed -i "s/MONGO_INITDB_ROOT_PASSWORD=.*/MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASSWORD/" .env
        sed -i "s/admin123@mongodb/$MONGO_PASSWORD@mongodb/" .env
        sed -i "s/MINIO_ROOT_PASSWORD=.*/MINIO_ROOT_PASSWORD=$MINIO_PASSWORD/" .env
        sed -i "s/S3_SECRET_KEY=.*/S3_SECRET_KEY=$MINIO_PASSWORD/" .env
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET_KEY/" .env

        print_success "Güvenlik anahtarları oluşturuldu ve .env dosyasına kaydedildi"
    else
        print_error ".env.example dosyası bulunamadı!"
        exit 1
    fi
else
    print_success ".env dosyası mevcut"
fi

# 3. Eski Container'ları Temizle
print_step "Eski container'lar temizleniyor..."
docker-compose down -v 2>/dev/null || true
print_success "Eski container'lar temizlendi"

# 4. Docker Container'larını Başlat
print_step "Docker container'ları başlatılıyor..."
docker-compose up -d

print_success "Container'lar başlatıldı"

# 5. MongoDB'nin Hazır Olmasını Bekle
print_step "MongoDB hazır olana kadar bekleniyor..."
MAX_TRIES=30
COUNTER=0

while [ $COUNTER -lt $MAX_TRIES ]; do
    if docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" --quiet > /dev/null 2>&1; then
        print_success "MongoDB hazır!"
        break
    fi

    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_TRIES ]; then
        print_error "MongoDB başlatılamadı (timeout)"
        docker-compose logs mongodb
        exit 1
    fi

    echo -n "."
    sleep 2
done

# 6. MinIO'nun Hazır Olmasını Bekle
print_step "MinIO hazır olana kadar bekleniyor..."
COUNTER=0

while [ $COUNTER -lt $MAX_TRIES ]; do
    if curl -s http://localhost:9000/minio/health/live > /dev/null 2>&1; then
        print_success "MinIO hazır!"
        break
    fi

    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_TRIES ]; then
        print_error "MinIO başlatılamadı (timeout)"
        docker-compose logs minio
        exit 1
    fi

    echo -n "."
    sleep 2
done

# 7. Backend'in Hazır Olmasını Bekle
print_step "Backend hazır olana kadar bekleniyor..."
COUNTER=0

while [ $COUNTER -lt $MAX_TRIES ]; do
    if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
        print_success "Backend hazır!"
        break
    fi

    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_TRIES ]; then
        print_error "Backend başlatılamadı (timeout)"
        docker-compose logs backend
        exit 1
    fi

    echo -n "."
    sleep 2
done

# 8. MinIO Bucket Oluştur
print_step "MinIO bucket oluşturuluyor..."

# .env'den MinIO bilgilerini oku
source .env

# MinIO client ile bucket oluştur
docker-compose exec -T minio mc alias set myminio http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD 2>/dev/null || true
docker-compose exec -T minio mc mb myminio/$S3_BUCKET 2>/dev/null || print_warning "Bucket zaten mevcut"
docker-compose exec -T minio mc anonymous set download myminio/$S3_BUCKET 2>/dev/null || true

print_success "MinIO bucket yapılandırıldı: $S3_BUCKET"

# 9. İlk Admin Kullanıcısını Oluştur
print_step "İlk admin kullanıcısı oluşturuluyor..."

# Kullanıcıdan admin bilgilerini al
echo ""
read -p "Admin kullanıcı adı (varsayılan: admin): " ADMIN_USERNAME
ADMIN_USERNAME=${ADMIN_USERNAME:-admin}

read -p "Admin email (varsayılan: admin@example.com): " ADMIN_EMAIL
ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}

read -p "Admin tam adı (varsayılan: Admin User): " ADMIN_FULLNAME
ADMIN_FULLNAME=${ADMIN_FULLNAME:-Admin User}

# Şifre al (gizli)
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

# Python script ile kullanıcı oluştur
cat > /tmp/create_admin.py << EOF
from pymongo import MongoClient
import bcrypt
import os
from datetime import datetime

# MongoDB bağlantısı
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.genaiwiki

# Admin kullanıcısı var mı kontrol et
existing_user = db.users.find_one({'username': '$ADMIN_USERNAME'})

if existing_user:
    print("MEVCUT: Admin kullanıcısı zaten mevcut")
else:
    # Şifreyi hashle
    password_hash = bcrypt.hashpw('$ADMIN_PASSWORD'.encode('utf-8'), bcrypt.gensalt())

    # Admin kullanıcısı oluştur
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

# Script'i backend container'da çalıştır
RESULT=$(docker-compose exec -T backend python /tmp/create_admin.py 2>&1)

if echo "$RESULT" | grep -q "BAŞARILI"; then
    print_success "Admin kullanıcısı oluşturuldu: $ADMIN_USERNAME"
elif echo "$RESULT" | grep -q "MEVCUT"; then
    print_warning "Admin kullanıcısı zaten mevcut: $ADMIN_USERNAME"
else
    print_error "Admin kullanıcısı oluşturulamadı"
    echo "$RESULT"
fi

# Geçici dosyayı sil
rm -f /tmp/create_admin.py

# 10. Bağlantı Testleri
print_step "Bağlantılar test ediliyor..."

# MongoDB test
if docker-compose exec -T mongodb mongosh $MONGODB_URI --eval "db.adminCommand('ping')" --quiet > /dev/null 2>&1; then
    print_success "MongoDB bağlantısı başarılı"
else
    print_error "MongoDB bağlantısı başarısız"
fi

# MinIO test
if curl -s http://localhost:9000/minio/health/live > /dev/null 2>&1; then
    print_success "MinIO bağlantısı başarılı"
else
    print_error "MinIO bağlantısı başarısız"
fi

# Backend test
HEALTH_CHECK=$(curl -s http://localhost:5001/api/health)
if echo "$HEALTH_CHECK" | grep -q "healthy"; then
    print_success "Backend API bağlantısı başarılı"
else
    print_error "Backend API bağlantısı başarısız"
fi

# Frontend test
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend bağlantısı başarılı"
else
    print_warning "Frontend henüz hazır değil (birkaç saniye sürebilir)"
fi

# 11. Özet
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                   KURULUM TAMAMLANDI! 🎉                 ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Erişim Bilgileri:${NC}"
echo ""
echo -e "  ${GREEN}Frontend:${NC}      http://localhost:3000"
echo -e "  ${GREEN}Backend API:${NC}   http://localhost:5001"
echo -e "  ${GREEN}MinIO Console:${NC} http://localhost:9001"
echo ""
echo -e "${BLUE}👤 Admin Kullanıcı:${NC}"
echo ""
echo -e "  ${GREEN}Kullanıcı Adı:${NC} $ADMIN_USERNAME"
echo -e "  ${GREEN}Email:${NC}         $ADMIN_EMAIL"
echo -e "  ${GREEN}Şifre:${NC}         [girdiğiniz şifre]"
echo ""
echo -e "${BLUE}🔑 MinIO Bilgileri:${NC}"
echo ""
echo -e "  ${GREEN}Kullanıcı:${NC}     $MINIO_ROOT_USER"
echo -e "  ${GREEN}Şifre:${NC}         $MINIO_ROOT_PASSWORD"
echo ""
echo -e "${YELLOW}💡 İpuçları:${NC}"
echo ""
echo -e "  • Logları görmek için:     ${GREEN}docker-compose logs -f${NC}"
echo -e "  • Container'ları durdurmak: ${GREEN}docker-compose down${NC}"
echo -e "  • Yeniden başlatmak:       ${GREEN}docker-compose restart${NC}"
echo ""
echo -e "${BLUE}🚀 Şimdi http://localhost:3000/login adresine gidip giriş yapabilirsiniz!${NC}"
echo ""
