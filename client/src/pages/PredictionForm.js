import React, { useState } from "react";
import axios from "axios";
import NavigationBar from '../NavigationBar';
import "./Prediction.css"; 

function PredictionForm(props) {
  const [title, setTitle] = useState("");
  const [budget, setBudget] = useState("");
  const [runtime, setRuntime] = useState("");
  const [releaseDate, setReleaseDate] = useState("");
  const [genres, setGenres] = useState([]);
  const [language, setLanguage] = useState("en");
  const [productionCompany, setProductionCompany] = useState("");
  const [successProbability, setSuccessProbability] = useState(null);
  const [estimatedRevenue, setEstimatedRevenue] = useState(null);
  const [loading, setLoading] = useState(false);

  const allGenres = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
  ];

  const handleGenreChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setGenres([...genres, value]);
    } else {
      setGenres(genres.filter((genre) => genre !== value));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/predict", {
        title: title,
        budget: Number(budget),
        genres: genres.join("-"),  
        original_language: language,
        production_companies: productionCompany,
        release_date: releaseDate,
        runtime: Number(runtime),
      });

      setSuccessProbability(response.data.success_probability);
      setEstimatedRevenue(response.data.estimated_revenue);
    } catch (error) {
      console.error("Erreur lors de la prédiction", error);
      setSuccessProbability("Erreur lors de la prédiction.");
      setEstimatedRevenue(null);
    }
    setLoading(false);
  };

  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage} />
      </header>
      <div className="prediction-container">
        <h2>🔮 Prédiction du Succès d'un Film 🎬</h2>
        
        <form onSubmit={handleSubmit} className="prediction-form">
          <fieldset>
            <legend>📜 Infos Générales</legend>
            <input type="text" placeholder="Titre du film" value={title} onChange={(e) => setTitle(e.target.value)} required />
            <input type="text" placeholder="Société de production" value={productionCompany} onChange={(e) => setProductionCompany(e.target.value)} required />
            <input type="text" placeholder="Date de sortie (YYYY-MM-DD)" value={releaseDate} onChange={(e) => setReleaseDate(e.target.value)} required />
          </fieldset>

          <fieldset>
            <legend>💰 Budget & Durée</legend>
            <input type="number" placeholder="Budget ($)" value={budget} onChange={(e) => setBudget(e.target.value)} required />
            <input type="number" placeholder="Durée (min)" value={runtime} onChange={(e) => setRuntime(e.target.value)} required />
          </fieldset>

          <fieldset>
            <legend>🎭 Genres</legend>
            <div className="genres-container">
              {allGenres.map((genre) => (
                <label key={genre} className="genre-label">
                  <input type="checkbox" value={genre} onChange={handleGenreChange} /> {genre}
                </label>
              ))}
            </div>
          </fieldset>

          <fieldset>
            <legend>🗣️ Langue</legend>
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              <option value="en">Anglais</option>
              <option value="fr">Français</option>
              <option value="es">Espagnol</option>
              <option value="de">Allemand</option>
              <option value="it">Italien</option>
            </select>
          </fieldset>

          <button type="submit" disabled={loading}>
            {loading ? "🔄 Prédiction en cours..." : "📊 Prédire"}
          </button>
        </form>

        {successProbability !== null && (
          <div className="result">
            <h3>🎬 Film : <strong>{title}</strong></h3>
            <p className={`probability ${successProbability > 60 ? "high" : successProbability > 40 ? "medium" : "low"}`}>
              🔥 Probabilité de succès : <strong>{successProbability}%</strong>
            </p>
            {estimatedRevenue !== null && (
              <p className="revenue">
                💰 Revenu estimé : <strong>{(estimatedRevenue / 1_000_000).toFixed(1)}M $</strong>
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default PredictionForm;
