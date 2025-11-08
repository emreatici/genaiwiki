import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { settingsAPI, categoriesAPI } from '../services/api';
import './Footer.css';

const Footer = () => {
  const [settings, setSettings] = useState(null);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    loadSettings();
    loadCategories();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await settingsAPI.get();
      setSettings(response.data);
    } catch (error) {
      console.error('Ayarlar yüklenemedi:', error);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      // Filter out 'main' category and limit to 6
      const filtered = response.data.filter(cat => cat.slug !== 'main').slice(0, 6);
      setCategories(filtered);
    } catch (error) {
      console.error('Kategoriler yüklenemedi:', error);
    }
  };

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>{settings?.site_title || 'GenAI Wiki'}</h3>
            <p>{settings?.site_description || 'Yapay zeka teknolojileri hakkında kapsamlı bilgi kaynağınız'}</p>
          </div>

          <div className="footer-section">
            <h4>Hızlı Bağlantılar</h4>
            <ul>
              {settings?.quick_links
                ?.sort((a, b) => (a.order || 0) - (b.order || 0))
                .map((link, index) => (
                  <li key={index}>
                    {link.external ? (
                      <a href={link.url} target="_blank" rel="noopener noreferrer">
                        {link.label}
                      </a>
                    ) : (
                      <Link to={link.url}>{link.label}</Link>
                    )}
                  </li>
                ))}
            </ul>
          </div>

          <div className="footer-section">
            <h4>Kategoriler</h4>
            <ul>
              {categories.map((category) => (
                <li key={category._id}>
                  <Link to={`/category/${category.slug}`}>{category.name}</Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>
            {settings?.footer_text
              ? settings.footer_text.replace('{year}', new Date().getFullYear())
              : `© ${new Date().getFullYear()} ${settings?.site_title || 'GenAI Wiki'}. Tüm hakları saklıdır.`
            }
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
