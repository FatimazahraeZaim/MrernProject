import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const authLinks = (
    <ul>
      <li>
        <Link to="/dashboard">Tableau de bord</Link>
      </li>
      <li>
        <Link to="/properties">Propriétés</Link>
      </li>
      {user && user.role === 'agent' && (
        <li>
          <Link to="/agent/properties">Mes Propriétés</Link>
        </li>
      )}
      <li>
        <a onClick={handleLogout} href="#!">
          <i className="fas fa-sign-out-alt"></i>{' '}
          <span className="hide-sm">Déconnexion</span>
        </a>
      </li>
    </ul>
  );

  const guestLinks = (
    <ul>
      <li>
        <Link to="/properties">Propriétés</Link>
      </li>
      <li>
        <Link to="/register">Inscription</Link>
      </li>
      <li>
        <Link to="/login">Connexion</Link>
      </li>
    </ul>
  );

  return (
    <nav className="navbar">
      <h1>
        <Link to="/">
          <i className="fas fa-building"></i> ImmoRDV
        </Link>
      </h1>
      {user ? authLinks : guestLinks}
    </nav>
  );
};

export default Navbar;