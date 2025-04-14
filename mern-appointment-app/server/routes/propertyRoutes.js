const express = require('express');
const router = express.Router();
const { 
  createProperty, 
  getProperties, 
  getPropertyById, 
  updateProperty, 
  deleteProperty 
} = require('../controllers/propertyController');
const { protect, agent } = require('../middleware/auth');

// Routes publiques
router.get('/', getProperties);
router.get('/:id', getPropertyById);

// Routes protégées (agent seulement)
router.post('/', protect, agent, createProperty);
router.put('/:id', protect, updateProperty);
router.delete('/:id', protect, deleteProperty);

module.exports = router;