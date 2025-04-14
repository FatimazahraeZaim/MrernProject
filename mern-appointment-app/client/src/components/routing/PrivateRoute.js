import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const PrivateRoute = ({ allowedRoles = [] }) => {
  const { user, loading } = useAuth();

  // Si l'authentification est en cours de chargement, afficher un indicateur de chargement
  if (loading) {
    return <div>Chargement...</div>;
  }

  // Vérifier si l'utilisateur est connecté
  if (!user) {
    return <Navigate to="/login" />;
  }

  // Si des rôles spécifiques sont requis, vérifier si l'utilisateur a le bon rôle
  if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    return <Navigate to="/dashboard" />;
  }

  // Si tout est bon, rendre les composants enfants
  return <Outlet />;
};

export default PrivateRoute;