import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { categoriesAPI, articlesAPI, settingsAPI } from '../services/api';
import { FiArrowRight, FiCpu, FiImage, FiMic, FiVideo, FiCode, FiZap } from 'react-icons/fi';
import './HomePage.css';

const HomePage = () => {
  const [categories, setCategories] = useState([]);
  const [mainArticles, setMainArticles] = useState([]);
  const [featuredArticles, setFeaturedArticles] = useState([]);
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (settings) {
      document.title = settings.site_title || 'GenAI Wiki';
    }
  }, [settings]);

  const loadData = async () => {
    try {
      // Önce settings'i yükle
      const settingsRes = await settingsAPI.get();
      const loadedSettings = settingsRes.data;
      setSettings(loadedSettings);

      // Settings'ten makale sayısını al (varsayılan: 20)
      const articlesCount = loadedSettings.homepage_articles_count || 20;

      // Diğer verileri yükle
      const [categoriesRes, mainRes, articlesRes] = await Promise.all([
        categoriesAPI.getAll(),
        articlesAPI.getAll({ status: 'published', category: 'main' }),
        articlesAPI.getAll({ status: 'published', limit: articlesCount })
      ]);

      // Filter out 'main' category from categories list
      const filteredCategories = categoriesRes.data.filter(cat => cat.slug !== 'main');
      setCategories(filteredCategories);
      setMainArticles(mainRes.data.articles);
      // Filter out main category articles from featured articles
      const filtered = articlesRes.data.articles.filter(article => article.category !== 'main');
      setFeaturedArticles(filtered);
    } catch (error) {
      console.error('Veri yükleme hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const categoryIcons = {
    metin: <FiCode size={40} />,
    gorsel: <FiImage size={40} />,
    ses: <FiMic size={40} />,
    video: <FiVideo size={40} />,
    kod: <FiCpu size={40} />,
    diger: <FiZap size={40} />
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  const bannerEnabled = settings?.banner?.enabled !== false;
  const bannerStyle = settings?.banner?.background_image ? {
    backgroundImage: `linear-gradient(rgba(0, 0, 0, ${settings.banner.overlay_opacity || 0.5}), rgba(0, 0, 0, ${settings.banner.overlay_opacity || 0.5})), url(${settings.banner.background_image})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    color: settings.banner.text_color || '#ffffff'
  } : {};

  return (
    <div className="home-page">
      {/* Hero Section - Only show if enabled in settings */}
      {bannerEnabled && (
        <section className="hero" style={bannerStyle}>
          <div className="container">
            <div className="hero-content">
              <h1 className="hero-title">
                {settings?.banner?.title || 'Üretken Yapay Zeka Dünyasına Hoş Geldiniz'}
              </h1>
              <p className="hero-subtitle">
                {settings?.banner?.subtitle || 'Metin, görsel, ses ve video üretimi için en güncel AI teknolojileri hakkında kapsamlı bilgi ve rehberler'}
              </p>
            </div>
          </div>
        </section>
      )}

      {/* Main Topics Section */}
      {mainArticles.length > 0 && (
        <section className="main-topics-section">
          <div className="container">
            {settings?.show_section_titles !== false && settings?.show_main_section_title !== false && (
              <h2 className="section-title">Konular</h2>
            )}
            <div className="main-topics-grid">
              {mainArticles.map((article) => (
                <Link
                  key={article._id}
                  to={`/article/${article.slug}`}
                  className="main-topic-card"
                >
                  {article.featured_image && (
                    <div className="main-topic-image">
                      <img src={article.featured_image} alt={article.title} />
                    </div>
                  )}
                  <h3 className="main-topic-title">{article.title}</h3>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Middle Banner Section */}
      {settings?.middle_banner?.enabled && settings?.middle_banner?.image && (
        <section className="middle-banner">
          <div className="container">
            {settings.middle_banner.link ? (
              settings.middle_banner.external ? (
                <a
                  href={settings.middle_banner.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="middle-banner-link"
                >
                  <div className="middle-banner-content">
                    <img
                      src={settings.middle_banner.image}
                      alt={settings.middle_banner.alt_text || 'Banner'}
                    />
                  </div>
                </a>
              ) : (
                <Link to={settings.middle_banner.link} className="middle-banner-link">
                  <div className="middle-banner-content">
                    <img
                      src={settings.middle_banner.image}
                      alt={settings.middle_banner.alt_text || 'Banner'}
                    />
                  </div>
                </Link>
              )
            ) : (
              <div className="middle-banner-content">
                <img
                  src={settings.middle_banner.image}
                  alt={settings.middle_banner.alt_text || 'Banner'}
                />
              </div>
            )}
          </div>
        </section>
      )}

      {/* Categories Section */}
      <section className="categories-section">
        <div className="container">
          {settings?.show_section_titles !== false && (
            <h2 className="section-title">Kategoriler</h2>
          )}
          <div className="categories-grid">
            {categories.map((category) => (
              <Link
                key={category._id}
                to={`/category/${category.slug}`}
                className="category-card"
              >
                {category.featured_image ? (
                  <div className="category-image">
                    <img src={category.featured_image} alt={category.name} />
                  </div>
                ) : (
                  <div className="category-icon">
                    {categoryIcons[category.slug] || <FiCpu size={40} />}
                  </div>
                )}
                <h3>{category.name}</h3>
                <p>{category.description}</p>
                <span className="category-link">
                  Keşfet <FiArrowRight />
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Articles Section */}
      {featuredArticles.length > 0 && (
        <section className="featured-section">
          <div className="container">
            {settings?.show_section_titles !== false && (
              <h2 className="section-title">Son Makaleler</h2>
            )}
            <div className="articles-grid">
              {featuredArticles.map((article) => (
                <Link
                  key={article._id}
                  to={`/article/${article.slug}`}
                  className="article-card"
                >
                  {article.featured_image && (
                    <div className="article-image">
                      <img src={article.featured_image} alt={article.title} />
                    </div>
                  )}
                  <div className="article-content">
                    <span className="article-category">{article.category}</span>
                    <h3>{article.title}</h3>
                    <p>{article.excerpt}</p>
                    <div className="article-meta">
                      <span>{article.author_name}</span>
                      <span>•</span>
                      <span>{new Date(article.created_at).toLocaleDateString('tr-TR')}</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            {settings?.show_section_titles !== false && (
              <h2>Daha Fazlasını Öğrenin</h2>
            )}
            <p>Blog bölümünde daha fazla makale ve rehber keşfedin</p>
            <Link to="/blog" className="btn btn-primary">
              Blog'a Git <FiArrowRight />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
