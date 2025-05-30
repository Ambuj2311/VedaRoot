import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Results.css';

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const { prediction } = location.state || {};

  if (!prediction) {
    return (
      <div className="results-container">
        <h2>No prediction data found</h2>
        <button onClick={() => navigate('/')}>Back to Home</button>
      </div>
    );
  }

  // Default details in case plant info isn't found
  const plantDetails = prediction.details || {
    scientific_name: "N/A",
    common_uses: "No information available",
    medicinal_uses: "No information available"
  };

  return (
    <div className="results-container">
      
      <div className="result-card">
        {prediction.image && (
          <div className="plant-image-container">
            <img 
              src={prediction.image} 
              alt="Uploaded Plant" 
              className="plant-image"
            />
          </div>
        )}

        <div className="plant-details">
          <h3 className="plant-name">Plant Name: {prediction.class}</h3>

          <div className="detail-section">
            <h4>Scientific Name</h4>
            <p>{plantDetails.scientific_name}</p>
          </div>

          <div className="detail-section">
            <h4>Common Uses</h4>
            <p>{plantDetails.common_uses}</p>
          </div>

          <div className="detail-section">
            <h4>Medicinal Uses</h4>
            <p>{plantDetails.medicinal_uses}</p>
          </div>
        </div>
      </div>

      <div className="action-buttons">
        <button 
          className="try-again-button"
          onClick={() => navigate('/upload')}
        >
          Try Another Image
        </button>
        <button 
          className="home-button"
          onClick={() => navigate('/')}
        >
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default Results;