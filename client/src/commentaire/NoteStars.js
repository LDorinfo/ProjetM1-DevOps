import './NoteStars.css'; 
function NoteStars(props){
    const MAX_STARS = 5; // je veux une note sur 5 étoiles 

    const handleStarClick = (rating) => {
        // dès que je clique sur une étoile je mets à jour la note dans le fronte 
        // cette note sera envoyé dans le back une fois le bouton envoyé validé. 
        props.setNoteUser(rating);
    };
    return (
        <div className="star-rating">
        {[...Array(MAX_STARS)].map((_, index) => (
            <span key={index} 
            className={props.isClickable ? (index + 1 <= props.noteUser ? "star-filled" : "star") : (index < props.noteUser ? "star-filled" : "star")}
            onClick={() => props.isClickable && handleStarClick(index + 1)}
            >
            ★
            </span>
        ))}
        </div>
    );
}

export default NoteStars; 