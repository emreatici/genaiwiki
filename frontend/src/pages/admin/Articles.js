import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { articlesAPI } from '../../services/api';
import { useAuth } from '../../services/AuthContext';
import { toast } from 'react-toastify';
import { FiPlus, FiEdit2, FiTrash2, FiCheckCircle } from 'react-icons/fi';
import './AdminStyles.css';

const Articles = () => {
  const { user } = useAuth();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticles();
  }, []);

  const loadArticles = async () => {
    try {
      const response = await articlesAPI.getAll({ limit: 100 });
      setArticles(response.data.articles);
    } catch (error) {
      toast.error('Makaleler yüklenemedi');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Bu makaleyi silmek istediğinizden emin misiniz?')) return;

    try {
      await articlesAPI.delete(id);
      toast.success('Makale silindi');
      loadArticles();
    } catch (error) {
      toast.error('Silme işlemi başarısız');
    }
  };

  const handleStatusToggle = async (article) => {
    const newStatus = article.status === 'published' ? 'draft' : 'published';
    try {
      await articlesAPI.update(article._id, { status: newStatus });
      toast.success(`Makale ${newStatus === 'published' ? 'yayınlandı' : 'taslağa alındı'}`);
      loadArticles();
    } catch (error) {
      toast.error('Durum değiştirilemedi');
    }
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  return (
    <div className="admin-page">
      <div className="container">
        <div className="admin-toolbar">
          <h2>Makaleler</h2>
          <Link to="/admin/articles/new" className="btn btn-primary">
            <FiPlus /> Yeni Makale
          </Link>
        </div>

        <div className="admin-table">
          <table>
            <thead>
              <tr>
                <th>Başlık</th>
                <th>Kategori</th>
                <th>Yazar</th>
                <th>Durum</th>
                <th>Tarih</th>
                <th>İşlemler</th>
              </tr>
            </thead>
            <tbody>
              {articles.map((article) => (
                <tr key={article._id}>
                  <td>{article.title}</td>
                  <td>{article.category}</td>
                  <td>{article.author_name}</td>
                  <td>
                    <span className={`status-badge status-${article.status}`}>
                      {article.status === 'published' ? 'Yayında' : 'Taslak'}
                    </span>
                  </td>
                  <td>{new Date(article.created_at).toLocaleDateString('tr-TR')}</td>
                  <td>
                    <div className="table-actions">
                      {user?.role === 'admin' && (
                        <button
                          onClick={() => handleStatusToggle(article)}
                          title={article.status === 'published' ? 'Taslağa Al' : 'Yayınla'}
                          style={{ color: article.status === 'published' ? '#10b981' : '#6b7280' }}
                        >
                          <FiCheckCircle />
                        </button>
                      )}
                      <Link to={`/admin/articles/edit/${article._id}`}>
                        <button title="Düzenle">
                          <FiEdit2 />
                        </button>
                      </Link>
                      <button onClick={() => handleDelete(article._id)} title="Sil">
                        <FiTrash2 />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Articles;
