// Fonction pour envoyer une requête GET à la route /test
function testAPIRequest() {
    fetch('http://localhost:5000/planning/test')
        .then(response => response.json())
        .then(data => {
            console.log('Response from /test:', data);
        })
        .catch(error => {
            console.error('Error fetching /test:', error);
        });
}

// Fonction pour envoyer une requête GET à la route /authorize
function authorize() {
    fetch('http://localhost:5000/planning/authorize')
        .then(response => response.text())
        .then(data => {
            console.log('Response from /authorize:', data);
            // Vous pouvez rediriger l'utilisateur vers l'URL d'autorisation ici si nécessaire
        })
        .catch(error => {
            console.error('Error fetching /authorize:', error);
        });
}

// Fonction pour envoyer une requête GET à la route /revoke
function revoke() {
    fetch('http://localhost:5000/planning/revoke')
        .then(response => response.text())
        .then(data => {
            console.log('Response from /revoke:', data);
        })
        .catch(error => {
            console.error('Error fetching /revoke:', error);
        });
}

// Fonction pour envoyer une requête GET à la route /clear
function clearCredentials() {
    fetch('http://localhost:5000/planning/clear')
        .then(response => response.text())
        .then(data => {
            console.log('Response from /clear:', data);
        })
        .catch(error => {
            console.error('Error fetching /clear:', error);
        });
}

// Appeler les différentes fonctions pour tester les routes
testAPIRequest();
authorize();
revoke();
clearCredentials();
