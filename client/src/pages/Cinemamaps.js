import React, { useState, useEffect } from 'react';
import NavigationBar from '../NavigationBar';

const Cinemamaps = () => {
  const [map, setMap] = useState(null);

  useEffect(() => {
    // Fonction pour initialiser la carte
    const initMap = () => {
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
        });
      } else {
        // Gestion du cas où la géolocalisation n'est pas supportée ou autorisée.
        console.error('La géolocalisation n\'est pas supportée ou autorisée.');
      }
    };

    // Charger l'API Google Maps
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyAQkQn5CZ3xbCiPq07KUBiOn0FOkW0DgsY&libraries=places&callback=initMap`;
    script.async = true;
    document.head.appendChild(script);

    // Nettoyer le script lors du démontage du composant
    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return (
    <div>
      <NavigationBar />
      <div id="map" style={{ height: '400px' }}></div>
    </div>
  );
};

export default Cinemamaps;
