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

### 1. Repository'yi Klonlayın

```bash
cd /Users/onuremreatici/workspace/genaiwiki
```

### 2. Docker ile Başlatın

```bash
docker-compose up -d
```

Bu komut şunları başlatır:
- **MongoDB** - Port 27017
- **MinIO** (S3) - Port 9000 (API), 9001 (Console)
- **Backend** (Flask) - Port 5000
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

### Backend Ayarları

`backend/config.py` dosyasında aşağıdaki ayarları yapabilirsiniz:

```python
# MongoDB
MONGODB_URI = "mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin"

# S3/MinIO
S3_ENDPOINT = "http://localhost:9000"
S3_ACCESS_KEY = "minioadmin"
S3_SECRET_KEY = "minioadmin123"

# AD/LDAP (Opsiyonel)
LDAP_HOST = "ldap://your-ad-server.com"
LDAP_BASE_DN = "DC=example,DC=com"
LDAP_REQUIRED_GROUP = "ContentEditors"
```

### Frontend Ayarları

`frontend/src/services/api.js` dosyasında API URL'sini değiştirebilirsiniz:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

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
