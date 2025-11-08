import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { articlesAPI } from '../services/api';

const TagPage = () => {
  const { tag } = useParams();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticles();
  }, [tag]);

  const loadArticles = async () => {
    try {
      const response = await articlesAPI.getAll({
        status: 'published',
        tag: decodeURIComponent(tag)
      });
      setArticles(response.data.articles);
    } catch (error) {
      console.error('Makaleler yüklenemedi:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  return (
    <div className="tag-page" style={{padding: '3rem 0'}}>
      <div className="container">
        <div className="blog-header">
          <h1>#{decodeURIComponent(tag)}</h1>
          <p>Bu etikete sahip makaleler</p>
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
            Bu etiketle ilgili henüz makale bulunmuyor.
          </div>
        )}
      </div>
    </div>
  );
};

export default TagPage;
