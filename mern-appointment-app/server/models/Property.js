const mongoose = require('mongoose');

const PropertySchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  type: {
    type: String,
    enum: ['Appartement', 'Maison', 'Villa', 'Bureau', 'Local commercial', 'Terrain'],
    required: true
  },
  status: {
    type: String,
    enum: ['À vendre', 'À louer', 'Vendu', 'Loué'],
    required: true
  },
  price: {
    type: Number,
    required: true
  },
  address: {
    street: {
      type: String,
      required: true
    },
    city: {
      type: String,
      required: true
    },
    postalCode: {
      type: String,
      required: true
    },
    country: {
      type: String,
      required: true,
      default: 'France'
    }
  },
  features: {
    area: {
      type: Number,
      required: true
    },
    bedrooms: {
      type: Number,
      default: 0
    },
    bathrooms: {
      type: Number,
      default: 0
    },
    floor: {
      type: Number
    },
    parking: {
      type: Boolean,
      default: false
    },
    garden: {
      type: Boolean,
      default: false
    },
    elevator: {
      type: Boolean,
      default: false
    },
    constructionYear: {
      type: Number
    }
  },
  images: [{
    url: {
      type: String,
      required: true
    },
    caption: {
      type: String
    }
  }],
  agent: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Agent',
    required: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Property', PropertySchema);