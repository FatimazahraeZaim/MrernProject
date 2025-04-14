import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useAlert } from '../context/AlertContext';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    password2: '',
    role: 'client'
  });
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const { addAlert } = useAlert();
  const navigate = useNavigate();

  const { name, email, phone, password, password2, role } = formData;

  const onChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = async e => {
    e.preventDefault();
    
    if (password !== password2) {
      addAlert('Les mots de passe ne correspondent pas', 'danger');
      return;
    }
    
    setLoading(true);
    
    const result = await register({
      name,
      email,
      phone,
      password,
      role
    });
    
    setLoading(false);
    
    if (result.success) {
      addAlert('Inscription réussie', 'success');
      navigate('/dashboard');
    } else {
      addAlert(result.error || 'Erreur lors de l\'inscription', 'danger');
    }
  };

  return (
    <section className="auth-page">
      <h1 className="large text-primary">Inscription</h1>
      <p className="lead">
        <i className="fas fa-user"></i> Créez votre compte
      </p>
      
      <form className="form" onSubmit={onSubmit}>
        <div className="form-group">
          <input
            type="text"
            placeholder="Nom complet"
            name="name"
            value={name}
            onChange={onChange}
            required
          />
        </div>
        <div className="form-group">
          <input
            type="email"
            placeholder="Adresse e-mail"
            name="email"
            value={email}
            onChange={onChange}
            required
          />
          <small className="form-text">
            Cette adresse e-mail sera utilisée pour votre profil
          </small>
        </div>
        <div className="form-group">
          <input
            type="tel"
            placeholder="Numéro de téléphone"
            name="phone"
            value={phone}
            onChange={onChange}
            required
          />
        </div>
        <div className="form-group">
          <input
            type="password"
            placeholder="Mot de passe"
            name="password"
            value={password}
            onChange={onChange}
            minLength="6"
            required
          />
        </div>
        <div className="form-group">
          <input
            type="password"
            placeholder="Confirmer le mot de passe"
            name="password2"
            value={password2}
            onChange={onChange}
            minLength="6"
            required
          />
        </div>
        <div className="form-group">
          <select name="role" value={role} onChange={onChange}>
            <option value="client">Client</option>
            <option value="agent">Agent immobilier</option>
          </select>
          <small className="form-text">
            Sélectionnez votre rôle sur la plateforme
          </small>
        </div>
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? 'Inscription en cours...' : 'S\'inscrire'}
        </button>
      </form>
      
      <p className="my-1">
        Vous avez déjà un compte ? <Link to="/login">Se connecter</Link>
      </p>
    </section>
  );
};

export default Register;