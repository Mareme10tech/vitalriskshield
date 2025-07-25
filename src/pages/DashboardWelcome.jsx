// src/components/DashboardWelcome.js
import React from 'react';
import '../styles/DashboardWelcome.css';
import vitalRiskShieldLogo from './vitalriskshield-logo.png';

function DashboardWelcome() {
  return (
    <div className="dashboard-welcome">
      <img src={vitalRiskShieldLogo} alt="VitalRiskShield Logo" className="welcome-logo" />
      <h1>Welcome to VitalRiskShield</h1>
      <div className="welcome-message">
        <p>
          VitalRiskShield is your AI-powered health risk forecasting platform. 
          We analyze your health data to identify potential risks for chronic conditions 
          like diabetes, cardiovascular disease, and cancer — helping you take 
          proactive steps toward better health.
        </p>
        <p>
          Get personalized recommendations, track your progress, and earn rewards 
          for healthy behaviors — all in one place.
        </p>
      </div>
    </div>
  );
}

export default DashboardWelcome;