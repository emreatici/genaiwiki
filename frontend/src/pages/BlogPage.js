import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { articlesAPI } from '../services/api';
import './BlogPage.css';

const BlogPage = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    loadArticles();
  }, [page]);

  const loadArticles = async () => {
    try {
      const response = await articlesAPI.getAll({ status: 'published', page, limit: 12 });
      // Filter out main category articles - they only appear on homepage
      const filtered = response.data.articles.filter(article => article.category !== 'main');
      setArticles(filtered);
      setTotalPages(response.data.pages);
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
    <div className="blog-page">
      <div className="container">
        <div className="blog-header">
          <h1>Blog</h1>
          <p>Üretken yapay zeka teknolojileri hakkında makaleler ve rehberler</p>
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

        {totalPages > 1 && (
          <div className="pagination">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="btn btn-secondary"
            >
              Önceki
            </button>
            <span>Sayfa {page} / {totalPages}</span>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="btn btn-secondary"
            >
              Sonraki
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default BlogPage;
