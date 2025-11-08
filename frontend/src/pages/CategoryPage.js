import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { categoriesAPI, articlesAPI } from '../services/api';

const CategoryPage = () => {
  const { slug } = useParams();
  const [category, setCategory] = useState(null);
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [slug]);

  const loadData = async () => {
    try {
      const [categoryRes, articlesRes] = await Promise.all([
        categoriesAPI.getById(slug),
        articlesAPI.getAll({ status: 'published', category: slug })
      ]);
      setCategory(categoryRes.data);
      setArticles(articlesRes.data.articles);
    } catch (error) {
      console.error('Veri yükleme hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  if (!category) {
    return <div className="container"><h2>Kategori bulunamadı</h2></div>;
  }

  return (
    <div className="category-page" style={{padding: '3rem 0'}}>
      <div className="container">
        <div className="blog-header">
          <h1>{category.name}</h1>
          <p>{category.description}</p>
        </div>

        <div className="articles-grid">
          {articles.map((article) => (
            <Link key={article._id} to={`/article/${article.slug}`} className="article-card">
              {article.featured_image && (
                <div className="article-image">
                  <img src={article.featured_image} alt={article.title} />
                </div>
              )}
              <div className="article-content">
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

        {articles.length === 0 && (
          <div style={{textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)'}}>
            Bu kategoride henüz makale bulunmuyor.
          </div>
        )}
      </div>
    </div>
  );
};

export default CategoryPage;
