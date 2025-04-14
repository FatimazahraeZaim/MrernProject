const Appointment = require('../models/Appointment');
const Agent = require('../models/Agent');
const Property = require('../models/Property');

// @desc    Créer un rendez-vous
// @route   POST /api/appointments
// @access  Private
exports.createAppointment = async (req, res) => {
  try {
    const { agent, property, date, startTime, endTime, notes, visitType } = req.body;

    // Vérifier que l'agent existe
    const agentExists = await Agent.findById(agent);
    if (!agentExists) {
      return res.status(404).json({ message: 'Agent non trouvé' });
    }

    // Vérifier que la propriété existe
    const propertyExists = await Property.findById(property);
    if (!propertyExists) {
      return res.status(404).json({ message: 'Propriété non trouvée' });
    }

    // Vérifier si l'horaire est disponible pour l'agent
    const appointmentDate = new Date(date);
    const dayOfWeek = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'][appointmentDate.getDay()];
    
    const agentAvailability = agentExists.availability.find(
      (a) => a.dayOfWeek === dayOfWeek
    );

    if (!agentAvailability) {
      return res.status(400).json({ message: `L'agent n'est pas disponible le ${dayOfWeek}` });
    }

    const requestStartTime = startTime;
    const requestEndTime = endTime;

    if (requestStartTime < agentAvailability.startTime || requestEndTime > agentAvailability.endTime) {
      return res.status(400).json({
        message: `L'horaire demandé n'est pas dans les heures de disponibilité de l'agent (${agentAvailability.startTime} - ${agentAvailability.endTime})`
      });
    }

    // Vérifier s'il existe déjà un rendez-vous pour cet agent à cette heure
    const existingAppointment = await Appointment.findOne({
      agent,
      date: { $eq: appointmentDate },
      $or: [
        { 
          startTime: { $lt: requestEndTime },
          endTime: { $gt: requestStartTime }
        }
      ]
    });

    if (existingAppointment) {
      return res.status(400).json({ message: 'Cet horaire est déjà réservé pour cet agent' });
    }

    // Créer le rendez-vous
    const appointment = await Appointment.create({
      client: req.user._id,
      agent,
      property,
      date: appointmentDate,
      startTime,
      endTime,
      notes,
      visitType
    });

    res.status(201).json(appointment);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Obtenir tous les rendez-vous de l'utilisateur
// @route   GET /api/appointments
// @access  Private
exports.getAppointments = async (req, res) => {
  try {
    let appointments;
    
    // Si l'utilisateur est un client, renvoyer ses rendez-vous
    if (req.user.role === 'client') {
      appointments = await Appointment.find({ client: req.user._id })
        .populate({
          path: 'agent',
          select: 'specialization',
          populate: {
            path: 'user',
            select: 'name email phone'
          }
        })
        .populate('property', 'title address status price images');
    } 
    // Si l'utilisateur est un agent, renvoyer les rendez-vous de ses propriétés
    else if (req.user.role === 'agent') {
      const agent = await Agent.findOne({ user: req.user._id });
      
      if (!agent) {
        return res.status(404).json({ message: 'Profil d\'agent non trouvé' });
      }
      
      appointments = await Appointment.find({ agent: agent._id })
        .populate('client', 'name email phone')
        .populate('property', 'title address status price images');
    }
    // Si l'utilisateur est un admin, renvoyer tous les rendez-vous
    else if (req.user.role === 'admin') {
      appointments = await Appointment.find({})
        .populate({
          path: 'agent',
          populate: {
            path: 'user',
            select: 'name email'
          }
        })
        .populate('client', 'name email phone')
        .populate('property', 'title address');
    }

    res.json(appointments);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Obtenir un rendez-vous par ID
// @route   GET /api/appointments/:id
// @access  Private
exports.getAppointmentById = async (req, res) => {
  try {
    const appointment = await Appointment.findById(req.params.id)
      .populate({
        path: 'agent',
        populate: {
          path: 'user',
          select: 'name email phone'
        }
      })
      .populate('client', 'name email phone')
      .populate('property', 'title description address status price images features');

    if (!appointment) {
      return res.status(404).json({ message: 'Rendez-vous non trouvé' });
    }

    // Vérifier que l'utilisateur est le client, l'agent ou un admin
    const agent = await Agent.findById(appointment.agent);
    
    if (
      req.user._id.toString() !== appointment.client._id.toString() &&
      agent.user.toString() !== req.user._id.toString() &&
      req.user.role !== 'admin'
    ) {
      return res.status(403).json({ message: 'Non autorisé' });
    }

    res.json(appointment);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};

// @desc    Mettre à jour le statut d'un rendez-vous
// @route   PUT /api/appointments/:id
// @access  Private
exports.updateAppointmentStatus = async (req, res) => {
  try {
    const { status, cancellationReason } = req.body;

    const appointment = await Appointment.findById(req.params.id);

    if (!appointment) {
      return res.status(404).json({ message: 'Rendez-vous non trouvé' });
    }

    // Vérifier que l'utilisateur est le client, l'agent ou un admin
    const agent = await Agent.findById(appointment.agent);
    
    if (
      req.user._id.toString() !== appointment.client.toString() &&
      agent.user.toString() !== req.user._id.toString() &&
      req.user.role !== 'admin'
    ) {
      return res.status(403).json({ message: 'Non autorisé' });
    }

    appointment.status = status || appointment.status;
    
    if (status === 'Annulé' && cancellationReason) {
      appointment.cancellationReason = cancellationReason;
    }

    const updatedAppointment = await appointment.save();
    res.json(updatedAppointment);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
};