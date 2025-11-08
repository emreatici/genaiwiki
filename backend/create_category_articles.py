#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Her kategoriye 3'er makale oluştur
Yazar: emreatici
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# MongoDB bağlantısı
client = MongoClient('mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin')
db = client.genaiwiki

# emreatici kullanıcısını bul
user = db.users.find_one({'username': 'emreatici'})
if not user:
    print("❌ emreatici kullanıcısı bulunamadı!")
    exit(1)

author_id = user['_id']
print(f"✓ Yazar bulundu: {user['full_name']} ({user['username']})")

# Main kategorisi hariç tüm kategorileri al
categories = list(db.categories.find({'slug': {'$ne': 'main'}}))
print(f"✓ {len(categories)} kategori bulundu")

# Her kategori için makaleler
articles_data = {
    'uretken-yz': [
        {
            'title': 'Üretken Yapay Zeka: Geleceğin Teknolojisi',
            'slug': 'uretken-yapay-zeka-gelecek',
            'excerpt': 'Üretken yapay zeka, içerik üretiminde devrim yaratıyor. Metin, görsel ve ses üretimi ile yaratıcılığın yeni boyutlarını keşfedin.',
            'content': '''
<h2>Üretken Yapay Zeka Nedir?</h2>
<p>Üretken yapay zeka (Generative AI), yeni ve özgün içerik üretebilen yapay zeka sistemleridir. Geleneksel yapay zeka sistemleri genellikle sınıflandırma ve tahmin yaparken, üretken yapay zeka tamamen yeni içerikler oluşturabilir.</p>

<img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800" alt="Yapay Zeka Teknolojisi" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Temel Özellikler</h3>
<ul>
    <li><strong>Yaratıcılık:</strong> Özgün içerik üretme yeteneği</li>
    <li><strong>Adaptasyon:</strong> Farklı stillere ve formatlara uyum sağlama</li>
    <li><strong>Ölçeklenebilirlik:</strong> Büyük miktarda içerik üretebilme</li>
    <li><strong>Çeşitlilik:</strong> Metin, görsel, ses gibi farklı modalitelerde çalışma</li>
</ul>

<h3>Çalışma Prensibi</h3>
<p>Üretken yapay zeka modelleri, milyarlarca parametreye sahip derin öğrenme ağları kullanır. Bu modeller, büyük veri setleri üzerinde eğitilerek, verideki örüntüleri ve yapıları öğrenir. Eğitim sonrasında, öğrendiği bilgiyi kullanarak yeni ve özgün içerikler oluşturabilir.</p>

<img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800" alt="Neural Network" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Uygulama Alanları</h3>
<p>Üretken yapay zeka günümüzde birçok alanda kullanılmaktadır:</p>

<h4>1. İçerik Üretimi</h4>
<p>Blog yazıları, sosyal medya içerikleri, ürün açıklamaları ve pazarlama metinleri otomatik olarak üretilebilmektedir.</p>

<h4>2. Tasarım ve Sanat</h4>
<p>Görseller, logolar, illüstrasyonlar ve hatta sanat eserleri yapay zeka ile oluşturulabilir.</p>

<h4>3. Yazılım Geliştirme</h4>
<p>Kod üretimi, hata düzeltme ve dokümantasyon yazımında yardımcı olur.</p>

<h4>4. Eğitim</h4>
<p>Kişiselleştirilmiş eğitim içerikleri ve interaktif öğrenme materyalleri oluşturur.</p>

<h3>Geleceğe Bakış</h3>
<p>Üretken yapay zeka teknolojisi hızla gelişmeye devam ediyor. Gelecekte daha karmaşık, daha gerçekçi ve daha yaratıcı içerikler üretebilen sistemler göreceğiz. Bu teknoloji, iş yapış şekillerimizi ve yaratıcı süreçlerimizi temelden değiştirecek potansiyele sahiptir.</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200',
            'tags': ['yapay zeka', 'teknoloji', 'üretken ai', 'gelecek'],
            'keywords': ['üretken yapay zeka', 'generative ai', 'yapay zeka teknolojisi']
        },
        {
            'title': 'Transformer Mimarisi: Modern Yapay Zekanın Temeli',
            'slug': 'transformer-mimarisi',
            'excerpt': 'Transformer mimarisi, modern yapay zeka sistemlerinin temelini oluşturur. Dikkat mekanizması ile dil modellerinde devrim yaratan bu teknoloji hakkında her şey.',
            'content': '''
<h2>Transformer Nedir?</h2>
<p>Transformer, 2017 yılında Google tarafından "Attention is All You Need" makalesiyle tanıtılan bir sinir ağı mimarisidir. Doğal dil işleme (NLP) alanında devrim yaratmış ve GPT, BERT gibi modern dil modellerinin temelini oluşturmuştur.</p>

<h3>Dikkat Mekanizması (Attention Mechanism)</h3>
<p>Transformer'ın en önemli yeniliği "self-attention" mekanizmasıdır. Bu mekanizma sayesinde model, bir cümledeki her kelimenin diğer kelimelerle ilişkisini anlayabilir.</p>

<img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800" alt="Attention Mechanism" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Mimarinin Bileşenleri</h3>

<h4>1. Encoder-Decoder Yapısı</h4>
<ul>
    <li><strong>Encoder:</strong> Girdi metnini anlayıp vektör temsili oluşturur</li>
    <li><strong>Decoder:</strong> Bu temsilden çıktı metni üretir</li>
</ul>

<h4>2. Multi-Head Attention</h4>
<p>Birden fazla dikkat kafası kullanarak, farklı açılardan ilişkileri yakalayabilir.</p>

<h4>3. Feed-Forward Katmanlar</h4>
<p>Her pozisyon için bağımsız olarak çalışan tam bağlantılı katmanlar.</p>

<h4>4. Positional Encoding</h4>
<p>Kelimelerin sırasını modele öğretmek için pozisyon bilgisi ekler.</p>

<img src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800" alt="Neural Network Architecture" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Avantajları</h3>
<ul>
    <li>Paralel işleme yeteneği</li>
    <li>Uzun mesafeli bağımlılıkları yakalama</li>
    <li>Ölçeklenebilir yapı</li>
    <li>Transfer öğrenme için uygunluk</li>
</ul>

<h3>Modern Uygulamalar</h3>
<p>Transformer mimarisi bugün birçok alanda kullanılmaktadır:</p>
<ul>
    <li><strong>GPT Serisi:</strong> Metin üretimi</li>
    <li><strong>BERT:</strong> Metin anlama</li>
    <li><strong>Vision Transformer:</strong> Görüntü işleme</li>
    <li><strong>Whisper:</strong> Konuşma tanıma</li>
</ul>
''',
            'featured_image': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200',
            'tags': ['transformer', 'deep learning', 'nlp', 'mimari'],
            'keywords': ['transformer mimarisi', 'attention mechanism', 'dil modeli']
        },
        {
            'title': 'Yapay Zeka Etiği ve Sorumlu Kullanım',
            'slug': 'yapay-zeka-etigi',
            'excerpt': 'Yapay zeka sistemlerinin etik kullanımı ve toplumsal etkileri. Önyargı, şeffaflık ve sorumluluk konularında bilmeniz gerekenler.',
            'content': '''
<h2>Yapay Zeka Etiği Neden Önemli?</h2>
<p>Yapay zeka teknolojileri hayatımızın her alanına girerken, bu sistemlerin etik kullanımı kritik önem kazanmıştır. Yanlış kullanıldığında toplumsal zararlara yol açabilecek bu teknolojilerin sorumlu geliştirilmesi gerekir.</p>

<img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800" alt="AI Ethics" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Temel Etik Prensipler</h3>

<h4>1. Adalet ve Tarafsızlık</h4>
<p>Yapay zeka sistemleri, eğitim verilerindeki önyargıları öğrenebilir ve pekiştirebilir. Bu durum, belirli gruplar aleyhine ayrımcı sonuçlara yol açabilir.</p>

<p><strong>Örnek:</strong> İşe alım yapay zekası, geçmiş verilerdeki cinsiyet önyargısını öğrenirse, kadın adayları adaletsiz şekilde elemeye başlayabilir.</p>

<h4>2. Şeffaflık</h4>
<p>Kullanıcılar, yapay zeka sistemlerinin nasıl çalıştığını ve kararları nasıl aldığını anlayabilmelidir.</p>

<ul>
    <li>Açıklanabilir yapay zeka (XAI) geliştirme</li>
    <li>Karar süreçlerini dokümante etme</li>
    <li>Kullanıcıları bilgilendirme</li>
</ul>

<h4>3. Gizlilik ve Veri Koruma</h4>
<p>Yapay zeka sistemleri büyük miktarda kişisel veri işler. Bu verilerin korunması ve etik kullanımı şarttır.</p>

<img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800" alt="Data Privacy" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h4>4. Hesap Verebilirlik</h4>
<p>Yapay zeka sistemlerinin kararlarından kim sorumludur? Bu sorunun net cevabı olmalıdır.</p>

<h3>Potansiyel Riskler</h3>

<h4>Deepfake ve Dezenformasyon</h4>
<p>Gerçekçi sahte içerik üretimi, toplumsal güveni sarsabilir ve manipülasyona açık hale getirebilir.</p>

<h4>İş Gücü Etkileri</h4>
<p>Otomasyon, bazı mesleklerin ortadan kalkmasına neden olabilir. Toplumun bu değişime hazırlanması gerekir.</p>

<h4>Gözetim ve Kontrol</h4>
<p>Yüz tanıma ve davranış analizi gibi teknolojiler, kötüye kullanıldığında bireysel özgürlükleri tehdit edebilir.</p>

<h3>Sorumlu Yapay Zeka Geliştirme</h3>

<p>Yapay zeka geliştiricileri ve kullanıcıları olarak sorumluluklarımız:</p>

<ol>
    <li><strong>Çeşitli ve temsili veri setleri kullanma</strong></li>
    <li><strong>Düzenli önyargı testleri yapma</strong></li>
    <li><strong>Etik kurallar ve politikalar oluşturma</strong></li>
    <li><strong>Paydaşlarla işbirliği yapma</strong></li>
    <li><strong>Sürekli izleme ve iyileştirme</strong></li>
</ol>

<h3>Gelecek İçin Öneriler</h3>
<p>Yapay zeka teknolojisinin topluma faydalı olması için:</p>

<ul>
    <li>Uluslararası etik standartlar geliştirilmeli</li>
    <li>Düzenleyici çerçeveler oluşturulmalı</li>
    <li>Toplumsal farkındalık artırılmalı</li>
    <li>Disiplinler arası işbirliği teşvik edilmeli</li>
</ul>

<p>Etik ve sorumlu yapay zeka geliştirme, sadece teknik bir konu değil, aynı zamanda toplumsal bir sorumluluktur.</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200',
            'tags': ['etik', 'sorumluluk', 'yapay zeka', 'toplum'],
            'keywords': ['yapay zeka etiği', 'ai ethics', 'sorumlu yapay zeka']
        }
    ],
    'dil-modelleri': [
        {
            'title': 'GPT-4: En Gelişmiş Dil Modeli',
            'slug': 'gpt-4-gelismis-dil-modeli',
            'excerpt': 'OpenAI\'ın GPT-4 modeli, doğal dil işlemede yeni standartlar koyuyor. Çok modalite, gelişmiş akıl yürütme ve yaratıcılık özellikleri ile tanışın.',
            'content': '''
<h2>GPT-4: Yeni Nesil Yapay Zeka</h2>
<p>GPT-4 (Generative Pre-trained Transformer 4), OpenAI tarafından geliştirilen en gelişmiş dil modelidir. Önceki versiyonlardan çok daha yetenekli olan bu model, metin anlama, üretme ve akıl yürütmede çığır açıcı performans gösteriyor.</p>

<img src="https://images.unsplash.com/photo-1676277791608-ac5dfc3f30f7?w=800" alt="GPT-4" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Temel Özellikler</h3>

<h4>1. Çok Modalite (Multimodal)</h4>
<p>GPT-4, sadece metin değil, aynı zamanda görsel girdi de işleyebilir. Resimleri anlayabilir ve hakkında detaylı açıklamalar yapabilir.</p>

<h4>2. Gelişmiş Akıl Yürütme</h4>
<p>Karmaşık problemleri çözme, mantıksal çıkarımlar yapma ve çok adımlı görevleri tamamlama konusunda çok başarılı.</p>

<ul>
    <li>Matematiksel problem çözme</li>
    <li>Kod yazma ve hata ayıklama</li>
    <li>Yaratıcı içerik üretme</li>
    <li>Analitik düşünme</li>
</ul>

<h4>3. Bağlam Anlama</h4>
<p>GPT-4, çok uzun metinleri (32,000 token'a kadar) işleyebilir ve bağlamı koruyarak yanıt verebilir.</p>

<img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800" alt="AI Processing" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Performans Metrikleri</h3>

<p>GPT-4, birçok standart testte insan seviyesi veya üstü performans gösteriyor:</p>

<ul>
    <li><strong>BAR Sınavı:</strong> İlk %10'luk dilimde</li>
    <li><strong>SAT Matematik:</strong> 700/800 puan</li>
    <li><strong>Kodlama:</strong> LeetCode problemlerinde %50+ başarı</li>
    <li><strong>Dil Testleri:</strong> Birçok dilde yetkin seviye</li>
</ul>

<h3>Uygulama Alanları</h3>

<h4>İçerik Üretimi</h4>
<p>Blog yazıları, makaleler, sosyal medya içerikleri ve yaratıcı yazarlık.</p>

<h4>Yazılım Geliştirme</h4>
<p>Kod yazma, debugging, dokümantasyon ve kod inceleme.</p>

<h4>Eğitim</h4>
<p>Kişiselleştirilmiş öğretmenlik, soru-cevap ve öğrenme materyali hazırlama.</p>

<h4>İş Süreçleri</h4>
<p>Raporlama, analiz, müşteri hizmetleri ve veri işleme.</p>

<h3>Güvenlik ve Sınırlamalar</h3>

<p>GPT-4, daha güvenli olması için RLHF (Reinforcement Learning from Human Feedback) ile eğitilmiştir:</p>

<ul>
    <li>Zararlı içerik üretimini reddetme</li>
    <li>Önyargılı yanıtları azaltma</li>
    <li>Gerçek bilgi sağlama</li>
</ul>

<p>Ancak bazı sınırlamaları var:</p>
<ul>
    <li>Bazen yanlış bilgi üretebilir (hallüsinasyon)</li>
    <li>Güncel olaylar hakkında bilgisi sınırlı</li>
    <li>Karmaşık hesaplamalarda hata yapabilir</li>
</ul>

<h3>Gelecek Perspektifi</h3>
<p>GPT-4, yapay zeka araştırmalarında önemli bir kilometre taşıdır. Gelecek versiyonlarda daha da gelişmiş yetenekler beklenmektedir.</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1676277791608-ac5dfc3f30f7?w=1200',
            'tags': ['gpt-4', 'openai', 'dil modeli', 'llm'],
            'keywords': ['gpt-4', 'dil modeli', 'chatgpt', 'openai']
        },
        {
            'title': 'Prompt Engineering: Yapay Zekadan En İyi Sonucu Alma',
            'slug': 'prompt-engineering-rehberi',
            'excerpt': 'Dil modellerinden optimal sonuçlar almak için prompt yazma sanatı. İpuçları, teknikler ve en iyi uygulamalar.',
            'content': '''
<h2>Prompt Engineering Nedir?</h2>
<p>Prompt engineering, yapay zeka dil modellerine en etkili şekilde talimat verme sanatıdır. Doğru yazılmış bir prompt, modelin performansını dramatik şekilde artırabilir.</p>

<h3>Temel Prensipler</h3>

<h4>1. Açık ve Spesifik Olun</h4>
<p>Belirsiz ifadeler yerine, net ve detaylı talimatlar verin.</p>

<p><strong>❌ Kötü Örnek:</strong><br/>
"Bir makale yaz"</p>

<p><strong>✅ İyi Örnek:</strong><br/>
"Yapay zeka etiği hakkında 500 kelimelik, akademik üslupda, giriş-gelişme-sonuç yapısında bir makale yaz"</p>

<img src="https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800" alt="Writing Prompts" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h4>2. Bağlam Sağlayın</h4>
<p>Model, yeterli bağlam bilgisi ile daha iyi sonuçlar üretir.</p>

<pre style="background:#f5f5f5; padding:15px; border-radius:5px; overflow-x:auto;">
Rol: Sen bir Python uzmanısın
Görev: Yeni başlayanlara kod örnekleri hazırla
Kısıt: Açıklamaları basit tut, jargon kullanma
Format: Her örnek için açıklama + kod + çıktı
</pre>

<h4>3. Örneklerle Öğretin (Few-Shot Learning)</h4>
<p>Beklediğiniz format ve tonu göstermek için örnekler verin.</p>

<h3>İleri Seviye Teknikler</h3>

<h4>Chain of Thought (CoT)</h4>
<p>Modelden adım adım düşünmesini isteyin:</p>

<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
Soru: 24 elma aldım, 7'sini yedim, sonra 5 tane daha aldım. Kaç elmam var?

Adım adım çözümle:
1. Başlangıç: 24 elma
2. 7 elma yedim: 24 - 7 = 17
3. 5 elma daha aldım: 17 + 5 = 22
Cevap: 22 elma
</pre>

<img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800" alt="Problem Solving" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h4>Self-Consistency</h4>
<p>Aynı soruyu farklı şekillerde sorup, tutarlı cevaplar alın.</p>

<h4>Tree of Thoughts</h4>
<p>Karmaşık problemlerde, farklı çözüm yollarını dallandırarak deneyin.</p>

<h3>Uygulama Örnekleri</h3>

<h4>Kod Üretimi</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px; overflow-x:auto;">
Görev: Python ile bir hesap makinesi yap
Gereksinimler:
- Toplama, çıkarma, çarpma, bölme fonksiyonları
- Hata yönetimi ekle
- Type hints kullan
- Docstring yaz
- Ana program örneği ekle
</pre>

<h4>İçerik Yazımı</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px; overflow-x:auto;">
Hedef Kitle: Lise öğrencileri
Konu: Kuantum bilgisayarlar
Ton: Samimi ve öğretici
Uzunluk: 300-400 kelime
Yapı:
- İlgi çekici giriş
- Basit terimlerle açıklama
- Günlük hayattan benzetme
- Gelecek beklentileri
</pre>

<h3>Yaygın Hatalar ve Çözümleri</h3>

<h4>Hata 1: Çok Genel Promptlar</h4>
<p>Çözüm: Spesifik detaylar ve kısıtlar ekleyin</p>

<h4>Hata 2: Modelin Sınırlarını Görmezden Gelmek</h4>
<p>Çözüm: Gerçekçi beklentiler belirleyin, karmaşık görevleri parçalara ayırın</p>

<h4>Hata 3: Yetersiz Bağlam</h4>
<p>Çözüm: İlgili arka plan bilgisi sağlayın</p>

<h3>Prompt Şablonları</h3>

<h4>Analiz Şablonu</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
[Veri/Metin]

Bu veriyi şu açılardan analiz et:
1. [Açı 1]
2. [Açı 2]
3. [Açı 3]

Her biri için:
- Ana bulgular
- İstatistikler
- Öneriler
</pre>

<h4>Yaratıcı Yazım Şablonu</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
Tür: [Roman/Hikaye/Şiir]
Tema: [Ana tema]
Karakter: [Karakter özellikleri]
Ortam: [Zaman ve mekan]
Ton: [Ciddi/Mizahi/Duygusal]
Uzunluk: [Kelime sayısı]
</pre>

<h3>Sonuç</h3>
<p>İyi prompt engineering, deneme-yanılma gerektirir. Farklı yaklaşımları test edin ve sonuçları karşılaştırın. Zamanla, modelinizden en iyi sonuçları alma konusunda uzmanlaşacaksınız.</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1200',
            'tags': ['prompt engineering', 'llm', 'yapay zeka', 'rehber'],
            'keywords': ['prompt engineering', 'prompt yazma', 'dil modeli kullanımı']
        },
        {
            'title': 'Fine-Tuning: Dil Modellerini Özelleştirme',
            'slug': 'fine-tuning-rehberi',
            'excerpt': 'Önceden eğitilmiş dil modellerini kendi ihtiyaçlarınıza göre uyarlama. Fine-tuning teknikleri, en iyi uygulamalar ve pratik örnekler.',
            'content': '''
<h2>Fine-Tuning Nedir?</h2>
<p>Fine-tuning, önceden eğitilmiş bir dil modelinin belirli bir görev veya alan için yeniden eğitilmesi sürecidir. Sıfırdan model eğitmeye göre çok daha az veri ve hesaplama gücü gerektirir.</p>

<img src="https://images.unsplash.com/photo-1555255707-c07966088b7b?w=800" alt="Model Training" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Neden Fine-Tuning?</h3>

<ul>
    <li><strong>Özelleştirilmiş Performans:</strong> Modelinizi spesifik görevler için optimize edin</li>
    <li><strong>Alan Bilgisi:</strong> Teknik veya endüstriye özel terminoloji öğretin</li>
    <li><strong>Tutarlı Davranış:</strong> Belirli bir tarz veya format sağlayın</li>
    <li><strong>Maliyet Etkinlik:</strong> Sıfırdan eğitime göre çok daha ekonomik</li>
</ul>

<h3>Fine-Tuning Yöntemleri</h3>

<h4>1. Full Fine-Tuning</h4>
<p>Modelin tüm parametrelerini güncelleme. En iyi sonuçları verir ama en pahalı yöntem.</p>

<h4>2. Parameter-Efficient Fine-Tuning (PEFT)</h4>
<p>Modelin sadece küçük bir kısmını güncelleme:</p>

<ul>
    <li><strong>LoRA (Low-Rank Adaptation):</strong> Düşük boyutlu adaptör katmanları ekler</li>
    <li><strong>Adapter Layers:</strong> Küçük eğitilebilir katmanlar ekler</li>
    <li><strong>Prefix Tuning:</strong> Girdi önüne öğrenilebilir prefix ekler</li>
</ul>

<img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800" alt="Data Analysis" style="width:100%; max-width:800px; margin:20px 0; border-radius:8px;" />

<h3>Veri Hazırlama</h3>

<h4>Kaliteli Veri Seti Oluşturma</h4>

<pre style="background:#f5f5f5; padding:15px; border-radius:5px; overflow-x:auto;">
{
  "messages": [
    {"role": "system", "content": "Sen bir Python uzmanısın"},
    {"role": "user", "content": "Liste comprehension nedir?"},
    {"role": "assistant", "content": "Liste comprehension..."}
  ]
}
</pre>

<h4>İyi Veri Seti Özellikleri</h4>
<ul>
    <li>Çeşitlilik: Farklı senaryoları kapsayın</li>
    <li>Kalite: Her örnek doğru ve tutarlı olmalı</li>
    <li>Miktar: Görev karmaşıklığına göre 100-10,000+ örnek</li>
    <li>Denge: Farklı kategoriler dengeli olmalı</li>
</ul>

<h3>Uygulama Adımları</h3>

<h4>1. Temel Model Seçimi</h4>
<p>GPT-3.5, GPT-4, Llama, Mistral gibi modellerden uygun olanı seçin.</p>

<h4>2. Veri Hazırlama</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px; overflow-x:auto;">
import pandas as pd

# Veriyi yükle ve temizle
df = pd.read_csv('training_data.csv')

# Format kontrolü
for example in df.iterrows():
    validate_format(example)

# Train/validation split
train_df = df.sample(frac=0.8)
val_df = df.drop(train_df.index)
</pre>

<h4>3. Hiperparametre Ayarı</h4>
<ul>
    <li><strong>Learning Rate:</strong> Genellikle 1e-5 ile 5e-5 arası</li>
    <li><strong>Batch Size:</strong> GPU belleğine göre 4-32 arası</li>
    <li><strong>Epochs:</strong> Overfit olmamak için 3-10 epoch</li>
    <li><strong>Warmup Steps:</strong> Toplam adımların %10'u</li>
</ul>

<h4>4. Eğitim ve İzleme</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px; overflow-x:auto;">
# Training loop monitoring
for epoch in range(num_epochs):
    train_loss = train_epoch(model, train_loader)
    val_loss = validate(model, val_loader)

    print(f"Epoch {epoch}: Train Loss={train_loss:.4f}, Val Loss={val_loss:.4f}")

    # Early stopping
    if val_loss < best_val_loss:
        save_checkpoint(model)
        best_val_loss = val_loss
</pre>

<h3>Değerlendirme Metrikleri</h3>

<h4>Otomatik Metrikler</h4>
<ul>
    <li><strong>Perplexity:</strong> Model belirsizliği</li>
    <li><strong>BLEU Score:</strong> Çeviri görevleri için</li>
    <li><strong>ROUGE Score:</strong> Özetleme için</li>
    <li><strong>F1 Score:</strong> Sınıflandırma için</li>
</ul>

<h4>Manuel Değerlendirme</h4>
<p>İnsan değerlendiriciler ile kalite kontrolü:</p>
<ul>
    <li>Doğruluk</li>
    <li>Tutarlılık</li>
    <li>Akıcılık</li>
    <li>Uygunluk</li>
</ul>

<h3>Yaygın Sorunlar ve Çözümler</h3>

<h4>Overfitting</h4>
<p><strong>Belirtiler:</strong> Eğitim loss düşüyor ama validation loss yükseliyor</p>
<p><strong>Çözümler:</strong></p>
<ul>
    <li>Daha fazla veri ekleyin</li>
    <li>Regularization uygulayın</li>
    <li>Epoch sayısını azaltın</li>
    <li>Dropout kullanın</li>
</ul>

<h4>Catastrophic Forgetting</h4>
<p><strong>Problem:</strong> Model önceki bilgilerini unutuyor</p>
<p><strong>Çözümler:</strong></p>
<ul>
    <li>Düşük learning rate kullanın</li>
    <li>Gradyan sınırlama uygulayın</li>
    <li>Genel domain veri örnekleri ekleyin</li>
</ul>

<h3>Pratik Örnekler</h3>

<h4>Müşteri Hizmetleri Botu</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
Eğitim Verisi: Şirket SSS, geçmiş konuşmalar, ürün bilgileri
Model: GPT-3.5-turbo
Metrik: Müşteri memnuniyeti skoru
Sonuç: %30 daha hızlı yanıt, %25 maliyet tasarrufu
</pre>

<h4>Kod Açıklama Asistanı</h4>
<pre style="background:#f5f5f5; padding:15px; border-radius:5px;">
Eğitim Verisi: GitHub kodları ve dokümantasyonları
Model: CodeLlama-7B
Metrik: BLEU score, insan değerlendirmesi
Sonuç: %40 daha iyi kod açıklamaları
</pre>

<h3>Sonuç</h3>
<p>Fine-tuning, dil modellerini özelleştirmenin güçlü bir yoludur. Doğru veri, dikkatli hiperparametre ayarı ve sürekli değerlendirme ile harika sonuçlar elde edebilirsiniz.</p>
''',
            'featured_image': 'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=1200',
            'tags': ['fine-tuning', 'machine learning', 'nlp', 'model training'],
            'keywords': ['fine-tuning', 'model eğitimi', 'transfer learning']
        }
    ]
}

# Her kategoriye makaleler ekle
created_count = 0
base_date = datetime.utcnow()

for category in categories:
    category_slug = category['slug']

    if category_slug not in articles_data:
        print(f"⚠️  {category['name']} kategorisi için makale verisi yok, atlanıyor...")
        continue

    articles = articles_data[category_slug]
    print(f"\n📝 {category['name']} kategorisi için {len(articles)} makale oluşturuluyor...")

    for idx, article_data in enumerate(articles):
        # Tarih hesapla (son makaleler daha yeni olsun)
        days_ago = len(articles) - idx
        published_at = base_date - timedelta(days=days_ago * 2)

        article = {
            'title': article_data['title'],
            'slug': article_data['slug'],
            'content': article_data['content'],
            'excerpt': article_data['excerpt'],
            'category': category_slug,
            'author_id': author_id,
            'featured_image': article_data['featured_image'],
            'tags': article_data['tags'],
            'keywords': article_data['keywords'],
            'status': 'published',
            'views': random.randint(100, 1000),
            'published_at': published_at,
            'created_at': published_at,
            'updated_at': published_at
        }

        # Aynı slug'a sahip makale var mı kontrol et
        existing = db.articles.find_one({'slug': article['slug']})
        if existing:
            print(f"  ⏭️  {article['title']} - Zaten var, atlanıyor")
            continue

        result = db.articles.insert_one(article)
        print(f"  ✅ {article['title']}")
        created_count += 1

print(f"\n🎉 Toplam {created_count} yeni makale oluşturuldu!")
print(f"✓ Yazar: {user['full_name']}")
