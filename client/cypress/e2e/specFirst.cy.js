// cypress/integration/search.spec.js

describe('Search functionality', () => {
  it('performs a search and displays results', () => {
    // Visitez votre application
    cy.visit('http://localhost:3000');

    // Effectuez une recherche
    cy.get('input[type="text"]').type('Avengers').should('have.value', 'Avengers');
    cy.get('.submit_search_bar').click();

    // Vérifiez si les résultats de la recherche sont affichés
    cy.get('.results', { timeout: 10000 }).should('exist');
    // Vérifier si le premier élément .resultsearch existe
    cy.get('.resultsearch').eq(0).should('exist');

    cy.get('.resultsearch', { timeout: 10000 })
    .eq(5)
    .find('.movieposter') // Remplace .title par le sélecteur de l'élément contenant l'image du film
    .should('be.visible') // Attend que l'élément soit visible
    .click();
    // Vérifier si "Avengers" est présent dans le premier résultat de la recherche
    cy.get('.film-details', { timeout: 10000 })
    .should('not.be.empty')
    .and('contain', 'Avengers');
  });
});
