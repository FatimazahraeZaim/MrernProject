const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Chemins
const clientPath = path.join(__dirname, 'client');
const buildPath = path.join(clientPath, 'build');

// Fonction pour vérifier si le build a déjà été effectué
function buildExists() {
  return fs.existsSync(buildPath) && fs.readdirSync(buildPath).length > 0;
}

// Construire l'application React
try {
  console.log('Compilation du client React...');
  
  // Installer les dépendances du client si elles ne sont pas déjà installées
  if (!fs.existsSync(path.join(clientPath, 'node_modules'))) {
    console.log('Installation des dépendances du client...');
    execSync('npm install', { 
      cwd: clientPath,
      stdio: 'inherit'
    });
  }
  
  // Construire l'application React
  if (!buildExists()) {
    console.log('Construction de l\'application React...');
    execSync('npm run build', { 
      cwd: clientPath,
      stdio: 'inherit'
    });
    console.log('Construction du client terminée');
  } else {
    console.log('Le build existe déjà, utilisation du build existant');
  }
  
  console.log('Succès de la compilation du client React');
} catch (error) {
  console.error('Erreur lors de la compilation du client React:', error.message);
  process.exit(1);
}