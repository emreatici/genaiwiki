#!/bin/bash

# GenAI Wiki - Docker Image Export Script
# Bu script gerekli Docker image'larını offline kullanım için kaydeder

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

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       GenAI Wiki - Docker Image Export Script           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Export klasörü oluştur
EXPORT_DIR="docker-images"
mkdir -p $EXPORT_DIR

print_step "Docker image'ları build ediliyor..."

# Docker Compose ile image'ları build et
docker-compose build

print_success "Image'lar build edildi"

print_step "Docker image'ları kaydediliyor..."

# Gerekli image'ları listele
IMAGES=(
    "mongo:7.0"
    "minio/minio:latest"
    "genaiwiki-backend"
    "genaiwiki-frontend"
)

# Her image'ı kaydet
for image in "${IMAGES[@]}"; do
    # Image adını dosya adına uygun hale getir
    filename=$(echo $image | sed 's/[\/:]/_/g')

    print_step "Kaydediliyor: $image -> $EXPORT_DIR/${filename}.tar"

    docker save -o "$EXPORT_DIR/${filename}.tar" "$image"

    # Dosya boyutunu göster
    size=$(du -h "$EXPORT_DIR/${filename}.tar" | cut -f1)
    print_success "$image kaydedildi (Boyut: $size)"
done

print_step "Proje dosyaları arşivleniyor..."

# Proje dosyalarını tar.gz olarak kaydet (node_modules ve venv hariç)
tar -czf "$EXPORT_DIR/genaiwiki-source.tar.gz" \
    --exclude="node_modules" \
    --exclude="venv" \
    --exclude="__pycache__" \
    --exclude=".git" \
    --exclude="docker-images" \
    --exclude="*.pyc" \
    --exclude="build" \
    --exclude="dist" \
    .

source_size=$(du -h "$EXPORT_DIR/genaiwiki-source.tar.gz" | cut -f1)
print_success "Proje dosyaları arşivlendi (Boyut: $source_size)"

# Toplam boyut
print_step "Toplam boyut hesaplanıyor..."
total_size=$(du -sh "$EXPORT_DIR" | cut -f1)

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              EXPORT İŞLEMİ TAMAMLANDI! 🎉                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📦 Export Klasörü:${NC} $EXPORT_DIR"
echo -e "${BLUE}📊 Toplam Boyut:${NC} $total_size"
echo ""
echo -e "${YELLOW}📋 Kaydedilen Dosyalar:${NC}"
echo ""
ls -lh "$EXPORT_DIR"
echo ""
echo -e "${BLUE}🚀 Offline Kurulum İçin:${NC}"
echo ""
echo -e "  1. ${GREEN}$EXPORT_DIR${NC} klasörünü hedef sisteme kopyalayın"
echo -e "  2. ${GREEN}./import-images.sh${NC} scriptini çalıştırın"
echo -e "  3. ${GREEN}./setup.sh${NC} ile kurulumu yapın"
echo ""
