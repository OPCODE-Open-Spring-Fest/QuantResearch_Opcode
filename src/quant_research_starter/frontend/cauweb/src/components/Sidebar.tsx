import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, TrendingUp, BarChart3, PlayCircle, Wallet, Eye, Bell, Activity, LogOut, User } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  const links = [
    { to: '/', icon: Home, label: 'Dashboard' },
    { to: '/trading', icon: TrendingUp, label: 'Trading' },
    { to: '/portfolio', icon: BarChart3, label: 'Portfolio' },
    { to: '/backtest', icon: PlayCircle, label: 'Backtest' },
    { to: '/watchlists', icon: Eye, label: 'Watchlists' },
    { to: '/alerts', icon: Bell, label: 'Alerts' },
    { to: '/cash', icon: Wallet, label: 'Cash' },
    { to: '/status', icon: Activity, label: 'Status' },
  ];

  return (
    <div className="sidebar">
      <div className="logo">CAUQUANT</div>
      <nav className="nav">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink key={link.to} to={link.to} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              <Icon size={20} />
              <span>{link.label}</span>
            </NavLink>
          );
        })}
      </nav>
      <div style={{ 
        padding: '1.5rem', 
        borderTop: '1px solid var(--border)',
        marginTop: 'auto'
      }}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <div style={{ 
              width: '40px', 
              height: '40px', 
              borderRadius: '50%',
              background: 'var(--gray-mid)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <User size={20} />
            </div>
            <div>
              <div style={{ fontWeight: '600', fontSize: '0.875rem' }}>
                {user.email || 'User'}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-light)' }}>
                Trader
              </div>
            </div>
          </div>
        </div>
        <button 
          onClick={handleLogout}
          className="btn btn-secondary"
          style={{ width: '100%' }}
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </div>
  );
};
