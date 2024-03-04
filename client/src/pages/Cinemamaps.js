import React, { useState, useEffect } from 'react';
import NavigationBar from '../NavigationBar';

const Cinemamaps = () => {
  const [map, setMap] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fonction pour initialiser la carte
    window.initMap = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
          const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };

          const mapInstance = new window.google.maps.Map(document.getElementById('map'), {
            center: userLocation,
            zoom: 15
          });

          // Vous pouvez ajouter des marqueurs ou d'autres fonctionnalités ici
          setMap(mapInstance);

          // Recherche des cinémas à proximité
          const request = {
            location: userLocation,
            radius: 5000, // Rayon de recherche en mètres (ajustez selon vos besoins)
            types: ['movie_theater'] // Type de lieu pour les cinémas
          };

          const service = new window.google.maps.places.PlacesService(mapInstance);
          service.nearbySearch(request, (results, status) => {
            if (status === window.google.maps.places.PlacesServiceStatus.OK) {
              // Création des marqueurs pour chaque résultat de cinéma
              for (let i = 0; i < results.length; i++) {
                createMarker(results[i]);
              }
            } else {
              setError('Erreur lors de la recherche de cinémas à proximité.');
            }
          });

          // Fonction pour créer un marqueur
          const createMarker = place => {
            const marker = new window.google.maps.Marker({
              map: mapInstance,
              position: place.geometry.location,
              title: place.name
            });

            // Vous pouvez personnaliser les marqueurs ou ajouter des informations supplémentaires ici
          };
        });
      } else {
        // Gestion du cas où la géolocalisation n'est pas supportée ou autorisée.
        console.error('La géolocalisation n\'est pas supportée ou autorisée.');
        setError('La géolocalisation n\'est pas supportée ou autorisée.');
      }
    };

    // Charger l'API Google Maps
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyBVHzvmWVkjyU4aexEM0krlXnxwL8nhuAA&libraries=places&callback=initMap&loading=async`;
    script.async = true;

    // Ajouter une vérification pour éviter de charger plusieurs fois l'API
    if (!window.google) {
      script.onerror = () => {
        setError('Erreur lors du chargement de l\'API Google Maps.');
      };

      document.head.appendChild(script);
    }

    // Nettoyer le script lors du démontage du composant
    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return (
    <div>
      <header>
        <NavigationBar />
      </header>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <h2>Cinéma à proximité</h2>
      {error ? (
        <div>Erreur : {error}</div>
      ) : (
      <div id="map" style={{ height: '600px', width: '50%' }}></div>
    )}
  </div>
    </div>
  );
};

export default Cinemamaps;