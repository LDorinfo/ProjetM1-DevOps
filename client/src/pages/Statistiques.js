import { useState, useEffect } from "react";

function Statistiques(props){
    const [genreStats, setGenreStats] = useState({});

    useEffect(() => {
        const fetchGenreStats = () => {
            // Fetch genre statistics
            fetch("http://localhost:5000/statistic/genre-stats", {
                method: 'GET',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' }
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setGenreStats(data);
            })
            .catch((error) => console.log(error));
        };
        fetchGenreStats(); 
    }, []);

    return (
        <div>
            <h2>Statistiques sur les genres de films préférés</h2>
            <div className="bar-chart">
                {Object.entries(genreStats).map(([genre, count]) => (
                    <div key={genre} className="bar" style={{ height: `${count * 10}px` }}>
                        <span>{genre}: {count}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Statistiques;
