import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>ImmoRDV</h3>
            <p>
              Votre plateforme de réservation de rendez-vous immobiliers en ligne.
              Trouvez le bien de vos rêves et rencontrez des agents qualifiés.
            </p>
          </div>
          <div className="footer-section">
            <h3>Liens rapides</h3>
            <ul>
              <li><Link to="/">Accueil</Link></li>
              <li><Link to="/properties">Propriétés</Link></li>
              <li><Link to="/login">Connexion</Link></li>
              <li><Link to="/register">Inscription</Link></li>
            </ul>
          </div>
          <div className="footer-section">
            <h3>Contact</h3>
            <p>
              <i className="fas fa-map-marker-alt"></i> 123 Rue de l'Immobilier, Paris
            </p>
            <p>
              <i className="fas fa-phone"></i> +33 1 23 45 67 89
            </p>
            <p>
              <i className="fas fa-envelope"></i> contact@immordv.fr
            </p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {year} ImmoRDV. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;