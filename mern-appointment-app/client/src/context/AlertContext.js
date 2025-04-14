import React, { createContext, useContext, useReducer } from 'react';
import { v4 as uuidv4 } from 'uuid';

// Initial state
const initialState = {
  alerts: []
};

// Action types
const SET_ALERT = 'SET_ALERT';
const REMOVE_ALERT = 'REMOVE_ALERT';

// Reducer function
const alertReducer = (state, action) => {
  const { type, payload } = action;

  switch (type) {
    case SET_ALERT:
      return {
        ...state,
        alerts: [...state.alerts, payload]
      };
    case REMOVE_ALERT:
      return {
        ...state,
        alerts: state.alerts.filter(alert => alert.id !== payload)
      };
    default:
      return state;
  }
};

// Create context
const AlertContext = createContext();

// Hook for using the alert context
export const useAlert = () => useContext(AlertContext);

// Provider component
export const AlertProvider = ({ children }) => {
  const [state, dispatch] = useReducer(alertReducer, initialState);

  // Add alert
  const addAlert = (msg, type = 'info', timeout = 5000) => {
    const id = uuidv4();
    
    dispatch({
      type: SET_ALERT,
      payload: { id, msg, type }
    });

    setTimeout(() => {
      dispatch({
        type: REMOVE_ALERT,
        payload: id
      });
    }, timeout);
  };

  return (
    <AlertContext.Provider
      value={{
        alerts: state.alerts,
        addAlert
      }}
    >
      {children}
    </AlertContext.Provider>
  );
};