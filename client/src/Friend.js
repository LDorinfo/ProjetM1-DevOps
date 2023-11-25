import { Button } from "react-bootstrap";
import { useState } from "react";

function Friend(props){
    // liste des utilisateurs suivis 
    // trouver un moyen pour visualiser la page de ses amis

    const [friendComponents, setFriendComponents] = useState([]);
	const [loading, setLoading] = useState(true);

    const handleClickOnFriend = (evt)=>{
        
    }

	async function fetchInfos(userId) {
		try {
		  const response = await fetch(`http://localhost:5000/api/userinfo?user_id=${userId}`, {
			method: 'GET',
			credentials: 'include',
		  });
		  const data = await response.json();
		  if (data.status === 200) {
			return data ;
		  }
		} catch (error) {
		  console.log(error);
		}
	  }

	useEffect(() => {
		async function createFriendComponent(friendId, setPage) {
			const friendInfos = await fetchInfos(friendId);
			return (
                <li >
			        <Button className="link-button" onClick={handleClickOnFriend}>{friendInfos.username}</Button>
		        </li>
            );
		}

        // il faut récupèrer la liste des amis
		async function fetchFriendComponents() {
		const promises = [];
		for (const friendId of props.friends){
			promises.push(createFriendComponent(friendId, props.setPage));
		}
		//   const promises = props.friends.map((friendId) => createFriendComponent(friendId, props.setPage) );
		  const components = await Promise.all(promises);
		  setFriendComponents(components);
		}
	  
		fetchFriendComponents();
		setLoading(false);
	  }, [props.friends, props.setPage]);

	return (
		<ul>
			{loading === true ? <div>Chargement...</div> : friendComponents}
		</ul>
	);

}

export default Friend; 