const express = require('express');
const router = express.Router();
const { 
  createAgentProfile, 
  getAgents, 
  getAgentById, 
  updateAgentProfile, 
  addAgentReview 
} = require('../controllers/agentController');
const { protect, agent } = require('../middleware/auth');

// Routes publiques
router.get('/', getAgents);
router.get('/:id', getAgentById);

// Routes protégées
router.post('/', protect, createAgentProfile);
router.put('/:id', protect, agent, updateAgentProfile);
router.post('/:id/reviews', protect, addAgentReview);

module.exports = router;