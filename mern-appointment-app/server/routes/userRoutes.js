const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const { protect } = require('../middleware/auth');

// Routes publiques
router.post('/', userController.registerUser);
router.post('/login', userController.loginUser);

// Routes protégées
router.get('/me', protect, userController.getUserProfile);
router.route('/profile')
  .get(protect, userController.getUserProfile)
  .put(protect, userController.updateUserProfile);

module.exports = router;