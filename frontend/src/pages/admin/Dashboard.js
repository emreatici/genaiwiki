import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../services/AuthContext';
import { FiFileText, FiFolder, FiImage, FiSettings, FiUsers } from 'react-icons/fi';
import './AdminStyles.css';

const Dashboard = () => {
  const { user } = useAuth();

  const allMenuItems = [
    { title: 'Makaleler', icon: <FiFileText size={32} />, path: '/admin/articles', color: '#3b82f6', roles: ['admin', 'author'] },
    { title: 'Kategoriler', icon: <FiFolder size={32} />, path: '/admin/categories', color: '#8b5cf6', roles: ['admin'] },
    { title: 'Medya', icon: <FiImage size={32} />, path: '/admin/media', color: '#10b981', roles: ['admin'] },
    { title: 'Kullanıcılar', icon: <FiUsers size={32} />, path: '/admin/users', color: '#ec4899', roles: ['admin'] },
    { title: 'Ayarlar', icon: <FiSettings size={32} />, path: '/admin/settings', color: '#f59e0b', roles: ['admin'] },
  ];

  // Filter menu items based on user role
  const menuItems = allMenuItems.filter(item => item.roles.includes(user?.role));

  return (
    <div className="admin-page">
      <div className="container">
        <div className="admin-header">
          <h1>Content Manager</h1>
          <p>Hoş geldiniz, {user?.full_name || user?.username}!</p>
        </div>

        <div className="dashboard-grid">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className="dashboard-card"
              style={{ borderColor: item.color }}
            >
              <div className="dashboard-icon" style={{ background: item.color }}>
                {item.icon}
              </div>
              <h3>{item.title}</h3>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
