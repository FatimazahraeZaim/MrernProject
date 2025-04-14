import React from 'react';
import { useAlert } from '../../context/AlertContext';

const Alert = () => {
  const { alerts } = useAlert();

  return (
    <div className="alert-container">
      {alerts.length > 0 &&
        alerts.map(alert => (
          <div key={alert.id} className={`alert alert-${alert.type}`}>
            {alert.msg}
          </div>
        ))}
    </div>
  );
};

export default Alert;