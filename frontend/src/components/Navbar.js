import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import { settingsAPI } from '../services/api';
import { FiMenu, FiX, FiUser, FiLogOut } from 'react-icons/fi';
import './Navbar.css';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [settings, setSettings] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await settingsAPI.get();
      setSettings(response.data);
    } catch (error) {
      console.error('Ayarlar yüklenemedi:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            {settings?.show_logo && settings?.site_logo && (
              <img src={settings.site_logo} alt={settings.site_title} style={{ height: '40px', marginRight: '10px' }} />
            )}
            {settings?.show_title && (
              <h1>{settings?.site_title || 'GenAI Wiki'}</h1>
            )}
          </Link>

          <button
            className="mobile-menu-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>

          <div className={`navbar-menu ${mobileMenuOpen ? 'active' : ''}`}>
            <div className="navbar-links">
              <Link to="/" onClick={() => setMobileMenuOpen(false)}>Ana Sayfa</Link>

              {settings?.menu?.items
                ?.sort((a, b) => (a.order || 0) - (b.order || 0))
                .map((item, index) => (
                  item.external ? (
                    <a
                      key={index}
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {item.label}
                    </a>
                  ) : (
                    <Link
                      key={index}
                      to={item.url}
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {item.label}
                    </Link>
                  )
                ))}

              <Link to="/blog" onClick={() => setMobileMenuOpen(false)}>Blog</Link>
            </div>

            <div className="navbar-actions">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/admin"
                    className="btn btn-secondary"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <FiUser /> {user?.username}
                  </Link>
                  <button className="btn btn-primary" onClick={handleLogout}>
                    <FiLogOut /> Çıkış
                  </button>
                </>
              ) : (
                <Link
                  to="/login"
                  className="btn btn-primary"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Giriş Yap
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
