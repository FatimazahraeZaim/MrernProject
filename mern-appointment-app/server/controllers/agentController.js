const Agent = require('../models/Agent');
const User = require('../models/User');

// @desc    Créer un profil d'agent
// @route   POST /api/agents
// @access  Private
exports.createAgentProfile = async (req, res) => {
  try {
    const {
      specialization,
      description,
      yearsOfExperience,
      languages,
      availability
    } = req.body;

    // Vérifier si l'utilisateur est déjà un agent
    const existingAgent = await Agent.findOne({ user: req.user._id });

    if (existingAgent) {
      return res.status(400).json({ message: 'Cet utilisateur possède déjà un profil d\'agent' });
    }

    // Mettre à jour le rôle de l'utilisateur en agent
    await User.findByIdAndUpdate(req.user._id, { role: 'agent' });

    // Créer un profil d'agent
    const agent = await Agent.create({
      user: req.user._id,
      specialization,
      description,
      yearsOfExperience,
      languages,
      availability
    });

    res.status(201).json(agent);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Obtenir tous les agents
// @route   GET /api/agents
// @access  Public
exports.getAgents = async (req, res) => {
  try {
    const agents = await Agent.find({})
      .populate('user', 'name email phone');
    
    res.json(agents);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Obtenir un agent par ID
// @route   GET /api/agents/:id
// @access  Public
exports.getAgentById = async (req, res) => {
  try {
    const agent = await Agent.findById(req.params.id)
      .populate('user', 'name email phone');
    
    if (agent) {
      res.json(agent);
    } else {
      res.status(404).json({ message: 'Agent non trouvé' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Mettre à jour un profil d'agent
// @route   PUT /api/agents/:id
// @access  Private
exports.updateAgentProfile = async (req, res) => {
  try {
    const agent = await Agent.findById(req.params.id);

    if (!agent) {
      return res.status(404).json({ message: 'Agent non trouvé' });
    }

    // Vérifier si l'utilisateur est l'agent ou un administrateur
    if (agent.user.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Non autorisé' });
    }

    const {
      specialization,
      description,
      yearsOfExperience,
      languages,
      availability
    } = req.body;

    // Mettre à jour les champs
    agent.specialization = specialization || agent.specialization;
    agent.description = description || agent.description;
    agent.yearsOfExperience = yearsOfExperience || agent.yearsOfExperience;
    agent.languages = languages || agent.languages;
    agent.availability = availability || agent.availability;

    const updatedAgent = await agent.save();
    res.json(updatedAgent);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Ajouter une évaluation à un agent
// @route   POST /api/agents/:id/reviews
// @access  Private
exports.addAgentReview = async (req, res) => {
  try {
    const { rating, comment } = req.body;

    const agent = await Agent.findById(req.params.id);

    if (!agent) {
      return res.status(404).json({ message: 'Agent non trouvé' });
    }

    // Vérifier si l'utilisateur a déjà évalué l'agent
    const alreadyReviewed = agent.reviews.find(
      (r) => r.user.toString() === req.user._id.toString()
    );

    if (alreadyReviewed) {
      return res.status(400).json({ message: 'Vous avez déjà évalué cet agent' });
    }

    const review = {
      user: req.user._id,
      rating: Number(rating),
      comment
    };

    agent.reviews.push(review);

    // Calculer la nouvelle moyenne des évaluations
    agent.averageRating = agent.reviews.reduce((acc, item) => item.rating + acc, 0) / agent.reviews.length;

    await agent.save();
    res.status(201).json({ message: 'Évaluation ajoutée' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};