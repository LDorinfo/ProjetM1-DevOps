import {useEffect,useState} from 'react';


function MainPage(props){
    const estconnecte = useState("false"); 
    const [page, setPage]= useState(["home_page", undefined]); 
    
    
    return (
        (()=>{
            if(page[0]==="login_page"){
                return (<Login setPage={setPage}/>)
            }
            else if (page[0]=== "home_page"){
                return (<HomePage setPage={setPage} />)
            }
            else if (page[0]=="profile_page"){
                return (
                    <ProfilePage setPage={setPage} user_id={page[1]}/>
                )
            }
        })
    )
}