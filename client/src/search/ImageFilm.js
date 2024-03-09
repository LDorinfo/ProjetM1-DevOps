
function ImageFilm(props){
    const handleClickImageFilm = (i) =>{
        if(i.media_type!="tv"){
            fetch(`http://localhost:5000/movie/details?query=${i.id}`, {
                method: 'GET',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
            })
            .then((response) => response.json())
            .then((data) => {
                props.setPage(["film_page", data])
            })
            .catch((error) => console.log(error));
        }else{
            fetch(`http://localhost:5000/tv/details?query=${i.id}`, {
                method: 'GET',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
            })
            .then((response) => response.json())
            .then((data) => {
                props.setPage(["film_page", data])
            })
            .catch((error) => console.log(error));
        }
    }
    return (<img
        className="movieposter"
        src={`https://image.tmdb.org/t/p/w500${props.dataFilm.poster_path}`}
        alt={props.dataFilm.title}
        onClick= {() => handleClickImageFilm(props.dataFilm)}
    />);
}

export default ImageFilm; 