import { useState } from "react";
import { toast } from 'react-toastify';
import "./Login.css";
import NavigationBar from "./NavigationBar";

function Login(props) {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");

  const getLogin = (evt) => {
    setLogin(evt.target.value);
  };

  const getPassword = (evt) => {
    setPassword(evt.target.value);
  };

  const handleClickSignin = (evt) => {
    evt.preventDefault();
    props.setPage(["signin_page", undefined]);
  };

  const handleClick = (evt) => {
    evt.preventDefault();
    let newerrorMessages = [];

    fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ username: login, password })
    })
      .then(response => response.json())
      .then(data => {
        console.log('User connected successfully:', data);
        toast("Connexion!");
        props.setPage(["home_page", data.id]);
      })
      .catch(error => {
        console.error('Error during connexion:', error);
        newerrorMessages.push("Une erreur s'est produite lors de la connexion. Veuillez réessayer.");
      });
  };

  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}></NavigationBar>
      </header>
      <main>
        <div className="wrapper">
          <form action="">
            <h1>Se connecter</h1>
            <div className="input-box">
              <input type="text" placeholder="Username" required onChange={getLogin} />
              <i className='bx bxs-user'></i>
            </div>
            <div className="input-box">
              <input type="password" placeholder="Mot de passe" required onChange={getPassword} />
              <i className='bx bxs-lock-alt' ></i>
            </div>

            <div className="remember-forgot">
              <a href="#">Mot de passe oublié ?</a>
            </div>
            <button type="submit" onClick={handleClick} className="button_log" variant="primary">Se connecter</button>

            <div className="register-link">
              <p>Pas de compte ? <a href="#" onClick={handleClickSignin}>S'inscrire</a></p>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}

export default Login;
