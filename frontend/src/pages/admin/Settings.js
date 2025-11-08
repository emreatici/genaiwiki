import React, { useState, useEffect } from 'react';
import { settingsAPI, mediaAPI } from '../../services/api';
import { toast } from 'react-toastify';
import { FiSave, FiUpload, FiTrash2, FiPlus, FiX } from 'react-icons/fi';
import './AdminStyles.css';

const Settings = () => {
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [settings, setSettings] = useState({
    site_title: '',
    site_logo: '',
    site_description: '',
    footer_text: '',
    show_logo: true,
    show_title: true,
    banner: {
      enabled: true,
      title: '',
      subtitle: '',
      background_image: '',
      text_color: '#ffffff',
      overlay_opacity: 0.5
    },
    middle_banner: {
      enabled: false,
      image: '',
      alt_text: '',
      link: '',
      external: false
    },
    menu: {
      items: []
    },
    quick_links: []
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await settingsAPI.get();
      setSettings(response.data);
    } catch (error) {
      toast.error('Ayarlar yüklenemedi');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setSettings({
        ...settings,
        [parent]: {
          ...settings[parent],
          [child]: type === 'checkbox' ? checked : value
        }
      });
    } else {
      setSettings({
        ...settings,
        [name]: type === 'checkbox' ? checked : value
      });
    }
  };

  const handleAddMenuItem = () => {
    const newItem = {
      label: '',
      url: '',
      order: settings.menu.items.length,
      external: false
    };
    setSettings({
      ...settings,
      menu: {
        ...settings.menu,
        items: [...settings.menu.items, newItem]
      }
    });
  };

  const handleRemoveMenuItem = (index) => {
    const newItems = settings.menu.items.filter((_, i) => i !== index);
    setSettings({
      ...settings,
      menu: {
        ...settings.menu,
        items: newItems
      }
    });
  };

  const handleMenuItemChange = (index, field, value) => {
    const newItems = [...settings.menu.items];
    newItems[index] = {
      ...newItems[index],
      [field]: field === 'external' ? value : value
    };
    setSettings({
      ...settings,
      menu: {
        ...settings.menu,
        items: newItems
      }
    });
  };

  const handleAddQuickLink = () => {
    const newLink = {
      label: '',
      url: '',
      order: settings.quick_links?.length || 0,
      external: false
    };
    setSettings({
      ...settings,
      quick_links: [...(settings.quick_links || []), newLink]
    });
  };

  const handleRemoveQuickLink = (index) => {
    const newLinks = settings.quick_links.filter((_, i) => i !== index);
    setSettings({
      ...settings,
      quick_links: newLinks
    });
  };

  const handleQuickLinkChange = (index, field, value) => {
    const newLinks = [...settings.quick_links];
    newLinks[index] = {
      ...newLinks[index],
      [field]: value
    };
    setSettings({
      ...settings,
      quick_links: newLinks
    });
  };

  const handleImageUpload = async (e, fieldPath) => {
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
      const formData = new FormData();
      formData.append('file', file);

      const response = await mediaAPI.upload(formData);
      const imageUrl = response.data.url;

      if (fieldPath.includes('.')) {
        const [parent, child] = fieldPath.split('.');
        setSettings({
          ...settings,
          [parent]: {
            ...settings[parent],
            [child]: imageUrl
          }
        });
      } else {
        setSettings({
          ...settings,
          [fieldPath]: imageUrl
        });
      }

      toast.success('Resim yüklendi');
    } catch (error) {
      toast.error('Resim yüklenemedi: ' + (error.response?.data?.error || error.message));
    } finally {
      setUploading(false);
    }
  };

  const handleRemoveImage = (fieldPath) => {
    if (fieldPath.includes('.')) {
      const [parent, child] = fieldPath.split('.');
      setSettings({
        ...settings,
        [parent]: {
          ...settings[parent],
          [child]: ''
        }
      });
    } else {
      setSettings({
        ...settings,
        [fieldPath]: ''
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await settingsAPI.update(settings);
      toast.success('Ayarlar kaydedildi');
      // Ayarları yeniden yükle
      await loadSettings();
      // Sayfayı yenile
      window.location.reload();
    } catch (error) {
      toast.error('Kayıt başarısız: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-page">
      <div className="container">
        <h2>Site Ayarları</h2>

        <form onSubmit={handleSubmit} className="admin-form">
          {/* Genel Ayarlar */}
          <div className="form-section">
            <h3>Genel Ayarlar</h3>

            <div className="form-group">
              <label>Site Başlığı *</label>
              <input
                type="text"
                name="site_title"
                value={settings.site_title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Site Açıklaması</label>
              <textarea
                name="site_description"
                value={settings.site_description}
                onChange={handleChange}
                rows="3"
              />
            </div>

            <div className="form-group">
              <label>Footer Metni</label>
              <input
                type="text"
                name="footer_text"
                value={settings.footer_text || ''}
                onChange={handleChange}
                placeholder="© {year} GenAI Wiki. Tüm hakları saklıdır."
              />
              <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                {'{year}'} otomatik olarak güncel yıl ile değiştirilir. Boş bırakılırsa varsayılan metin görünür.
              </p>
            </div>

            <div className="form-group">
              <label>Site Logosu</label>
              {settings.site_logo ? (
                <div className="image-preview">
                  <img src={settings.site_logo} alt="Logo" style={{ maxWidth: '200px', maxHeight: '100px', objectFit: 'contain' }} />
                  <button
                    type="button"
                    onClick={() => handleRemoveImage('site_logo')}
                    className="btn btn-danger btn-sm"
                    style={{ marginTop: '10px' }}
                  >
                    <FiTrash2 /> Logoyu Kaldır
                  </button>
                </div>
              ) : (
                <div>
                  <input
                    type="file"
                    id="logo-upload"
                    accept="image/*"
                    onChange={(e) => handleImageUpload(e, 'site_logo')}
                    style={{ display: 'none' }}
                  />
                  <label htmlFor="logo-upload" className="btn btn-secondary" style={{ cursor: 'pointer' }}>
                    <FiUpload /> {uploading ? 'Yükleniyor...' : 'Logo Yükle'}
                  </label>
                </div>
              )}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="show_logo"
                    checked={settings.show_logo !== false}
                    onChange={handleChange}
                  />
                  <span>Logoyu Göster</span>
                </label>
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="show_title"
                    checked={settings.show_title !== false}
                    onChange={handleChange}
                  />
                  <span>Site Başlığını Göster</span>
                </label>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="show_section_titles"
                    checked={settings.show_section_titles !== false}
                    onChange={handleChange}
                  />
                  <span>Başlıklar Görüntülensin</span>
                </label>
              </div>

              {settings.show_section_titles !== false && (
                <div className="form-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="show_main_section_title"
                      checked={settings.show_main_section_title !== false}
                      onChange={handleChange}
                    />
                    <span>Main Başlığı Görüntülensin</span>
                  </label>
                </div>
              )}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Ana Sayfada Görüntülenecek Makale Sayısı</label>
                <input
                  type="number"
                  name="homepage_articles_count"
                  value={settings.homepage_articles_count || 20}
                  onChange={handleChange}
                  min="1"
                  max="100"
                />
                <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                  Son makaleler bölümünde gösterilecek makale sayısı (1-100 arası)
                </p>
              </div>
            </div>
          </div>

          {/* Banner Ayarları */}
          <div className="form-section">
            <h3>Ana Sayfa Banner</h3>

            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  name="banner.enabled"
                  checked={settings.banner?.enabled}
                  onChange={handleChange}
                />
                {' '}Banner'ı Göster
              </label>
            </div>

            <div className="form-group">
              <label>Banner Başlığı</label>
              <input
                type="text"
                name="banner.title"
                value={settings.banner?.title || ''}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Banner Alt Başlığı</label>
              <input
                type="text"
                name="banner.subtitle"
                value={settings.banner?.subtitle || ''}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Banner Arkaplan Görseli</label>
              {settings.banner?.background_image ? (
                <div className="image-preview">
                  <img src={settings.banner.background_image} alt="Banner" style={{ maxWidth: '400px', maxHeight: '200px', objectFit: 'cover', borderRadius: '8px' }} />
                  <button
                    type="button"
                    onClick={() => handleRemoveImage('banner.background_image')}
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
                    id="banner-upload"
                    accept="image/*"
                    onChange={(e) => handleImageUpload(e, 'banner.background_image')}
                    style={{ display: 'none' }}
                  />
                  <label htmlFor="banner-upload" className="btn btn-secondary" style={{ cursor: 'pointer' }}>
                    <FiUpload /> {uploading ? 'Yükleniyor...' : 'Görsel Yükle'}
                  </label>
                </div>
              )}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Yazı Rengi</label>
                <input
                  type="color"
                  name="banner.text_color"
                  value={settings.banner?.text_color || '#ffffff'}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Arkaplan Opaklığı (0-1)</label>
                <input
                  type="number"
                  name="banner.overlay_opacity"
                  value={settings.banner?.overlay_opacity || 0.5}
                  onChange={handleChange}
                  step="0.1"
                  min="0"
                  max="1"
                />
              </div>
            </div>
          </div>

          {/* Orta Banner Ayarları */}
          <div className="form-section">
            <h3>Orta Banner (Konular ve Kategoriler Arası)</h3>

            <div style={{
              padding: '0.75rem',
              marginBottom: '1rem',
              background: '#fff3cd',
              border: '1px solid #ffc107',
              borderRadius: '8px',
              color: '#856404',
              fontSize: '14px'
            }}>
              <strong>📐 Önerilen Boyut:</strong> 1200x300 piksel (Yatay banner)
              <br />
              Kategoriler alanı ile aynı genişlikte görünecektir.
            </div>

            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="middle_banner.enabled"
                  checked={settings.middle_banner?.enabled || false}
                  onChange={handleChange}
                />
                <span>Orta Banner'ı Göster</span>
              </label>
            </div>

            {settings.middle_banner?.enabled && (
              <>
                <div className="form-group">
                  <label>Banner Görseli</label>
                  {settings.middle_banner?.image ? (
                    <div className="image-preview">
                      <img
                        src={settings.middle_banner.image}
                        alt="Middle Banner"
                        style={{
                          maxWidth: '100%',
                          maxHeight: '200px',
                          objectFit: 'contain',
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)'
                        }}
                      />
                      <button
                        type="button"
                        onClick={() => handleRemoveImage('middle_banner.image')}
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
                        id="middle-banner-upload"
                        accept="image/*"
                        onChange={(e) => handleImageUpload(e, 'middle_banner.image')}
                        style={{ display: 'none' }}
                      />
                      <label htmlFor="middle-banner-upload" className="btn btn-secondary" style={{ cursor: 'pointer' }}>
                        <FiUpload /> {uploading ? 'Yükleniyor...' : 'Görsel Yükle (1200x300px)'}
                      </label>
                    </div>
                  )}
                </div>

                <div className="form-group">
                  <label>Alternatif Metin (Alt Text)</label>
                  <input
                    type="text"
                    name="middle_banner.alt_text"
                    value={settings.middle_banner?.alt_text || ''}
                    onChange={handleChange}
                    placeholder="Banner açıklaması"
                  />
                </div>

                <div className="form-group">
                  <label>Banner Linki (Opsiyonel)</label>
                  <input
                    type="text"
                    name="middle_banner.link"
                    value={settings.middle_banner?.link || ''}
                    onChange={handleChange}
                    placeholder="Örn: /article/yeni-makale veya https://example.com"
                  />
                  <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                    Banner'a tıklandığında gidilecek sayfa. Boş bırakılırsa tıklanamaz.
                  </p>
                </div>

                <div className="form-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="middle_banner.external"
                      checked={settings.middle_banner?.external || false}
                      onChange={handleChange}
                    />
                    <span>Harici Link (Yeni sekmede aç)</span>
                  </label>
                </div>
              </>
            )}
          </div>

          {/* Menü Ayarları */}
          <div className="form-section">
            <h3>Menü Yönetimi</h3>

            {/* Bilgilendirme */}
            <div style={{
              padding: '1rem',
              marginBottom: '1.5rem',
              background: '#e3f2fd',
              border: '1px solid #2196f3',
              borderRadius: '8px',
              color: '#1565c0'
            }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#1565c0' }}>ℹ️ Menü Nasıl Yönetilir?</h4>
              <p style={{ margin: '0 0 0.5rem 0', fontSize: '14px' }}>
                <strong>Ana Menü Kategorileri:</strong> Kategoriler sayfasından "Ana menüde göster" işaretleyerek kategorilerinizi menüye ekleyebilirsiniz.
              </p>
              <p style={{ margin: '0', fontSize: '14px' }}>
                <strong>Özel Linkler:</strong> Bu bölümden harici bağlantılar veya özel sayfalar için ek menü öğeleri ekleyebilirsiniz.
              </p>
            </div>

            <p style={{ marginBottom: '1rem', color: '#666' }}>
              Özel menü linkleri ekleyin (opsiyonel - harici bağlantılar, özel sayfalar vb.)
            </p>

            {settings.menu?.items?.map((item, index) => (
              <div key={index} style={{
                padding: '1rem',
                marginBottom: '1rem',
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                backgroundColor: 'var(--bg-secondary)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <h4 style={{ margin: 0 }}>Menü Öğesi #{index + 1}</h4>
                  <button
                    type="button"
                    onClick={() => handleRemoveMenuItem(index)}
                    className="btn btn-danger btn-sm"
                  >
                    <FiX /> Kaldır
                  </button>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Etiket (Görünen İsim) *</label>
                    <input
                      type="text"
                      value={item.label}
                      onChange={(e) => handleMenuItemChange(index, 'label', e.target.value)}
                      placeholder="Örn: Hakkımızda"
                    />
                  </div>

                  <div className="form-group">
                    <label>URL / Yol *</label>
                    <input
                      type="text"
                      value={item.url}
                      onChange={(e) => handleMenuItemChange(index, 'url', e.target.value)}
                      placeholder="Örn: /about veya https://example.com"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Sıra</label>
                    <input
                      type="number"
                      value={item.order}
                      onChange={(e) => handleMenuItemChange(index, 'order', parseInt(e.target.value))}
                      min="0"
                    />
                  </div>

                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={item.external || false}
                        onChange={(e) => handleMenuItemChange(index, 'external', e.target.checked)}
                      />
                      <span>Harici Link (Yeni sekmede aç)</span>
                    </label>
                  </div>
                </div>
              </div>
            ))}

            <button
              type="button"
              onClick={handleAddMenuItem}
              className="btn btn-secondary"
              style={{ width: '100%' }}
            >
              <FiPlus /> Yeni Menü Öğesi Ekle
            </button>
          </div>

          {/* Hızlı Bağlantılar Yönetimi (Footer) */}
          <div className="form-section">
            <h3>Hızlı Bağlantılar Yönetimi (Footer)</h3>

            {/* Bilgilendirme */}
            <div style={{
              padding: '1rem',
              marginBottom: '1.5rem',
              background: '#e8f5e9',
              border: '1px solid #4caf50',
              borderRadius: '8px',
              color: '#2e7d32'
            }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#2e7d32' }}>ℹ️ Hızlı Bağlantılar Nedir?</h4>
              <p style={{ margin: '0', fontSize: '14px' }}>
                Footer bölümünde görünen "Hızlı Bağlantılar" menüsünü buradan yönetebilirsiniz.
                "Giriş Yap" linkini de buraya normal bir item olarak ekleyebilirsiniz.
              </p>
            </div>

            <p style={{ marginBottom: '1rem', color: '#666' }}>
              Footer'da görünecek hızlı bağlantıları ekleyin
            </p>

            {settings.quick_links?.map((link, index) => (
              <div key={index} style={{
                padding: '1rem',
                marginBottom: '1rem',
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                backgroundColor: 'var(--bg-secondary)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <h4 style={{ margin: 0 }}>Bağlantı #{index + 1}</h4>
                  <button
                    type="button"
                    onClick={() => handleRemoveQuickLink(index)}
                    className="btn btn-danger btn-sm"
                  >
                    <FiX /> Kaldır
                  </button>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Etiket (Görünen İsim) *</label>
                    <input
                      type="text"
                      value={link.label}
                      onChange={(e) => handleQuickLinkChange(index, 'label', e.target.value)}
                      placeholder="Örn: Ana Sayfa, Blog, Giriş Yap"
                    />
                  </div>

                  <div className="form-group">
                    <label>URL / Yol *</label>
                    <input
                      type="text"
                      value={link.url}
                      onChange={(e) => handleQuickLinkChange(index, 'url', e.target.value)}
                      placeholder="Örn: /, /blog, /login"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Sıra</label>
                    <input
                      type="number"
                      value={link.order}
                      onChange={(e) => handleQuickLinkChange(index, 'order', parseInt(e.target.value))}
                      min="0"
                    />
                  </div>

                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={link.external || false}
                        onChange={(e) => handleQuickLinkChange(index, 'external', e.target.checked)}
                      />
                      <span>Harici Link (Yeni sekmede aç)</span>
                    </label>
                  </div>
                </div>
              </div>
            ))}

            <button
              type="button"
              onClick={handleAddQuickLink}
              className="btn btn-secondary"
              style={{ width: '100%' }}
            >
              <FiPlus /> Yeni Hızlı Bağlantı Ekle
            </button>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading || uploading}>
              <FiSave /> {loading ? 'Kaydediliyor...' : 'Kaydet'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Settings;
