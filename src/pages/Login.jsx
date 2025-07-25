import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Auth.css';
import vitalRiskShieldLogo from '../assets/vitalriskshield-logo.png';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }
    onLogin();
  };

  return (
    <div className="login-container">
      {/* Welcome Section (Left Side) */}
      <div className="welcome-section">
        <img src={vitalRiskShieldLogo} alt="VitalRiskShield Logo" className="welcome-logo" />
        <h1>Welcome to VitalRiskShield</h1>
        <div className="welcome-message">
          <p>
            Your AI-powered health risk forecasting platform. We analyze your health data to identify 
            potential risks for chronic conditions like diabetes, cardiovascular disease, and cancer.
          </p>
          <p>
            Get personalized recommendations and track your progress toward better health.
          </p>
        </div>
      </div>

      {/* Login Form Section (Right Side) */}
      <div className="auth-card">
        <h2>Login to Your Account</h2>
        {error && <div className="auth-error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" className="auth-button">Login</button>
        </form>
        <div className="auth-footer">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;