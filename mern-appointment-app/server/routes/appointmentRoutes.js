const express = require('express');
const router = express.Router();
const { 
  createAppointment, 
  getAppointments, 
  getAppointmentById, 
  updateAppointmentStatus 
} = require('../controllers/appointmentController');
const { protect } = require('../middleware/auth');

// Toutes les routes sont protégées
router.route('/')
  .post(protect, createAppointment)
  .get(protect, getAppointments);

router.route('/:id')
  .get(protect, getAppointmentById)
  .put(protect, updateAppointmentStatus);

module.exports = router;