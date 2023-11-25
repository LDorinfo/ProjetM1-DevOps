import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

// permet de créer un context d'authentification 
// évite de propager manuellement les informations de l'utilisateur. 

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchAuth = async () => {
      try {
        // permet de vérifier que l'utilisateur est connecté, ne prend pas de paramètre 
        // le serveur renvoie les informations de l'utilisateur : user_id
        const response = await fetch('http://localhost:5000/@me', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData.id);
          console.log(userData.id);
        }
      } catch (error) {
        console.error('Erreur lors de la vérification de l\'authentification:', error);
      }
    };

    fetchAuth();
  }, [setUser]);

  return (
    <AuthContext.Provider value={ {user}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);


