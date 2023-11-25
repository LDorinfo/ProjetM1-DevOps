import React, { useState, useEffect } from 'react';
import './HomePage.css';
import NavigationBar from '../NavigationBar';
import ImageFilm from '../search/ImageFilm';

function HomePage(props) {
  const [popularMovies, setPopularMovies] = useState([]);
  const [popularTVShows, setPopularTVShows] = useState([]);
  const [currentSlideMovies, setCurrentSlideMovies] = useState(0);
  const [currentSlideTVShows, setCurrentSlideTVShows] = useState(0);


  useEffect(() => {
    const fetchPopularData = () => {
      // Fetch popular movies
      fetch('http://localhost:5000/api/trending-movies', {
        method: 'GET',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setPopularMovies(data || []);
        })
        .catch((error) => console.log(error));

      // Fetch popular TV shows
      fetch('http://localhost:5000/api/trending-tv', {
        method: 'GET',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setPopularTVShows(data || []);
        })
        .catch((error) => console.log(error));
    };

    fetchPopularData();
  }, [setPopularMovies,setPopularTVShows]);

  const nextSlideMovies = () => {
    setCurrentSlideMovies((prevSlide) => (prevSlide + 1) % Math.ceil(popularMovies.length / 7));
  };

  const prevSlideMovies = () => {
    setCurrentSlideMovies((prevSlide) => (prevSlide - 1 + Math.ceil(popularMovies.length / 7)) % Math.ceil(popularMovies.length / 7));
  };

  const nextSlideTVShows = () => {
    setCurrentSlideTVShows((prevSlide) => (prevSlide + 1) % Math.ceil(popularTVShows.length / 7));
  };

  const prevSlideTVShows = () => {
    setCurrentSlideTVShows((prevSlide) => (prevSlide - 1 + Math.ceil(popularTVShows.length / 7)) % Math.ceil(popularTVShows.length / 7));
  };

  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}/>
      </header>
      <div className="HomePage">
        <div className="text-container">
          <p>Dive into CineVerse: films, séries, animes. Votre univers de divertissement</p>
          <img src="/wordpress-cs-format-image-20.webp" alt="Description de l'image" />
        </div>
        <section className="trending-movies">
          <h2>Films tendances <img src="https://img.icons8.com/fluency/48/star--v1.png" alt="star--v1" /></h2>
          <div className="movies-list">
            {popularMovies.length > 0 && (
              <div className="carousel-container">
                <button className="carousel-button" onClick={prevSlideMovies}>
                  &lt;
                </button>
                <div className="carousel">
                  {popularMovies.slice(currentSlideMovies * 7, (currentSlideMovies + 1) * 7).map((movie) => (
                    <div key={movie.id} className="movie-poster">
                      <ImageFilm dataFilm={movie} setPage={props.setPage}/>
                    </div>
                  ))}
                </div>
                <button className="carousel-button" onClick={nextSlideMovies}>
                  &gt;
                </button>
              </div>
            )}
          </div>
        </section>

        <section className="trending-tv-shows">
          <h2>Séries tendances <img src="https://img.icons8.com/fluency/48/star--v1.png" alt="star--v1" /></h2>
          <div className="tv-shows-list">
            {popularTVShows.length > 0 && (
              <div className="carousel-container">
                <button className="carousel-button" onClick={prevSlideTVShows}>
                  &lt;
                </button>
                <div className="carousel">
                  {popularTVShows.slice(currentSlideTVShows * 7, (currentSlideTVShows + 1) * 7).map((tvShow) => (
                    <div key={tvShow.id} className="tv-show-poster">
                      <ImageFilm dataFilm={tvShow} setPage={props.setPage}/>
                    </div>
                  ))}
                </div>
                <button className="carousel-button" onClick={nextSlideTVShows}>
                  &gt;
                </button>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

export default HomePage;