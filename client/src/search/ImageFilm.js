
function ImageFilm(props){
    
    const handleClickImageFilm = (i) =>{
        console.log(i.id)
        props.setPage(["film_page", i])
      }
    return (<img
        className="movieposter"
        src={`https://image.tmdb.org/t/p/w500${props.dataFilm.poster_path}`}
        alt={props.dataFilm.title}
        onClick= {() => handleClickImageFilm(props.dataFilm)}
    />);
}

export default ImageFilm; 