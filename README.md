# Üretken Yapay Zeka Wiki

WordPress benzeri, basit ve güçlü bir içerik yönetim sistemi (CMS). Üretken yapay zeka teknolojileri hakkında makale, resim ve video içeriklerini yönetmek için tasarlanmıştır.

## 🚀 Özellikler

### Backend (Flask)
- 🔐 **AD Grup ile Kimlik Doğrulama** - Active Directory entegrasyonu (opsiyonel)
- 📝 **CRUD API'ler** - Makale, kategori ve medya yönetimi
- 🗄️ **MongoDB** - Esnek ve ölçeklenebilir veritabanı
- 📦 **S3/MinIO** - Resim ve video depolama
- 🔒 **JWT Authentication** - Güvenli token tabanlı kimlik doğrulama

### Frontend (React)
- 🎨 **Modern ve Responsive Tasarım** - Tüm cihazlarda mükemmel görünüm
- ✍️ **Zengin Metin Editörü** - React Quill ile güçlü içerik düzenleme
- 📱 **Admin Panel** - Makale, kategori ve medya yönetimi
- 🖼️ **Medya Yöneticisi** - Sürükle-bırak ile dosya yükleme
- 🏷️ **Kategori ve Etiket Sistemi** - İçerik organizasyonu
- 🔍 **SEO Dostu** - Slug, meta description ve keywords desteği

## 📋 Gereksinimler

- Docker & Docker Compose
- Node.js 18+ (local development için)
- Python 3.11+ (local development için)

## 🛠️ Kurulum

### 🚀 Hızlı Kurulum (Otomatik - Ubuntu)

Tek komutla tüm kurulum ve yapılandırmayı yapmak için:

```bash
git clone https://github.com/emreatici/genaiwiki.git
cd genaiwiki
./setup.sh
```

Bu script otomatik olarak:
- ✅ Docker ve sistem gereksinimlerini kontrol eder
- ✅ `.env` dosyasını oluşturur ve güvenli anahtarlar üretir
- ✅ Docker container'larını başlatır
- ✅ MongoDB ve MinIO'nun hazır olmasını bekler
- ✅ MinIO bucket'ını yapılandırır
- ✅ İlk admin kullanıcısını oluşturur
- ✅ Tüm bağlantıları test eder

**Script çalıştırıldıktan sonra admin kullanıcı bilgilerini gireceksiniz ve sistem hazır olacak!**

---

### 🏢 Production Kurulum (Harici MongoDB ve S3)

Eğer MongoDB ve S3 servisleriniz ayrı sistemlerde çalışıyorsa:

```bash
# Proje dosyalarını kopyalayın
cd genaiwiki

# .env.production dosyasını oluşturun
cp .env.production.example .env.production

# .env.production dosyasını düzenleyin ve harici servis bilgilerinizi girin
nano .env.production

# Production kurulum scriptini çalıştırın
./setup-production.sh
```

Bu script:
- ✅ Harici MongoDB bağlantısını test eder
- ✅ Harici S3 bağlantısını test eder
- ✅ S3 bucket'ını kontrol eder/oluşturur
- ✅ Sadece Backend ve Frontend container'larını başlatır
- ✅ İlk admin kullanıcısını oluşturur

**Not:** Bu kurulum `docker-compose.prod.yml` dosyasını kullanır ve MongoDB/MinIO container'larını başlatmaz.

---

### 📋 Manuel Kurulum

Eğer manuel kurulum yapmak isterseniz:

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/emreatici/genaiwiki.git
cd genaiwiki
```

### 2. Environment Değişkenlerini Yapılandırın

`.env` dosyası oluşturun:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin ve **kendi değerlerinizi** girin:

```bash
# MongoDB Ayarları
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=güçlü_şifreniz_buraya
MONGO_INITDB_DATABASE=genaiwiki

MONGODB_URI=mongodb://admin:güçlü_şifreniz_buraya@mongodb:27017/genaiwiki?authSource=admin

# MinIO/S3 Ayarları
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=güçlü_minio_şifreniz

S3_ENDPOINT=http://minio:9000
S3_PUBLIC_URL=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=güçlü_minio_şifreniz
S3_BUCKET=genaiwiki-media

# Flask Güvenlik
SECRET_KEY=uzun-rastgele-gizli-anahtar-buraya
JWT_SECRET_KEY=uzun-rastgele-jwt-anahtari-buraya
FLASK_ENV=production

# Frontend
REACT_APP_API_URL=http://localhost:5001
```

**⚠️ ÖNEMLİ:**
- Production ortamında **mutlaka** güçlü, rastgele şifreler kullanın
- `SECRET_KEY` ve `JWT_SECRET_KEY` en az 32 karakter olmalı
- `.env` dosyası Git'e commit edilmez (`.gitignore`'da)

### 3. Docker ile Başlatın

```bash
docker-compose up -d
```

Bu komut şunları başlatır:
- **MongoDB** - Port 27017
- **MinIO** (S3) - Port 9000 (API), 9001 (Console)
- **Backend** (Flask) - Port 5001
- **Frontend** (React) - Port 3000

### 3. İlk Kullanıcıyı Oluşturun

Backend container'ına bağlanın ve ilk kullanıcıyı oluşturun:

```bash
docker exec -it genaiwiki-backend python
```

Python shell'de:

```python
from pymongo import MongoClient
from models import User
import os

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.genaiwiki

user_model = User(db)
user_model.create({
    'username': 'admin',
    'email': 'admin@example.com',
    'full_name': 'Admin User',
    'password': 'admin123',  # Değiştirin!
    'role': 'admin'
})

print("Admin kullanıcısı oluşturuldu!")
exit()
```

### 4. Uygulamayı Açın

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **MinIO Console**: http://localhost:9001 (minioadmin / minioadmin123)

## 📚 Kullanım

### Giriş Yapma

1. http://localhost:3000/login adresine gidin
2. Kullanıcı adı: `admin`
3. Şifre: Oluşturduğunuz şifre

### Kategori Oluşturma

1. Admin paneline girin
2. "Kategoriler" sekmesine tıklayın
3. Kategori bilgilerini girin:
   - **Kategori Adı**: Örn. "Metin Üretimi"
   - **Slug**: Otomatik oluşturulur (örn. "metin-uretimi")
   - **Açıklama**: Kategori açıklaması
   - **Ana menüde göster**: Ana menüye eklemek için işaretleyin

### Makale Oluşturma

1. Admin panelinde "Makaleler" > "Yeni Makale"
2. Makale bilgilerini doldurun:
   - **Başlık**: Makale başlığı
   - **Slug**: URL için otomatik oluşturulur
   - **Kategori**: Daha önce oluşturduğunuz kategori
   - **İçerik**: Zengin metin editörü ile yazın
   - **Etiketler**: Virgülle ayırarak ekleyin
   - **Durum**: "Taslak" veya "Yayınla"
3. "Kaydet" butonuna tıklayın

### Medya Yükleme

1. Admin panelinde "Medya" sekmesine gidin
2. Dosyaları sürükleyip bırakın veya tıklayarak seçin
3. Yüklenen dosyaların URL'sini kopyalayıp makalelerde kullanın

## 🔧 Yapılandırma

### Environment Değişkenleri

Tüm yapılandırma `.env` dosyası üzerinden yapılır. `backend/config.py` bu değişkenleri otomatik olarak okur.

#### MongoDB Değişkenleri

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `MONGO_INITDB_ROOT_USERNAME` | MongoDB admin kullanıcı adı | `admin` |
| `MONGO_INITDB_ROOT_PASSWORD` | MongoDB admin şifresi | `SecurePass123!` |
| `MONGO_INITDB_DATABASE` | Veritabanı adı | `genaiwiki` |
| `MONGODB_URI` | Tam bağlantı string'i | `mongodb://admin:pass@mongodb:27017/genaiwiki?authSource=admin` |

#### S3/MinIO Değişkenleri

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `MINIO_ROOT_USER` | MinIO kullanıcı adı | `minioadmin` |
| `MINIO_ROOT_PASSWORD` | MinIO şifresi | `SecureMinIO123!` |
| `S3_ENDPOINT` | S3 internal endpoint | `http://minio:9000` |
| `S3_PUBLIC_URL` | S3 public URL (tarayıcıdan) | `http://localhost:9000` |
| `S3_ACCESS_KEY` | S3 access key | `minioadmin` |
| `S3_SECRET_KEY` | S3 secret key | `SecureMinIO123!` |
| `S3_BUCKET` | Bucket adı | `genaiwiki-media` |

#### Flask Değişkenleri

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `SECRET_KEY` | Flask secret key (min 32 char) | `abcdef1234567890...` |
| `JWT_SECRET_KEY` | JWT secret key (min 32 char) | `xyz9876543210...` |
| `FLASK_ENV` | Ortam | `production` veya `development` |

#### LDAP/AD Değişkenleri (Opsiyonel)

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `LDAP_HOST` | LDAP sunucu adresi | `ldap://ad.example.com` |
| `LDAP_BASE_DN` | Base DN | `DC=example,DC=com` |
| `LDAP_USER_DN` | User DN | `CN=Users` |
| `LDAP_GROUP_DN` | Group DN | `CN=Groups` |
| `LDAP_BIND_USER` | Bind kullanıcısı | `bind_user` |
| `LDAP_BIND_PASSWORD` | Bind şifresi | `bind_password` |
| `LDAP_REQUIRED_GROUP` | Gerekli grup | `ContentEditors` |

### Harici Ortamda Çalıştırma

Kendi ortamınızda çalıştırmak için environment değişkenlerini sisteminize tanımlayın:

**Linux/Mac:**
```bash
export MONGODB_URI="mongodb://user:pass@your-mongo-host:27017/genaiwiki"
export S3_ENDPOINT="https://your-s3-endpoint.com"
export S3_ACCESS_KEY="your-access-key"
# ... diğer değişkenler
```

**Windows:**
```cmd
set MONGODB_URI=mongodb://user:pass@your-mongo-host:27017/genaiwiki
set S3_ENDPOINT=https://your-s3-endpoint.com
# ... diğer değişkenler
```

**Docker Compose ile:**
`.env` dosyasını düzenleyin, docker-compose otomatik olarak okur.

## 🏗️ Proje Yapısı

```
genaiwiki/
├── backend/                 # Flask Backend
│   ├── models/             # MongoDB modelleri
│   ├── routes/             # API endpoint'leri
│   ├── services/           # İş mantığı (Auth, S3)
│   ├── utils/              # Yardımcı fonksiyonlar
│   ├── app.py              # Ana uygulama
│   ├── config.py           # Yapılandırma
│   └── requirements.txt    # Python bağımlılıkları
│
├── frontend/               # React Frontend
│   ├── public/            # Statik dosyalar
│   └── src/
│       ├── components/    # React bileşenleri
│       ├── pages/         # Sayfa bileşenleri
│       │   └── admin/     # Admin panel sayfaları
│       ├── services/      # API servisleri
│       └── styles/        # CSS dosyaları
│
└── docker-compose.yml     # Docker yapılandırması
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login` - Giriş yap
- `POST /api/auth/register` - Kayıt ol (development)
- `GET /api/auth/me` - Mevcut kullanıcı bilgisi

### Articles
- `GET /api/articles` - Tüm makaleleri listele
- `GET /api/articles/:id` - Tek makale getir
- `POST /api/articles` - Yeni makale oluştur (auth gerekli)
- `PUT /api/articles/:id` - Makale güncelle (auth gerekli)
- `DELETE /api/articles/:id` - Makale sil (auth gerekli)

### Categories
- `GET /api/categories` - Tüm kategorileri listele
- `GET /api/categories?main_menu=true` - Ana menü kategorileri
- `POST /api/categories` - Yeni kategori (auth gerekli)
- `PUT /api/categories/:id` - Kategori güncelle (auth gerekli)
- `DELETE /api/categories/:id` - Kategori sil (auth gerekli)

### Media
- `GET /api/media` - Tüm medyaları listele
- `POST /api/media/upload` - Medya yükle (auth gerekli)
- `DELETE /api/media/:id` - Medya sil (auth gerekli)

## 🔐 AD Entegrasyonu

Active Directory ile kimlik doğrulama için:

1. `backend/config.py` dosyasında LDAP ayarlarını yapın:

```python
LDAP_HOST = "ldap://your-ad-server.com"
LDAP_BASE_DN = "DC=example,DC=com"
LDAP_REQUIRED_GROUP = "ContentEditors"
```

2. Kullanıcılar AD kimlik bilgileriyle giriş yapabilir
3. İlk girişte otomatik olarak veritabanında kullanıcı oluşturulur

## 🐛 Sorun Giderme

### MongoDB bağlantı hatası
```bash
docker logs genaiwiki-mongo
docker restart genaiwiki-mongo
```

### Backend başlamıyor
```bash
docker logs genaiwiki-backend
docker-compose restart backend
```

### Frontend hatası
```bash
docker logs genaiwiki-frontend
# veya local'de
cd frontend
npm install
npm start
```

### MinIO'ya erişilemiyor
MinIO console'a gidin: http://localhost:9001
- Username: minioadmin
- Password: minioadmin123

Bucket'ın oluşturulduğundan ve public olduğundan emin olun.

## 📝 Development

### Local Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Local Frontend Development

```bash
cd frontend
npm install
npm start
```

## 🚀 Production Deployment

Production için:

1. `backend/config.py` dosyasında güvenlik ayarlarını yapın
2. `SECRET_KEY` ve `JWT_SECRET_KEY` değerlerini değiştirin
3. MongoDB ve MinIO için güçlü şifreler kullanın
4. HTTPS kullanın
5. Register endpoint'ini devre dışı bırakın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje Üretken Yapay Zeka teknolojileri hakkında bilgi paylaşımı için tasarlanmıştır. Altı ana kategori:
1. Metin Üretimi (GPT, Claude, vb.)
2. Görsel Üretimi (DALL-E, Midjourney, vb.)
3. Ses Üretimi (Text-to-Speech, Müzik)
4. Video Üretimi
5. Kod Üretimi
6. Diğer AI Teknolojileri

Her kategori için makaleler oluşturabilir ve blog bölümünde güncel içerikler paylaşabilirsiniz.
