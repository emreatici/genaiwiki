#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient('mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin')
db = client.genaiwiki

user = db.users.find_one({'username': 'emreatici'})
if not user:
    print("❌ emreatici kullanıcısı bulunamadı!")
    exit(1)

author_id = user['_id']
print(f"✓ Yazar: {user['full_name']}")

categories = list(db.categories.find({'slug': {'$ne': 'main'}}))
print(f"✓ {len(categories)} kategori bulundu\n")

articles_data = {
    'goruntu-uretme': [
        {
            'title': 'DALL-E 3: Metin'den Görüntü Üretiminde Yeni Dönem',
            'slug': 'dalle-3-goruntu-uretimi',
            'excerpt': 'OpenAI\'ın DALL-E 3 modeli, prompt anlama ve görsel kalitede yeni standartlar belirliyor. Sanat, tasarım ve yaratıcılıkta devrim yaratan bu teknoloji hakkında detaylar.',
            'content': '''
<h2>DALL-E 3: Görsel Yaratıcılığın Geleceği</h2>
<p>DALL-E 3, OpenAI tarafından geliştirilen en gelişmiş metin-to-görüntü modelidir. ChatGPT ile entegre çalışarak, kullanıcıların açıklamalarını çok daha iyi anlayan ve yüksek kaliteli görseller üreten bir sistemdir.</p>

<img src="https://images.unsplash.com/photo-1686904423955-b32cf8ff7560?w=800" alt="AI Generated Art" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Temel Özellikler</h3>

<h4>1. Gelişmiş Prompt Anlama</h4>
<p>DALL-E 3, karmaşık ve detaylı açıklamaları çok daha iyi anlar. ChatGPT ile entegrasyonu sayesinde, belirsiz promptları otomatik olarak genişletir ve iyileştirir.</p>

<h4>2. Yüksek Görsel Kalite</h4>
<ul>
    <li>Gerçekçi dokular ve ışıklandırma</li>
    <li>Tutarlı stil ve kompozisyon</li>
    <li>Detaylı objeler ve karakterler</li>
    <li>1024x1024 ve 1792x1024 çözünürlük desteği</li>
</ul>

<img src="https://images.unsplash.com/photo-1617791160505-6f00504e3519?w=800" alt="Digital Art" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h4>3. Güvenlik ve Telif Hakları</h4>
<p>DALL-E 3, yaşayan sanatçıların stillerini taklit etmeyi reddeder ve telif haklarını korur.</p>

<h3>Kullanım Alanları</h3>

<h4>Pazarlama ve Reklam</h4>
<p>Ürün görselleri, sosyal medya içerikleri ve reklam kampanyaları için özgün görseller.</p>

<h4>Eğitim</h4>
<p>Ders materyalleri, infografikler ve görsel sunumlar.</p>

<h4>Sanat ve Tasarım</h4>
<p>Konsept art, illüstrasyon, karakter tasarımı ve dijital sanat eserleri.</p>

<h4>E-ticaret</h4>
<p>Ürün mockup'ları, katalog görselleri ve lifestyle fotoğrafları.</p>

<h3>Prompt Yazma İpuçları</h3>

<ol>
    <li><strong>Spesifik Olun:</strong> "Bir köpek" yerine "Golden Retriever cinsi bir köpek, yeşil çimenlerde koşarken"</li>
    <li><strong>Stil Belirtin:</strong> "dijital art", "fotoğraf", "suluboya", "3D render" gibi</li>
    <li><strong>Kompozisyon:</strong> "geniş açı", "yakın çekim", "kuş bakışı" gibi açılar</li>
    <li><strong>Renkler ve Işık:</strong> "sıcak tonlar", "mavi saatdışı", "dramatik ışıklandırma"</li>
</ol>

<h3>Sınırlamalar</h3>
<ul>
    <li>Gerçek kişilerin görsellerini oluşturamaz</li>
    <li>Şiddet veya yetişkin içerik üretemez</li>
    <li>Telif hakkı korumalı karakterleri taklit edemez</li>
</ul>

<p>DALL-E 3, görsel içerik üretiminde yeni bir çağ başlatıyor ve yaratıcıların hayal güçlerini sınırsızca ifade etmelerini sağlıyor.</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1686904423955-b32cf8ff7560?w=1200',
            'tags': ['dall-e', 'görüntü üretimi', 'ai art', 'openai'],
            'keywords': ['dall-e 3', 'metin to görüntü', 'ai sanat']
        },
        {
            'title': 'Stable Diffusion: Açık Kaynak Görüntü Üretimi',
            'slug': 'stable-diffusion-kullanim',
            'excerpt': 'Açık kaynaklı Stable Diffusion ile kendi bilgisayarınızda profesyonel görsel üretimi. Kurulum, kullanım ve optimize etme rehberi.',
            'content': '''
<h2>Stable Diffusion Nedir?</h2>
<p>Stable Diffusion, Stability AI tarafından geliştirilen açık kaynaklı bir görüntü üretimi modelidir. Kendi bilgisayarınızda çalıştırabileceğiniz, ücretsiz ve güçlü bir araçtır.</p>

<img src="https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800" alt="AI Art Generation" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Avantajları</h3>
<ul>
    <li><strong>Açık Kaynak:</strong> Tamamen ücretsiz ve özelleştirilebilir</li>
    <li><strong>Yerel Çalıştırma:</strong> İnternet bağlantısı gerektirmez</li>
    <li><strong>Gizlilik:</strong> Verileriniz sizde kalır</li>
    <li><strong>Esneklik:</strong> Özel modeller ve eklentilerle genişletilebilir</li>
    <li><strong>Sınırsız Kullanım:</strong> Üretim kotası yok</li>
</ul>

<h3>Sistem Gereksinimleri</h3>

<h4>Minimum</h4>
<ul>
    <li>GPU: NVIDIA GTX 1660 (6GB VRAM)</li>
    <li>RAM: 16GB</li>
    <li>Disk: 20GB boş alan</li>
</ul>

<h4>Önerilen</h4>
<ul>
    <li>GPU: NVIDIA RTX 3060+ (12GB VRAM)</li>
    <li>RAM: 32GB</li>
    <li>Disk: 50GB+ SSD</li>
</ul>

<img src="https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800" alt="Computer Setup" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Kurulum</h3>

<h4>1. Automatic1111 WebUI</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
# Windows için
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
webui-user.bat

# Linux/Mac için
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
./webui.sh
</pre>

<h4>2. Model İndirme</h4>
<p>Hugging Face veya Civitai'den modelleri indirin:</p>
<ul>
    <li>Base Model: Stable Diffusion 1.5 veya SDXL</li>
    <li>Checkpoint modelleri /models/Stable-diffusion/ klasörüne</li>
</ul>

<h3>Temel Kullanım</h3>

<h4>Prompt Yapısı</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
Pozitif Prompt:
a beautiful landscape, mountains, lake, sunset, 
highly detailed, 4k, photorealistic

Negatif Prompt:
ugly, blurry, low quality, distorted, bad anatomy
</pre>

<h4>Önemli Parametreler</h4>
<ul>
    <li><strong>Steps:</strong> 20-30 (kalite vs hız dengesi)</li>
    <li><strong>CFG Scale:</strong> 7-12 (prompt'a ne kadar bağlı kalacağı)</li>
    <li><strong>Sampler:</strong> DPM++ 2M Karras (önerilen)</li>
    <li><strong>Resolution:</strong> 512x512 veya 768x768</li>
</ul>

<h3>İleri Seviye Özellikler</h3>

<h4>ControlNet</h4>
<p>Pose, kenar çizgileri veya derinlik bilgisi ile görsel üretimini kontrol edin.</p>

<h4>LoRA Modelleri</h4>
<p>Spesifik stiller, karakterler veya objeler için ince ayar yapılmış modeller.</p>

<h4>Img2Img</h4>
<p>Varolan bir görseli referans alarak yeni görsel üretin.</p>

<h4>Inpainting/Outpainting</h4>
<p>Görselin belirli kısımlarını değiştirin veya genişletin.</p>

<h3>En İyi Uygulamalar</h3>

<ol>
    <li>Farklı sampling methodları deneyin</li>
    <li>Seed değerlerini kaydedin (tekrarlanabilirlik için)</li>
    <li>Batch mode kullanarak varyasyonlar üretin</li>
    <li>Negatif promptları etkili kullanın</li>
    <li>Yüksek çözünürlük için upscaling uygulayın</li>
</ol>

<h3>Yaygın Sorunlar ve Çözümleri</h3>

<h4>CUDA Out of Memory</h4>
<ul>
    <li>Batch size'ı küçültün</li>
    <li>Resolution'ı düşürün (512x512)</li>
    <li>--medvram parametresini kullanın</li>
</ul>

<h4>Yavaş Üretim</h4>
<ul>
    <li>xFormers extension'ı kurun</li>
    <li>Half precision (fp16) kullanın</li>
    <li>Steps sayısını azaltın</li>
</ul>

<p>Stable Diffusion, profesyonel kalitede görsel üretimi herkesin erişimine açıyor. Biraz deneme yanılma ile harika sonuçlar elde edebilirsiniz!</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1200',
            'tags': ['stable diffusion', 'açık kaynak', 'local ai', 'görsel üretimi'],
            'keywords': ['stable diffusion', 'automatic1111', 'sd webui']
        },
        {
            'title': 'Midjourney: Sanatsal Görsel Üretiminde Lider',
            'slug': 'midjourney-kullanim-rehberi',
            'excerpt': 'Discord tabanlı Midjourney ile etkileyici görseller oluşturun. V6 özellikleri, komutlar ve profesyonel ipuçları.',
            'content': '''
<h2>Midjourney ile Tanışın</h2>
<p>Midjourney, sanatsal ve estetik kalitesi ile öne çıkan bir metin-to-görüntü platformudur. Discord üzerinden erişilebilen bu araç, özellikle konsept sanat ve fantastik görseller için mükemmeldir.</p>

<img src="https://images.unsplash.com/photo-1664365071717-c3b0de0e9bc9?w=800" alt="Midjourney Art" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Midjourney'nin Güçlü Yönleri</h3>
<ul>
    <li>Olağanüstü sanatsal kalite</li>
    <li>Tutarlı stil ve estetik</li>
    <li>Kolay kullanım (Discord bot)</li>
    <li>Aktif topluluk ve ilham kaynakları</li>
    <li>Hızlı üretim süreleri</li>
</ul>

<h3>Başlangıç</h3>

<h4>1. Hesap Oluşturma</h4>
<ol>
    <li>Midjourney.com'a gidin</li>
    <li>"Join the Beta" butonuna tıklayın</li>
    <li>Discord hesabınızla giriş yapın</li>
    <li>Abonelik planı seçin (Basic/Standard/Pro)</li>
</ol>

<h4>2. Discord Sunucusuna Katılma</h4>
<p>Davet linkinden Midjourney Discord sunucusuna katılın.</p>

<h3>Temel Komutlar</h3>

<h4>/imagine</h4>
<p>Görsel üretmek için ana komut:</p>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
/imagine prompt: a mystical forest at twilight, 
glowing mushrooms, fantasy art style, highly detailed
</pre>

<h4>/settings</h4>
<p>Model versiyonu ve parametreleri ayarlayın:</p>
<ul>
    <li>Model Version (V6, V5.2, niji vb.)</li>
    <li>Style (Raw, Default)</li>
    <li>Quality (0.25, 0.5, 1, 2)</li>
</ul>

<img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800" alt="Fantasy Art" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>V6 Özellikleri</h3>

<h4>Gelişmiş Prompt Anlama</h4>
<p>Midjourney V6, daha uzun ve karmaşık promptları anlayabilir. Doğal dil kullanımı gelişti.</p>

<h4>Daha İyi Metin Renderı</h4>
<p>Görsellerde metin yazılması artık mümkün (tırnak içinde belirtin):</p>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
/imagine prompt: a movie poster with text "ADVENTURE" 
at the top, epic landscape --v 6
</pre>

<h4>Parametreler</h4>
<ul>
    <li><strong>--ar</strong>: Aspect ratio (örn: --ar 16:9)</li>
    <li><strong>--style raw</strong>: Daha az stilize, fotoğrafik</li>
    <li><strong>--s</strong>: Stilizasyon seviyesi (0-1000)</li>
    <li><strong>--c</strong>: Kaos/varyasyon (0-100)</li>
</ul>

<h3>İleri Seviye Teknikler</h3>

<h4>Stil Referansları</h4>
<p>Belirli sanatçıları veya stilleri referans gösterin:</p>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
portrait in the style of Rembrandt, oil painting, 
dramatic lighting, baroque era
</pre>

<h4>Multi-Prompts</h4>
<p>İki kavramı :: ile ayırarak dengeleyin:</p>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
cat:: robot:: --v 6
(Yarı kedi, yarı robot)
</pre>

<h4>Image Prompts</h4>
<p>Başka bir görseli referans olarak kullanın:</p>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
[image URL] futuristic city, cyberpunk style --v 6
</pre>

<h4>Remix Mode</h4>
<p>Varyasyon üretirken promptu değiştirme imkanı.</p>

<h3>Kullanım Senaryoları</h3>

<h4>Konsept Sanatı</h4>
<p>Film, oyun ve animasyon projeleri için karakter ve ortam tasarımları.</p>

<h4>Kitap Kapakları</h4>
<p>Roman ve dergi kapakları için etkileyici illüstrasyonlar.</p>

<h4>NFT ve Dijital Sanat</h4>
<p>Özgün dijital sanat eserleri oluşturma.</p>

<h4>Mood Boards</h4>
<p>Tasarım projeleri için görsel ilham panoları.</p>

<h3>En İyi Uygulamalar</h3>

<ol>
    <li><strong>Açıklayıcı Olun:</strong> Detaylı promptlar daha iyi sonuç verir</li>
    <li><strong>Varyasyonları Deneyin:</strong> V1-V4 butonları ile alternatifler üretin</li>
    <li><strong>Upscale Edin:</strong> Beğendiğiniz görseli U butonları ile yükseltin</li>
    <li><strong>Topluluktan Öğrenin:</strong> Diğer kullanıcıların promptlarını inceleyin</li>
    <li><strong>Sabırlı Olun:</strong> İdeal sonuç için iterasyon gerekir</li>
</ol>

<h3>Fiyatlandırma</h3>

<ul>
    <li><strong>Basic:</strong> $10/ay - 200 görs el/ay (Fast mode)</li>
    <li><strong>Standard:</strong> $30/ay - 15 saat Fast mode</li>
    <li><strong>Pro:</strong> $60/ay - 30 saat Fast mode + Stealth mode</li>
</ul>

<p>Midjourney, yaratıcılar için güçlü bir araçtır. Deneme-yanılma ile kendi stilinizi geliştirin ve harika eserler üretin!</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1664365071717-c3b0de0e9bc9?w=1200',
            'tags': ['midjourney', 'ai art', 'discord', 'görsel üretimi'],
            'keywords': ['midjourney', 'midjourney v6', 'discord bot']
        }
    ]
}

created_count = 0
base_date = datetime.now()

for category in categories:
    slug = category['slug']
    if slug not in articles_data:
        print(f"⚠️  {category['name']} - Henüz eklenmedi")
        continue

    print(f"\n📝 {category['name']} için {len(articles_data[slug])} makale...")
    for idx, art in enumerate(articles_data[slug]):
        days_ago = len(articles_data[slug]) - idx
        pub_at = base_date - timedelta(days=days_ago * 2)

        article = {
            'title': art['title'],
            'slug': art['slug'],
            'content': art['content'],
            'excerpt': art['excerpt'],
            'category': slug,
            'author_id': author_id,
            'featured_image': art['featured_image'],
            'tags': art['tags'],
            'keywords': art['keywords'],
            'status': 'published',
            'views': random.randint(150, 900),
            'published_at': pub_at,
            'created_at': pub_at,
            'updated_at': pub_at
        }

        if db.articles.find_one({'slug': article['slug']}):
            print(f"  ⏭️  {art['title']}")
            continue

        db.articles.insert_one(article)
        print(f"  ✅ {art['title']}")
        created_count += 1

print(f"\n🎉 {created_count} yeni makale oluşturuldu!")
