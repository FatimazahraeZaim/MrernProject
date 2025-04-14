import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useAlert } from '../context/AlertContext';

const Dashboard = () => {
  const { user } = useAuth();
  const { addAlert } = useAlert();
  
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const res = await axios.get('/api/appointments');
        setAppointments(res.data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        addAlert('Erreur lors du chargement des rendez-vous', 'danger');
        setLoading(false);
      }
    };

    fetchAppointments();
  }, [addAlert]);

  const updateAppointmentStatus = async (id, status, cancellationReason = '') => {
    try {
      await axios.put(`/api/appointments/${id}`, { 
        status, 
        cancellationReason 
      });
      
      // Mettre à jour l'état local
      setAppointments(
        appointments.map(appointment => 
          appointment._id === id 
            ? { ...appointment, status, cancellationReason } 
            : appointment
        )
      );
      
      addAlert(`Rendez-vous ${status === 'Annulé' ? 'annulé' : 'mis à jour'}`, 'success');
    } catch (err) {
      console.error(err);
      addAlert('Erreur lors de la mise à jour du rendez-vous', 'danger');
    }
  };

  // Fonction pour formater la date
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
  };

  const renderAppointments = () => {
    if (appointments.length === 0) {
      return (
        <div className="no-appointments">
          <p>Vous n'avez pas encore de rendez-vous.</p>
          <Link to="/properties" className="btn btn-primary">
            Voir les propriétés
          </Link>
        </div>
      );
    }

    return appointments.map(appointment => (
      <div key={appointment._id} className="appointment-card">
        <div className="appointment-header">
          <h3>{appointment.property.title}</h3>
          <span className={`badge badge-${getBadgeColor(appointment.status)}`}>
            {appointment.status}
          </span>
        </div>
        
        <div className="appointment-details">
          <p>
            <strong>Date:</strong> {formatDate(appointment.date)}
          </p>
          <p>
            <strong>Heure:</strong> {appointment.startTime} - {appointment.endTime}
          </p>
          <p>
            <strong>Type de visite:</strong> {appointment.visitType}
          </p>
          
          {user.role === 'client' && (
            <p>
              <strong>Agent:</strong> {appointment.agent.user.name}
            </p>
          )}
          
          {user.role === 'agent' && (
            <p>
              <strong>Client:</strong> {appointment.client.name}
            </p>
          )}
          
          {appointment.notes && (
            <p>
              <strong>Notes:</strong> {appointment.notes}
            </p>
          )}
          
          {appointment.cancellationReason && (
            <p>
              <strong>Raison d'annulation:</strong> {appointment.cancellationReason}
            </p>
          )}
        </div>
        
        <div className="appointment-actions">
          {appointment.status === 'En attente' && (
            <>
              <button 
                className="btn btn-success"
                onClick={() => updateAppointmentStatus(appointment._id, 'Confirmé')}
              >
                Confirmer
              </button>
              <button 
                className="btn btn-danger"
                onClick={() => {
                  const reason = prompt('Raison de l\'annulation:');
                  if (reason) {
                    updateAppointmentStatus(appointment._id, 'Annulé', reason);
                  }
                }}
              >
                Annuler
              </button>
            </>
          )}
          
          {appointment.status === 'Confirmé' && (
            <button 
              className="btn btn-danger"
              onClick={() => {
                const reason = prompt('Raison de l\'annulation:');
                if (reason) {
                  updateAppointmentStatus(appointment._id, 'Annulé', reason);
                }
              }}
            >
              Annuler
            </button>
          )}
          
          <Link 
            to={`/properties/${appointment.property._id}`} 
            className="btn btn-outline"
          >
            Voir la propriété
          </Link>
        </div>
      </div>
    ));
  };

  // Fonction pour déterminer la couleur du badge en fonction du statut
  const getBadgeColor = (status) => {
    switch (status) {
      case 'Confirmé':
        return 'success';
      case 'En attente':
        return 'warning';
      case 'Annulé':
        return 'danger';
      case 'Terminé':
        return 'dark';
      default:
        return 'primary';
    }
  };

  // Gérer les sections en fonction du rôle de l'utilisateur
  const renderAgentSection = () => {
    if (user.role !== 'agent') return null;
    
    return (
      <div className="agent-section">
        <h2>Gestion d'agent</h2>
        <div className="agent-actions">
          <Link to="/agent/properties" className="btn btn-primary">
            Mes propriétés
          </Link>
          <Link to="/agent/profile" className="btn btn-outline">
            Profil d'agent
          </Link>
          <Link to="/agent/availability" className="btn btn-outline">
            Gérer mes disponibilités
          </Link>
        </div>
      </div>
    );
  };

  return (
    <section className="dashboard">
      <h1 className="large text-primary">Tableau de bord</h1>
      
      <div className="dashboard-welcome">
        <h2>Bienvenue, {user && user.name}</h2>
        <p>
          {user && user.role === 'client' 
            ? 'Gérez vos rendez-vous immobiliers ici' 
            : 'Gérez vos rendez-vous et propriétés ici'}
        </p>
      </div>
      
      {renderAgentSection()}
      
      <div className="dashboard-appointments">
        <h2>Mes rendez-vous</h2>
        
        {loading ? (
          <p>Chargement des rendez-vous...</p>
        ) : (
          <div className="appointments-list">
            {renderAppointments()}
          </div>
        )}
      </div>
    </section>
  );
};

export default Dashboard;