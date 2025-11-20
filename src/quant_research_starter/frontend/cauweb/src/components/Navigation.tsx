import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  PlayCircle, 
  Beaker, 
  PieChart, 
  Settings,
  TrendingUp
} from 'lucide-react';

export const Navigation: React.FC = () => {
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/backtest', icon: PlayCircle, label: 'Backtest Studio' },
    { path: '/research', icon: Beaker, label: 'Research Lab' },
    { path: '/portfolio', icon: PieChart, label: 'Portfolio Analytics' },
    { path: '/settings', icon: Settings, label: 'Settings' },
    { path: '/login', icon: TrendingUp, label: 'Login' }
  ];

  return (
    <nav className="navigation">
      {/* Logo */}
      <div className="nav-header">
        <div className="nav-logo">
          <div className="logo-icon">
            <TrendingUp size={20} />
          </div>
          <div className="logo-text">
            <h1>CAUQuant</h1>
            <p>Research Platform</p>
          </div>
        </div>
      </div>

      {/* Navigation Items */}
      <div className="nav-items">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `nav-item ${isActive ? 'active' : ''}`
              }
            >
              <Icon className="icon" size={20} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      {/* Quick Stats */}
      <div className="nav-stats">
        <div className="stat-item">
          <span>Strategies</span>
          <span>12</span>
        </div>
        <div className="stat-item">
          <span>Assets</span>
          <span>248</span>
        </div>
        <div className="stat-item">
          <span>Backtests</span>
          <span>1.2K</span>
        </div>
      </div>
    </nav>
  );
};