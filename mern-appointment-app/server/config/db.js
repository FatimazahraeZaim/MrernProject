const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');

let mongoServer;

const connectDB = async () => {
  try {
    console.log('Tentative de connexion à MongoDB...');
    
    // Vérifier l'environnement
    if (process.env.NODE_ENV === 'production' && process.env.MONGO_URI) {
      // Utiliser MongoDB Atlas en production
      console.log('Mode production : Connexion à MongoDB Atlas...');
      
      const conn = await mongoose.connect(process.env.MONGO_URI, {
        serverSelectionTimeoutMS: 10000
      });
      
      console.log(`MongoDB Atlas connecté: ${conn.connection.host}`);
    } else {
      // Utiliser MongoDB Memory Server en développement
      console.log('Mode développement : Création d\'une base de données MongoDB en mémoire...');
      
      mongoServer = await MongoMemoryServer.create();
      const uri = mongoServer.getUri();
      
      const conn = await mongoose.connect(uri, {
        serverSelectionTimeoutMS: 10000
      });
      
      console.log(`MongoDB Memory Server connecté: ${conn.connection.host}`);
      console.log('ATTENTION: Vous utilisez une base de données en mémoire. Les données seront perdues à chaque redémarrage.');
    }
  } catch (error) {
    console.error(`Erreur de connexion MongoDB: ${error.message}`);
    
    if (process.env.NODE_ENV === 'production') {
      console.error('Assurez-vous que votre adresse IP est autorisée dans MongoDB Atlas et que la chaîne de connexion est correcte');
    } else {
      console.error('Erreur lors de la création de la base de données en mémoire');
    }
    
    // Ne quittez pas le processus pour que le serveur reste en ligne
    // process.exit(1);
  }
};

// Fonction pour fermer proprement la connexion
const closeDatabase = async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.connection.close();
  
  if (mongoServer) {
    await mongoServer.stop();
  }
};

module.exports = { connectDB, closeDatabase };