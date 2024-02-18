import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from 'react-toastify';
import "./Login.css";
import NavigationBar from "../NavigationBar";

function Login() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const history = useNavigate();

  const getLogin = (evt) => {
    setLogin(evt.target.value);
  };

  const getPassword = (evt) => {
    setPassword(evt.target.value);
  };

  const getemail = (evt) => {
    setEmail(evt.target.value);
  };

  const handleClickSignin = (evt) => {
    evt.preventDefault();
    history("/signin");
  };

  const handleForgotPassword = (evt) => {
    evt.preventDefault();
    if (email.length === 0) {
      toast("Merci de renseigner votre mail");
    } else {
      // Envoie une demande de réinitialisation de mot de passe au backend
      fetch('http://localhost:5000/forgot-password', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email })
      })
        .then(response => response.json())
        .then(data => {
          console.log('Password reset email sent:', data);
          toast("Un e-mail de réinitialisation de mot de passe a été envoyé.");
        })
        .catch(error => {
          console.error('Error sending password reset email:', error);
          toast("Une erreur s'est produite. Veuillez réessayer.");
        });
    }
  };

  const handleClick = (evt) => {
    evt.preventDefault();
    let newerrorMessages = [];

    fetch('http://localhost:5000/users/login', {
      method: 'PUT',
      credentials: 'include',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: login, password })
    })
      .then(response => response.json())
      .then(data => {
        console.log('User connected successfully:', data);
        toast("Connexion!");
        history("/",{ replace: true }); // Redirige vers la page d'accueil après la connexion
      })
      .catch(error => {
        console.error('Error during connexion:', error);
        newerrorMessages.push("Une erreur s'est produite lors de la connexion. Veuillez réessayer.");
      });
  };

  return (
    <div>
      <header>
        <NavigationBar ></NavigationBar>
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
              <a href="#" onClick={handleForgotPassword}>Mot de passe oublié ?</a>
            </div>
            <div className="input-box">
              <input type="email" placeholder="email" required onChange={getemail} />
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
