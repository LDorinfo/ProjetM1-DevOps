// possibilité de regrouper les test grace à la fonction describe
import renderer from 'react-test-renderer';
import Signin from './Signin.js';

describe("TestSignin", ()=>{
    // fonction contenant les tests
    test("Premier test", ()=>{
        //1) Génération 
        const component = renderer.create(<Signin setPage={["signin_page", undefined]}/>,); 
        // fonctionnalité de snapshot de jest pour capturer le rendu composant dans un fichier
        let tree = component.toJSON(); 
        expect(tree).toMatchSnapshot(); 
        // au lieu d'avoir un rendu graphique, on utilise un moteur de rendu de test pour générer rapidement une valeur sérialisable pour notre arborescence React. 
        // le callback : fonction de rappel est une fonction passée dans une autre fonction en tant qu'argument qui est ensuite invoquée à l'intérieur de la fonction externe pour accomplir une routine. 
        
        //2) Actions 


        //3) Assertions
        //pour faire des assertions avec Jest il faut utiliser la fonction except()
    }); 



})
// pour exécuter Jest directelent depuis le CLI : 
// jest Test --notify --config=config.json
