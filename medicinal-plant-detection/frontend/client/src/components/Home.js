import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="hero-section">
        <div className="content-overlay">
          <h1 className="app-title">VedaRoot-Medicinal Plant Detection</h1>
          <p className="app-description">
            VedaRoot is an AI-powered web app designed to identify medicinal plants from images 
            and provide insights into their Ayurvedic uses for treating various diseases.
          </p>
          <button 
            className="try-button"
            onClick={() => navigate('/upload')}
          >
            Try It Now
          </button>
        </div>
      </div>
    </div>
  );
}


export default Home;