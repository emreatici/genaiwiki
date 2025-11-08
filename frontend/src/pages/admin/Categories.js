import React, { useState, useEffect } from 'react';
import { categoriesAPI, mediaAPI } from '../../services/api';
import { toast } from 'react-toastify';
import slugify from 'slugify';
import { FiPlus, FiEdit2, FiTrash2, FiUpload } from 'react-icons/fi';
import './AdminStyles.css';

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [editing, setEditing] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    description: '',
    featured_image: '',
    is_main_menu: false,
    order: 0
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data);
    } catch (error) {
      toast.error('Kategoriler yüklenemedi');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    setFormData({ ...formData, [name]: newValue });

    if (name === 'name') {
      setFormData(prev => ({
        ...prev,
        name: value,
        slug: slugify(value, { lower: true, strict: true })
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editing) {
        await categoriesAPI.update(editing, formData);
        toast.success('Kategori güncellendi');
      } else {
        await categoriesAPI.create(formData);
        toast.success('Kategori oluşturuldu');
      }
      resetForm();
      loadCategories();
    } catch (error) {
      toast.error('Kayıt başarısız');
    }
  };

  const handleEdit = (category) => {
    setEditing(category._id);
    setFormData({
      name: category.name,
      slug: category.slug,
      description: category.description || '',
      featured_image: category.featured_image || '',
      is_main_menu: category.is_main_menu || false,
      order: category.order || 0
    });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Bu kategoriyi silmek istediğinizden emin misiniz?')) return;

    try {
      await categoriesAPI.delete(id);
      toast.success('Kategori silindi');
      loadCategories();
    } catch (error) {
      toast.error('Silme işlemi başarısız');
    }
  };

  const resetForm = () => {
    setEditing(null);
    setFormData({ name: '', slug: '', description: '', featured_image: '', is_main_menu: false, order: 0 });
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Lütfen sadece resim dosyası yükleyin');
      return;
    }

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

  return (
    <div className="admin-page">
      <div className="container">
        <h2>Kategoriler</h2>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
          <div className="admin-form">
            <h3>{editing ? 'Kategori Düzenle' : 'Yeni Kategori'}</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Kategori Adı *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
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

              <div className="form-group">
                <label>Açıklama</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label>Kategori Görseli</label>
                {formData.featured_image ? (
                  <div className="image-preview">
                    <img src={formData.featured_image} alt="Kategori" style={{ maxWidth: '200px', maxHeight: '150px', objectFit: 'cover', borderRadius: '8px' }} />
                    <button
                      type="button"
                      onClick={() => setFormData({ ...formData, featured_image: '' })}
                      className="btn btn-danger btn-sm"
                      style={{ marginTop: '10px' }}
                    >
                      Görseli Kaldır
                    </button>
                  </div>
                ) : (
                  <div>
                    <input
                      type="file"
                      id="category-image-upload"
                      accept="image/*"
                      onChange={handleImageUpload}
                      style={{ display: 'none' }}
                    />
                    <label htmlFor="category-image-upload" className="btn btn-secondary" style={{ cursor: 'pointer' }}>
                      <FiUpload /> {uploading ? 'Yükleniyor...' : 'Görsel Yükle'}
                    </label>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Sıra</label>
                <input
                  type="number"
                  name="order"
                  value={formData.order}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <input
                    type="checkbox"
                    name="is_main_menu"
                    checked={formData.is_main_menu}
                    onChange={handleChange}
                  />
                  Ana menüde göster
                </label>
              </div>

              <div style={{ display: 'flex', gap: '1rem' }}>
                {editing && (
                  <button type="button" onClick={resetForm} className="btn btn-secondary">
                    İptal
                  </button>
                )}
                <button type="submit" className="btn btn-primary">
                  <FiPlus /> {editing ? 'Güncelle' : 'Oluştur'}
                </button>
              </div>
            </form>
          </div>

          <div className="admin-table">
            <table>
              <thead>
                <tr>
                  <th>Görsel</th>
                  <th>Kategori</th>
                  <th>Slug</th>
                  <th>Ana Menü</th>
                  <th>Sıra</th>
                  <th>İşlemler</th>
                </tr>
              </thead>
              <tbody>
                {categories.map((category) => (
                  <tr key={category._id}>
                    <td>
                      {category.featured_image ? (
                        <img
                          src={category.featured_image}
                          alt={category.name}
                          style={{
                            width: '50px',
                            height: '50px',
                            objectFit: 'cover',
                            borderRadius: '4px'
                          }}
                          onError={(e) => {
                            console.error('Resim yüklenemedi:', category.featured_image);
                            e.target.style.display = 'none';
                          }}
                        />
                      ) : (
                        <div style={{
                          width: '50px',
                          height: '50px',
                          background: '#f0f0f0',
                          borderRadius: '4px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: '#999',
                          fontSize: '10px'
                        }}>
                          Yok
                        </div>
                      )}
                    </td>
                    <td>{category.name}</td>
                    <td>{category.slug}</td>
                    <td>{category.is_main_menu ? '✓' : '-'}</td>
                    <td>{category.order}</td>
                    <td>
                      <div className="table-actions">
                        <button onClick={() => handleEdit(category)}>
                          <FiEdit2 />
                        </button>
                        <button onClick={() => handleDelete(category._id)}>
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
    </div>
  );
};

export default Categories;
