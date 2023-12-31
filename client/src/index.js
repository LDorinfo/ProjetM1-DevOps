import React from 'react';
import ReactDOM from 'react-dom/client';
//import './index.css';
import MainPage from './pages/MainPage.js';
import reportWebVitals from './reportWebVitals';
import { AuthProvider } from './AuthenticateContext.js';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
    <MainPage />
    <ToastContainer/>
    </AuthProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
