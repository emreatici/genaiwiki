import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { articlesAPI } from '../services/api';
import './ArticlePage.css';

const ArticlePage = () => {
  const { slug } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticle();
  }, [slug]);

  const loadArticle = async () => {
    try {
      const response = await articlesAPI.getById(slug);
      setArticle(response.data);
    } catch (error) {
      console.error('Makale yüklenemedi:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  if (!article) {
    return <div className="container"><h2>Makale bulunamadı</h2></div>;
  }

  return (
    <div className="article-page">
      <div className="container">
        <article className="article">
          <header className="article-header">
            <span className="article-category">{article.category}</span>
            <h1>{article.title}</h1>
            <div className="article-meta">
              <span>{article.author_name}</span>
              <span>•</span>
              <span>{new Date(article.created_at).toLocaleDateString('tr-TR')}</span>
              <span>•</span>
              <span>{article.views} görüntülenme</span>
            </div>
          </header>

          {article.featured_image && (
            <div className="article-featured-image">
              <img src={article.featured_image} alt={article.title} />
            </div>
          )}

          <div className="article-body" dangerouslySetInnerHTML={{ __html: article.content }} />

          {article.tags && article.tags.length > 0 && (
            <div className="article-tags">
              <h4>Etiketler:</h4>
              <div className="tags">
                {article.tags.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
            </div>
          )}
        </article>
      </div>
    </div>
  );
};

export default ArticlePage;
