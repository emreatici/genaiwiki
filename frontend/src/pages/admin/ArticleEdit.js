import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { articlesAPI, categoriesAPI, mediaAPI, usersAPI } from '../../services/api';
import { useAuth } from '../../services/AuthContext';
import { toast } from 'react-toastify';
import ReactQuill, { Quill } from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import ImageResize from 'quill-image-resize-module-react';
import slugify from 'slugify';
import { FiSave, FiX, FiUpload, FiTrash2 } from 'react-icons/fi';
import './AdminStyles.css';

// Register image resize module
Quill.register('modules/imageResize', ImageResize);

const ArticleEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const quillRef = useRef(null);
  const { user } = useAuth();
  const [categories, setCategories] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [editorReady, setEditorReady] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    content: '',
    excerpt: '',
    category: '',
    tags: [],
    keywords: [],
    featured_image: '',
    status: 'published',
    author_id: '',
    published_at: ''
  });

  useEffect(() => {
    const initEditor = async () => {
      await loadCategories();
      if (user?.role === 'admin') {
        await loadUsers();
      }
      if (id) {
        await loadArticle();
      }
      // Editörü biraz gecikmeli başlat
      setTimeout(() => setEditorReady(true), 100);
    };
    initEditor();
  }, [id, user]);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data);
    } catch (error) {
      toast.error('Kategoriler yüklenemedi');
    }
  };

  const loadUsers = async () => {
    try {
      const response = await usersAPI.getAll();
      setUsers(response.data);
    } catch (error) {
      console.error('Kullanıcılar yüklenemedi:', error);
    }
  };

  const loadArticle = async () => {
    try {
      const response = await articlesAPI.getById(id);
      const article = response.data;

      // published_at'i datetime-local input için formatla
      let publishedAt = '';
      if (article.published_at) {
        const date = new Date(article.published_at);
        publishedAt = date.toISOString().slice(0, 16); // YYYY-MM-DDTHH:mm format
      }

      setFormData({
        title: article.title,
        slug: article.slug,
        content: article.content,
        excerpt: article.excerpt,
        category: article.category,
        tags: article.tags || [],
        keywords: article.keywords || [],
        featured_image: article.featured_image || '',
        status: article.status,
        author_id: article.author_id || '',
        published_at: publishedAt
      });
    } catch (error) {
      toast.error('Makale yüklenemedi');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Title değiştiğinde slug'ı otomatik oluştur
    if (name === 'title' && !id) {
      setFormData(prev => ({
        ...prev,
        title: value,
        slug: slugify(value, { lower: true, strict: true })
      }));
    }
  };

  const handleTagsChange = (e) => {
    const tags = e.target.value.split(',').map(tag => tag.trim()).filter(Boolean);
    setFormData({ ...formData, tags });
  };

  const handleKeywordsChange = (e) => {
    const keywords = e.target.value.split(',').map(kw => kw.trim()).filter(Boolean);
    setFormData({ ...formData, keywords });
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Dosya tipini kontrol et
    if (!file.type.startsWith('image/')) {
      toast.error('Lütfen sadece resim dosyası yükleyin');
      return;
    }

    // Dosya boyutunu kontrol et (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('Dosya boyutu en fazla 5MB olabilir');
      return;
    }

    setUploading(true);

    try {
      const formDataUpload = new FormData();
      formDataUpload.append('file', file);

      const response = await mediaAPI.upload(formDataUpload);
      const imageUrl = response.data.url;

      setFormData({ ...formData, featured_image: imageUrl });
      toast.success('Resim yüklendi');
    } catch (error) {
      toast.error('Resim yüklenemedi: ' + (error.response?.data?.error || error.message));
    } finally {
      setUploading(false);
    }
  };

  const handleRemoveFeaturedImage = () => {
    setFormData({ ...formData, featured_image: '' });
  };

  // Custom image handler for Quill editor
  const imageHandler = useCallback(() => {
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.click();

    input.onchange = async () => {
      const file = input.files[0];
      if (!file) return;

      // Validate file type
      if (!file.type.startsWith('image/')) {
        toast.error('Lütfen sadece resim dosyası yükleyin');
        return;
      }

      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        toast.error('Dosya boyutu en fazla 5MB olabilir');
        return;
      }

      try {
        const formDataUpload = new FormData();
        formDataUpload.append('file', file);

        const response = await mediaAPI.upload(formDataUpload);
        const imageUrl = response.data.url;

        // Insert image into editor
        if (quillRef.current) {
          const quill = quillRef.current.getEditor();
          const range = quill.getSelection() || { index: 0 };
          quill.insertEmbed(range.index, 'image', imageUrl);
          quill.setSelection(range.index + 1);
        }

        toast.success('Resim yüklendi');
      } catch (error) {
        toast.error('Resim yüklenemedi: ' + (error.response?.data?.error || error.message));
      }
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // FormData'yı hazırla
      const submitData = { ...formData };

      // Eğer published_at varsa, ISO formatına çevir
      if (submitData.published_at) {
        submitData.published_at = new Date(submitData.published_at).toISOString();
      } else {
        // Boş string ise alanı kaldır
        delete submitData.published_at;
      }

      // author_id boş ise kaldır
      if (!submitData.author_id) {
        delete submitData.author_id;
      }

      if (id) {
        await articlesAPI.update(id, submitData);
        toast.success('Makale güncellendi');
      } else {
        await articlesAPI.create(submitData);
        toast.success('Makale oluşturuldu');
      }
      navigate('/admin/articles');
    } catch (error) {
      toast.error('Kayıt başarısız: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const quillModules = useMemo(() => ({
    toolbar: {
      container: [
        [{ 'header': [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'align': [] }],
        [{ 'color': [] }, { 'background': [] }],
        ['link', 'image', 'video'],
        ['clean']
      ],
      handlers: {
        image: imageHandler
      }
    },
    imageResize: {
      parchment: Quill.import('parchment'),
      modules: ['Resize', 'DisplaySize']
    }
  }), [imageHandler]);

  const quillFormats = useMemo(() => [
    'header',
    'bold', 'italic', 'underline', 'strike',
    'list', 'bullet',
    'align',
    'color', 'background',
    'link', 'image', 'video',
    'width', 'height', 'style'
  ], []);

  return (
    <div className="admin-page">
      <div className="container">
        <h2>{id ? 'Makale Düzenle' : 'Yeni Makale'}</h2>

        <form onSubmit={handleSubmit} className="admin-form">
          <div className="form-row">
            <div className="form-group">
              <label>Başlık *</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Slug *</label>
              <input
                type="text"
                name="slug"
                value={formData.slug}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Kategori *</label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                required
              >
                <option value="">Seçiniz</option>
                {categories.map((cat) => (
                  <option key={cat._id} value={cat.slug}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Durum *</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
              >
                <option value="draft">Taslak</option>
                <option value="published">Yayınla</option>
              </select>
            </div>
          </div>

          {/* Admin için yazar ve tarih seçimi */}
          {user?.role === 'admin' && (
            <div className="form-row">
              <div className="form-group">
                <label>Yazar</label>
                <select
                  name="author_id"
                  value={formData.author_id}
                  onChange={handleChange}
                >
                  <option value="">Yazar Yok (Admin)</option>
                  {users.map((u) => (
                    <option key={u._id} value={u._id}>
                      {u.full_name || u.username} ({u.role})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Yayın Tarihi</label>
                <input
                  type="datetime-local"
                  name="published_at"
                  value={formData.published_at}
                  onChange={handleChange}
                />
                <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                  Sıralama için kullanılır. Boş bırakılırsa otomatik ayarlanır.
                </p>
              </div>
            </div>
          )}

          <div className="form-group">
            <label>Özet</label>
            <textarea
              name="excerpt"
              value={formData.excerpt}
              onChange={handleChange}
              rows="5"
              placeholder="Makalenin kısa bir özetini yazın..."
            />
          </div>

          <div className="form-group">
            <label>İçerik *</label>
            <div className="quill-container">
              {editorReady ? (
                <ReactQuill
                  ref={quillRef}
                  theme="snow"
                  value={formData.content}
                  onChange={(value) => setFormData({ ...formData, content: value })}
                  modules={quillModules}
                  formats={quillFormats}
                  placeholder="Makale içeriğinizi buraya yazın..."
                />
              ) : (
                <div style={{
                  height: '400px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: '#f8f9fa',
                  border: '1px solid #ddd',
                  borderRadius: '8px'
                }}>
                  <p>Editör yükleniyor...</p>
                </div>
              )}
            </div>
          </div>

          <div className="form-group">
            <label>Öne Çıkan Görsel</label>
            {formData.featured_image ? (
              <div className="featured-image-preview">
                <img src={formData.featured_image} alt="Featured" style={{ maxWidth: '300px', maxHeight: '200px', objectFit: 'cover', borderRadius: '8px' }} />
                <button
                  type="button"
                  onClick={handleRemoveFeaturedImage}
                  className="btn btn-danger btn-sm"
                  style={{ marginTop: '10px' }}
                >
                  <FiTrash2 /> Görseli Kaldır
                </button>
              </div>
            ) : (
              <div>
                <input
                  type="file"
                  id="featured-image-upload"
                  accept="image/*"
                  onChange={handleImageUpload}
                  style={{ display: 'none' }}
                />
                <label htmlFor="featured-image-upload" className="btn btn-secondary" style={{ cursor: 'pointer' }}>
                  <FiUpload /> {uploading ? 'Yükleniyor...' : 'Görsel Yükle'}
                </label>
                <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                  Maksimum 5MB, JPG, PNG veya GIF formatında
                </p>
              </div>
            )}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Etiketler (virgülle ayırın)</label>
              <input
                type="text"
                value={formData.tags.join(', ')}
                onChange={handleTagsChange}
                placeholder="AI, GPT, Makine Öğrenimi"
              />
            </div>

            <div className="form-group">
              <label>Anahtar Kelimeler (virgülle ayırın)</label>
              <input
                type="text"
                value={formData.keywords.join(', ')}
                onChange={handleKeywordsChange}
                placeholder="yapay zeka, chatgpt"
              />
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/admin/articles')}
              className="btn btn-secondary"
            >
              <FiX /> İptal
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              <FiSave /> {loading ? 'Kaydediliyor...' : 'Kaydet'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ArticleEdit;
