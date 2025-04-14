import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useAlert } from '../context/AlertContext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const { addAlert } = useAlert();
  const navigate = useNavigate();

  const { email, password } = formData;

  const onChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    
    const result = await login(email, password);
    
    setLoading(false);
    
    if (result.success) {
      addAlert('Connexion réussie', 'success');
      navigate('/dashboard');
    } else {
      addAlert(result.error || 'Erreur de connexion', 'danger');
    }
  };

  return (
    <section className="auth-page">
      <h1 className="large text-primary">Connexion</h1>
      <p className="lead">
        <i className="fas fa-user"></i> Connectez-vous à votre compte
      </p>
      
      <form className="form" onSubmit={onSubmit}>
        <div className="form-group">
          <input
            type="email"
            placeholder="Adresse e-mail"
            name="email"
            value={email}
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
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? 'Connexion en cours...' : 'Se connecter'}
        </button>
      </form>
      
      <p className="my-1">
        Vous n'avez pas de compte ? <Link to="/register">S'inscrire</Link>
      </p>
    </section>
  );
};

export default Login;