import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { BacktestStudio } from './pages/BacktestStudio';
import { ResearchLab } from './pages/ResearchLab';
import { PortfolioAnalytics } from './pages/PortfolioAnalytics';
import { Settings } from './pages/Settings';
import './styles/globals.css';


export const App: React.FC = () => {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <div className="main-content">
          <Header />
          <div className="page-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/backtest" element={<BacktestStudio />} />
              <Route path="/research" element={<ResearchLab />} />
              <Route path="/portfolio" element={<PortfolioAnalytics />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};