import React,{useRef, useState} from 'react'; 

function SelecteurDate(props){
    const dateInputRef = useRef(null); 

    return (
        <div>
        <input type="datetime-local" onChange={props.handleChange} ref={dateInputRef} />
        <p>Selected Date: {props.date}</p>
        </div>
    )
}; 

export default SelecteurDate; 