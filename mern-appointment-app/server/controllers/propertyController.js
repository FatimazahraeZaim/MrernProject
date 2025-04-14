const Property = require('../models/Property');
const Agent = require('../models/Agent');

// @desc    Créer une nouvelle propriété
// @route   POST /api/properties
// @access  Private (Agent seulement)
exports.createProperty = async (req, res) => {
  try {
    const {
      title,
      description,
      type,
      status,
      price,
      address,
      features,
      images
    } = req.body;

    // Vérifier si l'utilisateur est un agent
    const agent = await Agent.findOne({ user: req.user._id });

    if (!agent && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Seuls les agents peuvent créer des propriétés' });
    }

    // Créer une nouvelle propriété
    const property = await Property.create({
      title,
      description,
      type,
      status,
      price,
      address,
      features,
      images,
      agent: agent ? agent._id : null
    });

    res.status(201).json(property);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Obtenir toutes les propriétés
// @route   GET /api/properties
// @access  Public
exports.getProperties = async (req, res) => {
  try {
    // Extraction des paramètres de requête pour le filtrage
    const { type, status, minPrice, maxPrice, city, bedrooms } = req.query;

    // Construire l'objet de filtrage
    const filter = {};
    
    if (type) filter.type = type;
    if (status) filter.status = status;
    if (city) filter['address.city'] = { $regex: city, $options: 'i' };
    if (minPrice) filter.price = { ...filter.price, $gte: Number(minPrice) };
    if (maxPrice) filter.price = { ...filter.price, $lte: Number(maxPrice) };
    if (bedrooms) filter['features.bedrooms'] = Number(bedrooms);

    const properties = await Property.find(filter)
      .populate({
        path: 'agent',
        select: 'specialization yearsOfExperience averageRating',
        populate: {
          path: 'user',
          select: 'name email phone'
        }
      });
    
    res.json(properties);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Obtenir une propriété par ID
// @route   GET /api/properties/:id
// @access  Public
exports.getPropertyById = async (req, res) => {
  try {
    const property = await Property.findById(req.params.id)
      .populate({
        path: 'agent',
        select: 'specialization yearsOfExperience averageRating availability',
        populate: {
          path: 'user',
          select: 'name email phone'
        }
      });
    
    if (property) {
      res.json(property);
    } else {
      res.status(404).json({ message: 'Propriété non trouvée' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Mettre à jour une propriété
// @route   PUT /api/properties/:id
// @access  Private (Agent propriétaire ou Admin)
exports.updateProperty = async (req, res) => {
  try {
    const property = await Property.findById(req.params.id);

    if (!property) {
      return res.status(404).json({ message: 'Propriété non trouvée' });
    }

    // Vérifier si l'utilisateur est un agent et est propriétaire de cette propriété
    const agent = await Agent.findOne({ user: req.user._id });
    
    if (
      (agent && property.agent.toString() !== agent._id.toString()) &&
      req.user.role !== 'admin'
    ) {
      return res.status(403).json({ message: 'Non autorisé, vous n\'êtes pas le propriétaire de cette propriété' });
    }

    const {
      title,
      description,
      type,
      status,
      price,
      address,
      features,
      images
    } = req.body;

    // Mettre à jour les champs
    property.title = title || property.title;
    property.description = description || property.description;
    property.type = type || property.type;
    property.status = status || property.status;
    property.price = price || property.price;
    property.address = address || property.address;
    property.features = features || property.features;
    property.images = images || property.images;

    const updatedProperty = await property.save();
    res.json(updatedProperty);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Supprimer une propriété
// @route   DELETE /api/properties/:id
// @access  Private (Agent propriétaire ou Admin)
exports.deleteProperty = async (req, res) => {
  try {
    const property = await Property.findById(req.params.id);

    if (!property) {
      return res.status(404).json({ message: 'Propriété non trouvée' });
    }

    // Vérifier si l'utilisateur est un agent et est propriétaire de cette propriété
    const agent = await Agent.findOne({ user: req.user._id });
    
    if (
      (agent && property.agent.toString() !== agent._id.toString()) &&
      req.user.role !== 'admin'
    ) {
      return res.status(403).json({ message: 'Non autorisé, vous n\'êtes pas le propriétaire de cette propriété' });
    }

    await property.remove();
    res.json({ message: 'Propriété supprimée' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};