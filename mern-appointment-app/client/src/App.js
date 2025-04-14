import React, { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './index.css';

// Layout Components
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Alert from './components/layout/Alert';

// Page Components
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

// Route Protection
import PrivateRoute from './components/routing/PrivateRoute';

// Auth Context
import { useAuth } from './context/AuthContext';

// Configuration d'Axios
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

const App = () => {
  const { loadUser } = useAuth();

  useEffect(() => {
    // Configurer l'intercepteur pour ajouter le token à chaque requête
    const requestInterceptor = axios.interceptors.request.use(
      config => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers['x-auth-token'] = token;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    // Charger l'utilisateur au démarrage
    loadUser();

    // Nettoyage
    return () => {
      axios.interceptors.request.eject(requestInterceptor);
    };
  }, [loadUser]);

  return (
    <>
      <Navbar />
      <Alert />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Routes protégées */}
          <Route element={<PrivateRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
          
          <Route element={<PrivateRoute allowedRoles={['agent']} />}>
            <Route path="/agent/properties" element={<div>Propriétés de l'agent (à venir)</div>} />
            <Route path="/agent/profile" element={<div>Profil de l'agent (à venir)</div>} />
          </Route>
        </Routes>
      </main>
      <Footer />
    </>
  );
};

export default App;