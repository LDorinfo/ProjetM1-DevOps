import {useState} from 'react';
import Login from '../connexion/Login.js';
import Signin from '../connexion/Signin.js';
import HomePage from './HomePage.js';
import ProfilePage from './ProfilePage.js';
import Search from '../search/Search.js';
import PageFilm from './PageFilm.js';
import Watchlist from './Watchlist.js';

function MainPage(props){
    const [page, setPage]= useState(["home_page", undefined]); 
    console.log(page)
    
    return (() => {
        if (page[0] === "login_page") {
          return <Login setPage={setPage} />;
        } else if (page[0] === "home_page") {
          return <HomePage setPage={setPage} />;
        } else if (page[0] === "profile_page") {
          return <ProfilePage setPage={setPage} user_id={page[1]} />;
        } else if (page[0] === "signin_page") {
          return <Signin setPage={setPage} />;
        }else if(page[0]=== "search_page") {
          return <Search setPage={setPage} datasearch={page[1]} />; 
        }else if(page[0]=== "film_page") {
          return <PageFilm setPage={setPage} dataFilm={page[1]} />; 
        }else if(page[0]=== "page_watchlist") {
          return <Watchlist setPage={setPage} data={page[1]} />; 
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