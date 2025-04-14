require('dotenv').config();
const mongoose = require('mongoose');

async function testConnection() {
  try {
    console.log('Tentative de connexion à MongoDB Atlas...');
    console.log('URI MongoDB:', process.env.MONGO_URI ? 'défini' : 'non défini');
    
    if (!process.env.MONGO_URI) {
      throw new Error('MONGO_URI n\'est pas défini dans les variables d\'environnement');
    }
    
    await mongoose.connect(process.env.MONGO_URI, {
      serverSelectionTimeoutMS: 10000
    });
    
    console.log('Connexion réussie à MongoDB!');
    
    // Créer un modèle simple pour tester l'opération
    const TestModel = mongoose.model('Test', new mongoose.Schema({
      name: String,
      date: { type: Date, default: Date.now }
    }));
    
    // Créer un document de test
    const testDoc = new TestModel({ name: 'Test de connexion' });
    await testDoc.save();
    console.log('Document test créé avec succès!');
    
    // Récupérer le document pour confirmer
    const docs = await TestModel.find();
    console.log('Documents dans la collection Test:', docs);
    
    // Nettoyer
    await TestModel.deleteMany({});
    console.log('Collection Test nettoyée');
    
    // Fermer la connexion
    await mongoose.connection.close();
    console.log('Connexion fermée');
  } catch (error) {
    console.error('Erreur de connexion MongoDB:', error.message);
    console.error('Message d\'erreur complet:', error);
    
    if (error.name === 'MongooseServerSelectionError') {
      console.error('Détails de l\'erreur:', error.reason);
    }
  }
}

testConnection();