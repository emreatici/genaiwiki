#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create main category and articles
"""

from pymongo import MongoClient
from datetime import datetime
import sys

# MongoDB connection
MONGODB_URI = 'mongodb://admin:admin123@localhost:27017/genaiwiki?authSource=admin'
client = MongoClient(MONGODB_URI)
db = client['genaiwiki']

def create_main_category():
    """Create main category"""
    category = {
        'name': 'Ana Sayfa',
        'slug': 'main',
        'description': 'Ana sayfa özel içerikleri',
        'is_main_menu': False,
        'order': 0,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }

    # Check if exists
    existing = db.categories.find_one({'slug': 'main'})
    if existing:
        print('Main category already exists')
        return existing['_id']

    result = db.categories.insert_one(category)
    print(f'Created main category with ID: {result.inserted_id}')
    return result.inserted_id

def create_articles():
    """Create 8 main articles"""
    articles_data = [
        {
            'title': 'Üretken Yapay Zeka Nedir?',
            'slug': 'uretken-yapay-zeka-nedir',
            'content': '''<h2>Üretken Yapay Zeka Nedir?</h2>
<p>Üretken yapay zeka (Generative AI), metin, görüntü, ses, video ve diğer medya türlerini oluşturabilen yapay zeka sistemleridir. Bu sistemler, büyük veri setleri üzerinde eğitilerek, orijinal ve yaratıcı içerikler üretebilir.</p>
<h3>Temel Özellikler</h3>
<ul>
<li><strong>İçerik Üretimi:</strong> Sıfırdan yeni içerik oluşturabilir</li>
<li><strong>Öğrenme Yeteneği:</strong> Büyük veri setlerinden öğrenir</li>
<li><strong>Çok Yönlülük:</strong> Farklı medya türlerinde çalışabilir</li>
<li><strong>Yaratıcılık:</strong> İnsan benzeri yaratıcı çıktılar üretir</li>
</ul>
<h3>Popüler Modeller</h3>
<p>ChatGPT, DALL-E, Midjourney, Stable Diffusion gibi modeller üretken yapay zekanın örnekleridir.</p>''',
            'excerpt': 'Üretken yapay zeka, metin, görüntü, ses ve video gibi içerikleri oluşturabilen yapay zeka sistemleridir.',
            'featured_image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
        },
        {
            'title': 'Metin Üretme',
            'slug': 'metin-uretme',
            'content': '''<h2>Metin Üretme ile Yapay Zeka</h2>
<p>Metin üretme teknolojileri, yapay zekanın en popüler uygulamalarından biridir. ChatGPT, GPT-4, Claude gibi modeller, insan benzeri metinler oluşturabilir.</p>
<h3>Kullanım Alanları</h3>
<ul>
<li><strong>İçerik Yazarlığı:</strong> Blog yazıları, makaleler, sosyal medya içerikleri</li>
<li><strong>Kod Yazımı:</strong> Programlama dilleri için kod üretimi</li>
<li><strong>Çeviri:</strong> Diller arası çeviri işlemleri</li>
<li><strong>Özet Çıkarma:</strong> Uzun metinlerin özetlenmesi</li>
<li><strong>Soru-Cevap:</strong> Doğal dil ile soru cevaplama</li>
</ul>
<h3>Popüler Araçlar</h3>
<p>ChatGPT, GPT-4, Claude, Gemini, LLaMA gibi büyük dil modelleri metin üretiminde kullanılır.</p>''',
            'excerpt': 'Metin üretme teknolojileri ile blog yazıları, kod, çeviri ve daha fazlasını otomatik olarak oluşturabilirsiniz.',
            'featured_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800',
        },
        {
            'title': 'Görüntü Üretme',
            'slug': 'goruntu-uretme',
            'content': '''<h2>Görüntü Üretme Teknolojileri</h2>
<p>Görüntü üretme, yapay zekanın en etkileyici uygulamalarından biridir. Sadece metin açıklamasıyla gerçekçi ve sanatsal görüntüler oluşturabilirsiniz.</p>
<h3>Temel Teknolojiler</h3>
<ul>
<li><strong>Diffusion Models:</strong> Stable Diffusion, DALL-E 3</li>
<li><strong>GAN (Generative Adversarial Networks):</strong> StyleGAN</li>
<li><strong>Transformer-Based:</strong> DALL-E 2, Imagen</li>
</ul>
<h3>Kullanım Alanları</h3>
<ul>
<li>Dijital sanat ve illüstrasyon</li>
<li>Ürün tasarımı ve prototipleme</li>
<li>Reklam ve pazarlama görselleri</li>
<li>Mimari görselleştirme</li>
<li>Oyun ve film endüstrisi</li>
</ul>
<h3>Popüler Platformlar</h3>
<p>Midjourney, DALL-E 3, Stable Diffusion, Leonardo.ai, Firefly</p>''',
            'excerpt': 'Metin açıklamalarından gerçekçi ve sanatsal görüntüler oluşturmak için yapay zeka araçlarını keşfedin.',
            'featured_image': 'https://images.unsplash.com/photo-1686191128892-c842fff96f9a?w=800',
        },
        {
            'title': 'Ses Üretme',
            'slug': 'ses-uretme',
            'content': '''<h2>Ses Üretme ve Yapay Zeka</h2>
<p>Ses üretme teknolojileri, konuşma sentezinden müzik üretimine kadar geniş bir yelpazede kullanılır. Yapay zeka, gerçekçi insan sesleri ve ses efektleri oluşturabilir.</p>
<h3>Teknolojiler</h3>
<ul>
<li><strong>Text-to-Speech (TTS):</strong> Metinden konuşma sentezi</li>
<li><strong>Voice Cloning:</strong> Ses klonlama</li>
<li><strong>Audio Generation:</strong> Ses efektleri üretimi</li>
<li><strong>Speech Enhancement:</strong> Ses iyileştirme</li>
</ul>
<h3>Kullanım Alanları</h3>
<ul>
<li>Sesli kitaplar ve podcast'ler</li>
<li>Video seslendirme ve dublaj</li>
<li>Asistan uygulamaları</li>
<li>Erişilebilirlik araçları</li>
<li>Oyun karakterleri</li>
</ul>
<h3>Popüler Araçlar</h3>
<p>ElevenLabs, Play.ht, Murf.ai, Resemble.ai, Azure Speech</p>''',
            'excerpt': 'Yapay zeka ile gerçekçi insan sesleri, ses efektleri ve seslendirmeler oluşturun.',
            'featured_image': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800',
        },
        {
            'title': 'Video Üretme',
            'slug': 'video-uretme',
            'content': '''<h2>Video Üretme Teknolojileri</h2>
<p>Video üretme, yapay zekanın en yeni ve hızla gelişen alanlarından biridir. Metinden veya görüntülerden video oluşturma imkanı sunar.</p>
<h3>Video Üretim Türleri</h3>
<ul>
<li><strong>Text-to-Video:</strong> Metinden video oluşturma</li>
<li><strong>Image-to-Video:</strong> Görüntüden video animasyonu</li>
<li><strong>Video Düzenleme:</strong> Otomatik kurgu ve düzenleme</li>
<li><strong>Deepfake:</strong> Yüz değiştirme teknolojisi</li>
</ul>
<h3>Kullanım Alanları</h3>
<ul>
<li>İçerik üretimi ve sosyal medya</li>
<li>Eğitim videoları</li>
<li>Reklam ve tanıtım filmleri</li>
<li>Animasyon ve görsel efektler</li>
<li>Sanal karakterler</li>
</ul>
<h3>Popüler Platformlar</h3>
<p>Runway ML, Pika Labs, Synthesia, D-ID, HeyGen</p>''',
            'excerpt': 'Yapay zeka ile metinden video oluşturun, görüntüleri canlandırın ve profesyonel videolar üretin.',
            'featured_image': 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800',
        },
        {
            'title': 'Müzik Üretme',
            'slug': 'muzik-uretme',
            'content': '''<h2>Müzik Üretme ve Yapay Zeka</h2>
<p>Yapay zeka müzik üretimi, bestelerden ritim bölümlerine kadar her türlü müzik elementini oluşturabilir. Artık müzisyen olmadan orijinal müzik üretmek mümkün.</p>
<h3>Müzik Üretim Teknolojileri</h3>
<ul>
<li><strong>Melodi Üretimi:</strong> Özgün melodiler oluşturma</li>
<li><strong>Ritim ve Beat:</strong> Davul ve ritim desenleri</li>
<li><strong>Armoni:</strong> Akor ve armoni yapıları</li>
<li><strong>Ses Sentezi:</strong> Enstrüman sesleri</li>
</ul>
<h3>Kullanım Alanları</h3>
<ul>
<li>Film ve oyun müzikleri</li>
<li>Podcast ve video arkaplan müzikleri</li>
<li>Reklam jingleları</li>
<li>Müzik prodüksiyonu</li>
<li>Meditasyon ve ambient müzik</li>
</ul>
<h3>Popüler Araçlar</h3>
<p>Suno AI, Udio, AIVA, Soundraw, Mubert</p>''',
            'excerpt': 'Yapay zeka ile özgün müzikler, melodiler ve soundtrackler oluşturun.',
            'featured_image': 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800',
        },
        {
            'title': 'Bankamızdan Örnekler',
            'slug': 'bankamizdan-ornekler',
            'content': '''<h2>Bankamızdan Örnek Uygulamalar</h2>
<p>Üretken yapay zeka teknolojilerinin gerçek dünya uygulamalarından örnekler ve örnek çalışmalar.</p>
<h3>İçerik Üretimi</h3>
<ul>
<li>Blog yazıları ve makaleler</li>
<li>Sosyal medya içerikleri</li>
<li>Ürün açıklamaları</li>
<li>E-posta kampanyaları</li>
</ul>
<h3>Görsel Üretim</h3>
<ul>
<li>Ürün görselleri ve mockup'lar</li>
<li>Logo ve branding çalışmaları</li>
<li>İllüstrasyonlar ve grafikler</li>
<li>Sosyal medya görselleri</li>
</ul>
<h3>Multimedya</h3>
<ul>
<li>Tanıtım videoları</li>
<li>Podcast ve sesli içerikler</li>
<li>Arkaplan müzikleri</li>
<li>Animasyonlar</li>
</ul>
<h3>Daha Fazlası İçin</h3>
<p>Örnek çalışmalarımızı incelemek ve kendi projeleriniz için ilham almak için blog bölümümüzü ziyaret edin.</p>''',
            'excerpt': 'Üretken yapay zeka ile oluşturulmuş gerçek dünya örneklerini ve başarı hikayelerini keşfedin.',
            'featured_image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
        },
        {
            'title': 'Üretken Yapay Zeka Sözlüğü',
            'slug': 'uretken-yapay-zeka-sozlugu',
            'content': '''<h2>Üretken Yapay Zeka Sözlüğü</h2>
<p>Üretken yapay zeka dünyasında kullanılan temel terimler ve kavramlar.</p>
<h3>Temel Terimler</h3>
<p><strong>LLM (Large Language Model):</strong> Büyük dil modeli, milyarlarca parametreyle eğitilmiş metin üretim modeli.</p>
<p><strong>Prompt:</strong> Yapay zekaya verilen talimat veya giriş metni.</p>
<p><strong>Token:</strong> Modelin işlediği temel metin birimi.</p>
<p><strong>Fine-tuning:</strong> Var olan bir modeli belirli bir görev için özelleştirme.</p>
<p><strong>Diffusion Model:</strong> Görüntü üretiminde kullanılan, gürültüden temiz görüntü elde eden model türü.</p>
<h3>Teknik Terimler</h3>
<p><strong>Transformer:</strong> Modern yapay zeka modellerinin temelini oluşturan mimari.</p>
<p><strong>Attention Mechanism:</strong> Modelin önemli bilgilere odaklanmasını sağlayan mekanizma.</p>
<p><strong>Zero-shot Learning:</strong> Örnekler görmeden yeni görevleri öğrenme.</p>
<p><strong>Few-shot Learning:</strong> Az sayıda örnekle öğrenme.</p>
<p><strong>Hallucination:</strong> Modelin gerçek olmayan bilgiler üretmesi.</p>
<h3>Model İsimleri</h3>
<p><strong>GPT:</strong> Generative Pre-trained Transformer</p>
<p><strong>BERT:</strong> Bidirectional Encoder Representations from Transformers</p>
<p><strong>GAN:</strong> Generative Adversarial Network</p>
<p><strong>VAE:</strong> Variational Autoencoder</p>''',
            'excerpt': 'Üretken yapay zeka alanında kullanılan temel terimleri ve kavramları öğrenin.',
            'featured_image': 'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800',
        }
    ]

    created_count = 0
    for article_data in articles_data:
        # Check if exists
        existing = db.articles.find_one({'slug': article_data['slug']})
        if existing:
            print(f'Article "{article_data["title"]}" already exists')
            continue

        article = {
            **article_data,
            'category': 'main',
            'tags': ['yapay zeka', 'üretken ai', 'teknoloji'],
            'keywords': ['yapay zeka', 'ai', 'generative ai'],
            'status': 'published',
            'author_name': 'Admin',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = db.articles.insert_one(article)
        print(f'Created article: {article_data["title"]} (ID: {result.inserted_id})')
        created_count += 1

    return created_count

if __name__ == '__main__':
    try:
        print('Creating main category...')
        create_main_category()

        print('\nCreating articles...')
        count = create_articles()

        print(f'\n✓ Successfully created {count} articles')
        print('✓ All done!')

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
