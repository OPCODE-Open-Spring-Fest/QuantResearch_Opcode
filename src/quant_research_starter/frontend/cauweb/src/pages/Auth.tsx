import React from 'react';
import { Login, Signup } from '../components/AuthForm';
import { supabase } from '../utils/supabaseClient';
import { useNavigate } from 'react-router-dom';

export const AuthPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLogin = (token: string) => {
    try {
      // store token for app usage; supabase-js also persists session
      window.localStorage.setItem('sb:token', token);
    } catch (err) {
      // ignore
    }
    navigate('/');
  };

  return (
    <div className="auth-page p-6">
      <div style={{ maxWidth: 420, margin: '0 auto' }}>
        <Login onLogin={handleLogin} />
        <hr className="my-6" />
        <Signup />
      </div>
    </div>
  );
};
