import React, { useState, useEffect } from 'react';
import NavigationBar from '../NavigationBar';
import { propTypes } from 'react-bootstrap/esm/Image';

function Cinemamaps(props) {
  const [map, setMap] = useState(null);

  useEffect(() => {
    // Define initMap in the global scope
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

          // You can add markers or other features here
          setMap(mapInstance);
        });
      } else {
        // Handle case where geolocation is not supported or allowed
        console.error('Geolocation is not supported or allowed.');
      }
    };

    // Load Google Maps API asynchronously
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyAQkQn5CZ3xbCiPq07KUBiOn0FOkW0DgsY&libraries=places&callback=initMap`;
    script.async = true;
    document.head.appendChild(script);

    // Clean up the script on component unmount
    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return (
    <div>
      <NavigationBar setPage={props.setPage}/>
      <div id="map" style={{ height: '400px' }}></div>
    </div>
  );
};

export default Cinemamaps;
