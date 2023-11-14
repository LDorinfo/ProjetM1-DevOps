import {useState} from 'react';
import Login from './Login.js';
import Signin from './Signin.js';
import HomePage from './HomePage.js';
import ProfilePage from './ProfilePage.js';

function MainPage(props){
    const [page, setPage]= useState(["login_page", undefined]); 
    
    
    return (() => {
        if (page[0] === "login_page") {
          return <Login setPage={setPage} />;
        } else if (page[0] === "home_page") {
          return <HomePage setPage={setPage} user_id={page[1]} />;
        } else if (page[0] === "profile_page") {
          return <ProfilePage setPage={setPage} user_id={page[1]} />;
        } else if (page[0] === "signin_page") {
          return <Signin setPage={setPage} />;
        }
      })();
}
    

export default MainPage; 

/*(()=>{
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
            else if(page[0]==="signin_page"){
                return <Signin setPage={setPage}/>
            }
        })
*/