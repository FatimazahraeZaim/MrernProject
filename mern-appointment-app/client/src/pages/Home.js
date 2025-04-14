import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const { user } = useAuth();

  return (
    <section className="home-page">
      <div className="hero">
        <h1>Trouvez votre futur bien immobilier</h1>
        <p className="lead">
          Découvrez des propriétés exceptionnelles et réservez des rendez-vous avec des agents immobiliers professionnels
        </p>
        
        {!user ? (
          <div className="buttons">
            <Link to="/register" className="btn btn-primary">
              S'inscrire
            </Link>
            <Link to="/login" className="btn btn-outline">
              Se connecter
            </Link>
          </div>
        ) : (
          <div className="buttons">
            <Link to="/properties" className="btn btn-primary">
              Voir les propriétés
            </Link>
            <Link to="/dashboard" className="btn btn-outline">
              Mon tableau de bord
            </Link>
          </div>
        )}
      </div>

      <div className="features">
        <div className="feature-card">
          <i className="fas fa-search"></i>
          <h3>Recherchez</h3>
          <p>Des milliers de biens disponibles à la vente et à la location.</p>
        </div>
        <div className="feature-card">
          <i className="fas fa-calendar-alt"></i>
          <h3>Réservez</h3>
          <p>Planifiez des visites directement avec les agents immobiliers.</p>
        </div>
        <div className="feature-card">
          <i className="fas fa-home"></i>
          <h3>Emménagez</h3>
          <p>Trouvez le bien qui correspond à vos besoins et votre budget.</p>
        </div>
      </div>

      <div className="cta-section">
        <h2>Vous êtes un agent immobilier ?</h2>
        <p>Rejoignez notre plateforme pour promouvoir vos biens et gérer vos rendez-vous.</p>
        <Link to="/register" className="btn btn-success">
          Devenir agent
        </Link>
      </div>
    </section>
  );
};

export default Home;