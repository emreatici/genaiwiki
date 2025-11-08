# GenAI Wiki - Kurulum Kılavuzu

## 🚀 Otomatik Kurulum (Önerilen)

### Ubuntu/Debian Sistemler

Tek komutla tüm kurulumu yapabilirsiniz:

```bash
git clone https://github.com/emreatici/genaiwiki.git
cd genaiwiki
./setup.sh
```

### Script Ne Yapar?

`setup.sh` scripti aşağıdaki adımları otomatik olarak gerçekleştirir:

#### 1. Sistem Kontrolleri
- Docker kurulu mu?
- Docker Compose kurulu mu?
- Gerekli portlar (3000, 5001, 9000, 9001, 27017) kullanılabilir mi?

#### 2. Ortam Yapılandırması
- `.env.example` dosyasından `.env` oluşturur
- Güvenli rastgele anahtarlar üretir:
  - `SECRET_KEY` (Flask)
  - `JWT_SECRET_KEY` (JWT token'lar)
  - `MONGO_PASSWORD` (MongoDB)
  - `MINIO_PASSWORD` (MinIO/S3)

#### 3. Container'ları Başlatır
- MongoDB (veritabanı)
- MinIO (dosya depolama)
- Backend (Flask API)
- Frontend (React UI)

#### 4. Servislerin Hazır Olmasını Bekler
- MongoDB ping test
- MinIO health check
- Backend API health check
- Frontend bundle build

#### 5. MinIO Yapılandırması
- `genaiwiki-media` bucket'ını oluşturur
- Public download erişimi yapılandırır

#### 6. İlk Admin Kullanıcısı
- Kullanıcı adı, email, tam ad ve şifre bilgilerini ister
- Admin rolü ile kullanıcı oluşturur
- Şifreyi bcrypt ile hashler

#### 7. Bağlantı Testleri
- MongoDB bağlantısı
- MinIO bağlantısı
- Backend API bağlantısı
- Frontend bağlantısı

### Çalıştırma

```bash
./setup.sh
```

Script çalıştırıldığında sizden şu bilgiler istenecek:

```
Admin kullanıcı adı (varsayılan: admin): admin
Admin email (varsayılan: admin@example.com): admin@example.com
Admin tam adı (varsayılan: Admin User): Admin User
Admin şifresi (varsayılan: admin123): ********
Şifreyi tekrar girin: ********
```

### Başarılı Kurulum Sonrası

Script başarıyla tamamlandığında şu bilgileri göreceksiniz:

```
╔══════════════════════════════════════════════════════════╗
║                   KURULUM TAMAMLANDI! 🎉                 ║
╚══════════════════════════════════════════════════════════╝

📋 Erişim Bilgileri:

  Frontend:      http://localhost:3000
  Backend API:   http://localhost:5001
  MinIO Console: http://localhost:9001

👤 Admin Kullanıcı:

  Kullanıcı Adı: admin
  Email:         admin@example.com
  Şifre:         [girdiğiniz şifre]

🔑 MinIO Bilgileri:

  Kullanıcı:     minioadmin
  Şifre:         [otomatik üretilen]

💡 İpuçları:

  • Logları görmek için:     docker-compose logs -f
  • Container'ları durdurmak: docker-compose down
  • Yeniden başlatmak:       docker-compose restart

🚀 Şimdi http://localhost:3000/login adresine gidip giriş yapabilirsiniz!
```

---

## 🔧 Manuel Kurulum

Eğer otomatik script kullanmak istemiyorsanız, manuel kurulum için [README.md](README.md) dosyasındaki "Manuel Kurulum" bölümüne bakınız.

---

## 🐛 Sorun Giderme

### Script Hataları

#### "Docker kurulu değil"
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker $USER
# Yeniden login yapın
```

#### "Permission denied: ./setup.sh"
```bash
chmod +x setup.sh
./setup.sh
```

#### "Port already in use"
```bash
# Hangi port kullanılıyor kontrol edin
sudo lsof -i :3000
sudo lsof -i :5001
sudo lsof -i :9000
sudo lsof -i :27017

# Kullanılan portu durdurun veya docker-compose.yml'de portları değiştirin
```

### Container Sorunları

#### MongoDB başlamıyor
```bash
# Logları kontrol edin
docker-compose logs mongodb

# Container'ı yeniden başlatın
docker-compose restart mongodb

# Tüm volume'leri temizleyip yeniden başlatın
docker-compose down -v
./setup.sh
```

#### Backend başlamıyor
```bash
# Logları kontrol edin
docker-compose logs backend

# Requirements eksik olabilir
docker-compose exec backend pip install -r requirements.txt
docker-compose restart backend
```

#### Frontend başlamıyor
```bash
# Logları kontrol edin
docker-compose logs frontend

# node_modules eksik olabilir
docker-compose exec frontend npm install
docker-compose restart frontend
```

### Bağlantı Sorunları

#### Backend'e bağlanılamıyor
```bash
# Backend'in çalıştığından emin olun
curl http://localhost:5001/api/health

# Çıktı: {"status":"healthy",...}
```

#### MongoDB'ye bağlanılamıyor
```bash
# MongoDB'nin çalıştığından emin olun
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

#### MinIO'ya bağlanılamıyor
```bash
# MinIO'nun çalıştığından emin olun
curl http://localhost:9000/minio/health/live

# MinIO console'a tarayıcıdan erişin
# http://localhost:9001
```

---

## 🔄 Yeniden Kurulum

Eğer sistemi sıfırdan kurmak isterseniz:

```bash
# Tüm container'ları ve volume'leri silin
docker-compose down -v

# .env dosyasını silin (yeni anahtarlar için)
rm .env

# Setup scriptini yeniden çalıştırın
./setup.sh
```

---

## 📦 Production Deployment

Production ortamı için:

1. **Güvenli Şifreler**: Script otomatik olarak üretir, ancak manuel kurulumda güçlü şifreler kullanın
2. **HTTPS**: Nginx/Caddy ile reverse proxy kurun
3. **Firewall**: Sadece gerekli portları açın (80, 443)
4. **Backup**: MongoDB ve MinIO için düzenli yedekleme ayarlayın
5. **Monitoring**: Container sağlık kontrolü yapın

---

## 🆘 Yardım

Sorun yaşıyorsanız:

1. Script loglarını kontrol edin
2. Docker container loglarını kontrol edin: `docker-compose logs`
3. `.env` dosyasının doğru yapılandırıldığından emin olun
4. GitHub'da issue açın: [Issues](https://github.com/emreatici/genaiwiki/issues)

---

## 📝 Notlar

- Script ilk çalıştırmada birkaç dakika sürebilir (Docker image'ları indirme)
- Minimum 2GB RAM önerilir
- Disk alanı: En az 5GB boş alan
- Internet bağlantısı gereklidir (ilk kurulum için)
