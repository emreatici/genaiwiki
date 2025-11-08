import React, { useState, useEffect } from 'react';
import { usersAPI } from '../../services/api';
import { toast } from 'react-toastify';
import { FiEdit2, FiTrash2, FiUser, FiShield, FiPlus } from 'react-icons/fi';
import './AdminStyles.css';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingUser, setEditingUser] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'author',
    is_active: true
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const response = await usersAPI.getAll();
      setUsers(response.data);
    } catch (error) {
      toast.error('Kullanıcılar yüklenemedi: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleNew = () => {
    setIsCreating(true);
    setFormData({
      username: '',
      email: '',
      password: '',
      full_name: '',
      role: 'author',
      is_active: true
    });
    setEditingUser(null);
    setShowModal(true);
  };

  const handleEdit = (user) => {
    setIsCreating(false);
    setEditingUser({ ...user });
    setShowModal(true);
  };

  const handleCreate = async () => {
    try {
      await usersAPI.create(formData);
      toast.success('Kullanıcı oluşturuldu');
      setShowModal(false);
      loadUsers();
    } catch (error) {
      toast.error('Oluşturma başarısız: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleSave = async () => {
    try {
      await usersAPI.update(editingUser._id, {
        role: editingUser.role,
        is_active: editingUser.is_active
      });
      toast.success('Kullanıcı güncellendi');
      setShowModal(false);
      loadUsers();
    } catch (error) {
      toast.error('Güncelleme başarısız: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Bu kullanıcıyı silmek istediğinizden emin misiniz?')) {
      return;
    }

    try {
      await usersAPI.delete(userId);
      toast.success('Kullanıcı silindi');
      loadUsers();
    } catch (error) {
      toast.error('Silme başarısız: ' + (error.response?.data?.error || error.message));
    }
  };

  const getRoleBadge = (role) => {
    const roleMap = {
      admin: { text: 'Admin', className: 'role-badge-admin', icon: <FiShield /> },
      author: { text: 'Yazar', className: 'role-badge-author', icon: <FiEdit2 /> }
    };
    const roleData = roleMap[role] || roleMap.author;
    return (
      <span className={`role-badge ${roleData.className}`}>
        {roleData.icon} {roleData.text}
      </span>
    );
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  return (
    <div className="admin-page">
      <div className="container">
        <div className="admin-header">
          <div>
            <h2>Kullanıcı Yönetimi</h2>
            <p>Kullanıcıları görüntüleyin, yeni kullanıcı ekleyin veya silin</p>
          </div>
          <button className="btn btn-primary" onClick={handleNew}>
            <FiPlus /> Yeni Kullanıcı
          </button>
        </div>

        <div className="admin-table">
          <table>
            <thead>
              <tr>
                <th>Kullanıcı Adı</th>
                <th>Email</th>
                <th>Tam Ad</th>
                <th>Rol</th>
                <th>Durum</th>
                <th>Son Giriş</th>
                <th>İşlemler</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user._id}>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{user.full_name || '-'}</td>
                  <td>{getRoleBadge(user.role)}</td>
                  <td>
                    <span className={`status-badge ${user.is_active ? 'status-published' : 'status-draft'}`}>
                      {user.is_active ? 'Aktif' : 'Pasif'}
                    </span>
                  </td>
                  <td>
                    {user.last_login
                      ? new Date(user.last_login).toLocaleDateString('tr-TR')
                      : 'Hiç giriş yapmadı'}
                  </td>
                  <td>
                    <div className="table-actions">
                      <button
                        onClick={() => handleEdit(user)}
                        className="btn-icon"
                        title="Düzenle"
                      >
                        <FiEdit2 />
                      </button>
                      <button
                        onClick={() => handleDelete(user._id)}
                        className="btn-icon btn-danger"
                        title="Sil"
                      >
                        <FiTrash2 />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Create/Edit Modal */}
        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h3>{isCreating ? 'Yeni Kullanıcı Oluştur' : 'Kullanıcı Düzenle'}</h3>

              {isCreating ? (
                <>
                  <div className="form-group">
                    <label>Kullanıcı Adı *</label>
                    <input
                      type="text"
                      value={formData.username}
                      onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                      placeholder="kullanici_adi"
                    />
                  </div>
                  <div className="form-group">
                    <label>Email *</label>
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="email@example.com"
                    />
                  </div>
                  <div className="form-group">
                    <label>Şifre *</label>
                    <input
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      placeholder="••••••••"
                    />
                  </div>
                  <div className="form-group">
                    <label>Tam Ad *</label>
                    <input
                      type="text"
                      value={formData.full_name}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                      placeholder="Adı Soyadı"
                    />
                  </div>
                  <div className="form-group">
                    <label>Rol *</label>
                    <select
                      value={formData.role}
                      onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    >
                      <option value="admin">Admin (Tam Yetki)</option>
                      <option value="author">Yazar (Sadece Makale Yazma)</option>
                    </select>
                  </div>
                </>
              ) : editingUser && (
                <>
                  <div className="form-group">
                    <label>Kullanıcı Adı</label>
                    <input type="text" value={editingUser.username} disabled />
                  </div>
                  <div className="form-group">
                    <label>Email</label>
                    <input type="text" value={editingUser.email} disabled />
                  </div>
                  <div className="form-group">
                    <label>Rol</label>
                    <select
                      value={editingUser.role}
                      onChange={(e) => setEditingUser({ ...editingUser, role: e.target.value })}
                    >
                      <option value="admin">Admin (Tam Yetki)</option>
                      <option value="author">Yazar (Sadece Makale Yazma)</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={editingUser.is_active}
                        onChange={(e) => setEditingUser({ ...editingUser, is_active: e.target.checked })}
                      />
                      <span>Aktif</span>
                    </label>
                  </div>
                </>
              )}

              <div className="modal-actions">
                <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  İptal
                </button>
                <button
                  className="btn btn-primary"
                  onClick={isCreating ? handleCreate : handleSave}
                >
                  {isCreating ? 'Oluştur' : 'Kaydet'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .admin-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 2rem;
        }
        .role-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.25rem;
          padding: 0.25rem 0.75rem;
          border-radius: 20px;
          font-size: 0.875rem;
          font-weight: 500;
        }
        .role-badge-admin {
          background: #fce7f3;
          color: #be185d;
        }
        .role-badge-author {
          background: #dbeafe;
          color: #1e40af;
        }
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }
        .modal-content {
          background: var(--bg-primary);
          padding: 2rem;
          border-radius: 12px;
          min-width: 400px;
          max-width: 500px;
        }
        .modal-content h3 {
          margin-bottom: 1.5rem;
          color: var(--text-primary);
        }
        .modal-actions {
          display: flex;
          gap: 1rem;
          justify-content: flex-end;
          margin-top: 1.5rem;
        }
        .btn-icon {
          background: none;
          border: none;
          cursor: pointer;
          padding: 0.5rem;
          color: var(--text-primary);
          transition: color 0.2s;
        }
        .btn-icon:hover {
          color: var(--primary-color);
        }
        .btn-icon.btn-danger:hover {
          color: #dc2626;
        }
      `}</style>
    </div>
  );
};

export default Users;
