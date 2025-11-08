import React, { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { mediaAPI } from '../../services/api';
import { toast } from 'react-toastify';
import { FiUpload, FiTrash2, FiCopy } from 'react-icons/fi';
import './AdminStyles.css';

const Media = () => {
  const [media, setMedia] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMedia();
  }, []);

  const loadMedia = async () => {
    try {
      const response = await mediaAPI.getAll();
      setMedia(response.data.media);
    } catch (error) {
      toast.error('Medya yüklenemedi');
    }
  };

  const onDrop = useCallback(async (acceptedFiles) => {
    setLoading(true);

    for (const file of acceptedFiles) {
      try {
        const formData = new FormData();
        formData.append('file', file);

        await mediaAPI.upload(formData);
        toast.success(`${file.name} yüklendi`);
      } catch (error) {
        toast.error(`${file.name} yüklenemedi: ${error.response?.data?.error || error.message}`);
      }
    }

    setLoading(false);
    loadMedia();
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
      'video/*': ['.mp4', '.webm'],
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  const handleDelete = async (id) => {
    if (!window.confirm('Bu medyayı silmek istediğinizden emin misiniz?')) return;

    try {
      await mediaAPI.delete(id);
      toast.success('Medya silindi');
      loadMedia();
    } catch (error) {
      toast.error('Silme işlemi başarısız');
    }
  };

  const copyUrl = (url) => {
    navigator.clipboard.writeText(url);
    toast.success('URL kopyalandı');
  };

  return (
    <div className="admin-page">
      <div className="container">
        <h2>Medya Kütüphanesi</h2>

        <div {...getRootProps()} className="upload-zone">
          <input {...getInputProps()} />
          <FiUpload size={48} style={{ margin: '0 auto', display: 'block', marginBottom: '1rem' }} />
          {isDragActive ? (
            <p>Dosyaları buraya bırakın...</p>
          ) : (
            <p>Dosya yüklemek için tıklayın veya sürükleyin<br />
            <small>Desteklenen formatlar: PNG, JPG, GIF, WebP, MP4, WebM, PDF</small></p>
          )}
        </div>

        {loading && (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div className="spinner" style={{ margin: '0 auto' }}></div>
            <p>Dosyalar yükleniyor...</p>
          </div>
        )}

        <div className="media-grid">
          {media.map((item) => (
            <div key={item._id} className="media-item">
              {item.file_type === 'image' ? (
                <img src={item.url} alt={item.alt_text || item.original_filename} />
              ) : item.file_type === 'video' ? (
                <video src={item.url} />
              ) : (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100%',
                  background: 'var(--bg-secondary)',
                  fontSize: '0.875rem',
                  padding: '1rem',
                  textAlign: 'center'
                }}>
                  {item.original_filename}
                </div>
              )}
              <div className="media-item-actions">
                <button
                  onClick={() => copyUrl(item.url)}
                  title="URL'yi kopyala"
                  style={{ background: 'var(--primary-color)', color: 'white', padding: '0.5rem', borderRadius: '4px' }}
                >
                  <FiCopy />
                </button>
                <button
                  onClick={() => handleDelete(item._id)}
                  title="Sil"
                  style={{ background: 'var(--error)', color: 'white', padding: '0.5rem', borderRadius: '4px' }}
                >
                  <FiTrash2 />
                </button>
              </div>
            </div>
          ))}
        </div>

        {media.length === 0 && !loading && (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
            Henüz medya yüklenmemiş.
          </div>
        )}
      </div>
    </div>
  );
};

export default Media;
