import React, { useState, useEffect } from 'react';
import NavigationBar from '../NavigationBar';
import "./Analytics.css"; 
import zoomPlugin from 'chartjs-plugin-zoom';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Tooltip,
    Legend,
  } from "chart.js";
import { Pie, Line, Bar, Scatter } from "react-chartjs-2";
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Tooltip,
    Legend
  );


ChartJS.register(zoomPlugin);

const zoomOptions = {
    plugins: {
      zoom: {
        zoom: {
          wheel: {
            enabled: true, // Activer le zoom avec la molette
          },
          pinch: {
            enabled: true, // Activer le zoom tactile
          },
          mode: "xy", // Zoom sur les axes X et Y
        },
        pan: {
          enabled: true, // Activer le pan
          mode: "xy", // Déplacement sur les axes X et Y
        },
      },
    },
  };

  const tooltipOptions = {
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context) {
            return `Film: ${context.label}, Rentabilité: ${context.raw}`;
          },
        },
      },
    },
  };
  

  function Analytics(props) {
    const [genreData, setGenreData] = useState({});
    const [popularityTimeData, setPopularityTimeData] = useState({});
    const [languageData, setLanguageData] = useState({});
    const [budgetRevenueData, setBudgetRevenueData] = useState({});
    const [averageBudgetData, setAverageBudgetData] = useState({});
    const [popularMoviesData, setPopularMoviesData] = useState({});
    const [popularityRevenueData, setPopularityRevenueData] = useState({});
    const [monthlyReleaseData, setMonthlyReleaseData] = useState({});
    const [productionCompaniesData, setProductionCompaniesData] = useState({});
    const [topRatedMoviesData, setTopRatedMoviesData] = useState({});
  
    useEffect(() => {
      // Récupérer les données des genres
      fetch("http://localhost:5000/api/genre-distribution")
        .then((res) => res.json())
        .then((data) => {
          setGenreData({
            labels: data.labels,
            datasets: [
              {
                data: data.data,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
            "#9966FF", "#FF9F40", "#E57373", "#81C784", 
            "#FFD700", "#8E24AA", "#00ACC1", "#D81B60",
            "#64B5F6", "#4DD0E1", "#AED581", "#FFB74D"],
              },
            ],
          });
        });
  
      // Récupérer les données de popularité au fil du temps
      fetch("http://localhost:5000/api/popularity-over-time")
        .then((res) => res.json())
        .then((data) => {
            setPopularityTimeData({
            labels: data.labels,
            datasets: [
              {
                label: "Popularité moyenne",
                data: data.data,
                borderColor: "rgba(75,192,192,1)",
                fill: false,
              },
            ],
          });
        });
  
      // Récupérer les données de répartition des langues
      fetch("http://localhost:5000/api/language-distribution")
        .then((res) => res.json())
        .then((data) => {
          setLanguageData({
            labels: data.labels,
            datasets: [
              {
                data: data.data,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
            "#9966FF", "#FF9F40", "#E57373", "#81C784", 
            "#FFD700", "#8E24AA", "#00ACC1", "#D81B60",
            "#64B5F6", "#4DD0E1", "#AED581", "#FFB74D"],
              },
            ],
          });
        });

      // Récupérer les données de Budget Moyen par Genre
    fetch("http://localhost:5000/api/average-budget-by-genre")
    .then((res) => res.json())
    .then((data) => {
        setAverageBudgetData({
        labels: data.labels,
        datasets: [
            {
            label: "Budget Moyen ($)",
            data: data.data,
            backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
            "#9966FF", "#FF9F40", "#E57373", "#81C784", 
            "#FFD700", "#8E24AA", "#00ACC1", "#D81B60",
            "#64B5F6", "#4DD0E1", "#AED581", "#FFB74D"],
            },
        ],
        });
    });
  
      // Récupérer les données Budget vs Revenus
      fetch("http://localhost:5000/api/budget-vs-revenue")
        .then((res) => res.json())
        .then((data) => {
          setBudgetRevenueData({
            datasets: [
              {
                label: "Budget vs Revenus",
                data: data.budget.map((value, index) => ({
                  x: value,
                  y: data.revenue[index],
                })),
                backgroundColor: "rgba(75,192,192,1)",
              },
            ],
          });
        });

        // Films les Plus Populaires
        fetch("http://localhost:5000/api/top-popular-movies")
            .then((res) => res.json())
            .then((data) => {
            setPopularMoviesData({
                labels: data.titles,
                datasets: [
                {
                    label: "Popularité",
                    data: data.popularity,
                    backgroundColor: "#FF6384",
                },
                ],
            });
            });
        
        // Popularité vs Revenus (Nuage de Points Interactif)
            fetch("http://localhost:5000/api/popularity-vs-revenue")
              .then((res) => res.json())
              .then((data) => {
                setPopularityRevenueData({
                  datasets: [
                    {
                      label: "Popularité vs Revenus",
                      data: data.popularity.map((pop, index) => ({
                        x: pop,
                        y: data.revenue[index],
                      })),
                      backgroundColor: "rgba(75,192,192,1)",
                    },
                  ],
                });
              });

        // Nombre de Films Sortis par Mois (Interactif)
        fetch("http://localhost:5000/api/release-month-distribution")
            .then((res) => res.json())
            .then((data) => {
            setMonthlyReleaseData({
                labels: data.labels,
                datasets: [
                {
                    label: "Nombre de Films",
                    data: data.data,
                    backgroundColor: "#FFCE56",
                },
                ],
            });
            });
        
        // Films par Compagnies de Production
        fetch("http://localhost:5000/api/top-production-companies")
        .then((res) => res.json())
        .then((data) => {
            setProductionCompaniesData({
            labels: data.labels,
            datasets: [
                {
                label: "Films par Compagnies",
                data: data.data,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
            "#9966FF", "#FF9F40", "#E57373", "#81C784", 
            "#FFD700", "#8E24AA", "#00ACC1", "#D81B60",
            "#64B5F6", "#4DD0E1", "#AED581", "#FFB74D"],
                },
            ],
            });
        });

        fetch("http://localhost:5000/api/top-rated-movies")
            .then((res) => res.json())
            .then((data) => {
            setTopRatedMoviesData({
                labels: data.titles,
                datasets: [
                {
                    label: "Note Moyenne",
                    data: data.ratings,
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
            "#9966FF", "#FF9F40", "#E57373", "#81C784", 
            "#FFD700", "#8E24AA", "#00ACC1", "#D81B60",
            "#64B5F6", "#4DD0E1", "#AED581", "#FFB74D"],
                },
                ],
            });
            });
        
    }, []);
  
    return (
      <div>
        <header>
          <NavigationBar setPage={props.setPage} />
        </header>
        <div className="analytics-description">
        <h2>À propos des données</h2>
        <p>
            Les données utilisées dans ce tableau de bord proviennent d'une base de données contenant des informations sur plus de <strong>700 000 films</strong>.
            Pour optimiser les performances, nous avons conservé uniquement les <strong>50 000 premières lignes</strong> les plus pertinentes.
            Ces données incluent des informations détaillées telles que les genres, la popularité, le budget, les revenus, les notes, et les compagnies de production associées à chaque film.
        </p>
        </div>
        <h1 className="dashboard-title">Dashboard</h1>
        <div className="analytics-dashboard">
        <div className="analytics-card">
          <h2>Répartition des Genres</h2>
          {genreData.labels ? (
            <Pie data={genreData} />
          ) : (
            <p className="loading-text">Chargement...</p>
          )}
          <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les genres dominants, comme le drame et la comédie, reflètent les préférences globales des spectateurs et les investissements dans ces catégories.</span>
            </div>
        </div>

          <div className="analytics-card">
            <h2>Répartition des Langues</h2>
            {languageData.labels ? (
              <Bar data={languageData} />
            ) : (
              <p className="loading-text">Chargement...</p>
            )}
            <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">La prédominance de l'anglais reflète la domination de l'industrie cinématographique hollywoodienne.</span>
            </div>
          </div>
  
          <div className="analytics-card">
            <h2>Popularité au Fil du Temps</h2>
            {popularityTimeData.labels ? (
              <Line data={popularityTimeData} />
            ) : (
              <p className="loading-text">Chargement...</p>
            )}
            <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les pics de popularité correspondent souvent à des périodes de sorties majeures, comme les blockbusters ou des franchises célèbres.</span>
            </div>
          </div>

          <div className="analytics-card">
                <h2>Nombre de Films Sortis par Mois</h2>
                {monthlyReleaseData.labels ? (
                    <Bar data={monthlyReleaseData} options={zoomOptions} />
                ) : (
                    <p>Chargement...</p>
                )}
                <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les pics en août et décembre s'expliquent par les périodes de vacances, où les spectateurs sont plus disponibles.</span>
            </div>
          </div>

          <div className="analytics-card">
                <h2>Films par Compagnies de Production</h2>
                {productionCompaniesData.labels ? (
                    <Bar data={productionCompaniesData} />
                ) : (
                    <p>Chargement...</p>
                )}
                <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les grandes compagnies comme Paramount dominent l'industrie grâce à leurs capacités de production et de distribution.</span>
            </div>
          </div>


          <div className="analytics-card">
            <h2>Budget Moyen par Genre</h2>
            {averageBudgetData.labels ? (
                <Bar data={averageBudgetData} />
            ) : (
                <p className="loading-text">Chargement...</p>
            )}
            <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les genres comme la science-fiction et l'action ont des budgets moyens élevés en raison des besoins en effets spéciaux et en décors coûteux.</span>
            </div>
            </div>
  
           <div className="analytics-card wide-card">
            <h2>Budget vs Revenus</h2>
            {budgetRevenueData.datasets ? (
              <Scatter data={budgetRevenueData} />
            ) : (
              <p className="loading-text">Chargement...</p>
            )}
            <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Un budget élevé ne garantit pas toujours un succès, mais il peut augmenter les chances d'atteindre un public plus large grâce à des effets spéciaux et à la publicité.</span>
            </div>
          </div>

          <div className="analytics-card">
            <h2>Films les Plus Populaires</h2>
            {popularMoviesData.labels ? (
                <Bar data={popularMoviesData} />
            ) : (
                <p>Chargement...</p>
            )}
            <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les films les plus populaires sont souvent ceux qui appartiennent à des franchises établies ou qui ont bénéficié d'un large marketing.</span>
            </div>
            </div>

            <div className="analytics-card">
                <h2>Films les Mieux Notés</h2>
                {topRatedMoviesData.labels ? (
                    <Bar data={topRatedMoviesData} />
                ) : (
                    <p>Chargement...</p>
                )}
                <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Les films les mieux notés combinent souvent un scénario captivant, un bon jeu d'acteurs et une réalisation de qualité.</span>
            </div>
                </div>

            <div className="analytics-card wide-card">
            <h2>Popularité vs Revenus</h2>
            {popularityRevenueData.datasets ? (
                <Scatter data={popularityRevenueData} options={zoomOptions} />
            ) : (
                <p>Chargement...</p>
            )}
            <div className="custom-tooltip">
            <div className="tooltip-icon">
            <i className="question-icon">?</i>
            </div>
            <span className="custom-tooltip-text">Certains films très populaires peuvent avoir un faible revenu net si leurs budgets et leurs coûts marketing sont élevés.</span>
            </div>
            </div>
            
        </div>
      </div>
    );
  }
  
  export default Analytics;
  