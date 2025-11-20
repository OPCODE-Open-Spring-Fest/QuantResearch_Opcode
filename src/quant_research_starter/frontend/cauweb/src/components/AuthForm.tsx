import React, { useState } from 'react';
import { supabase } from '../utils/supabaseClient';

export const Signup: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg('');
    if (!supabase) {
      setMsg('Supabase not configured');
      return;
    }
    const { data, error } = await supabase.auth.signUp({ email, password });
    if (error) setMsg(error.message);
    else setMsg('Check your email for confirmation (if enabled).');
  };

  return (
    <form onSubmit={handleSignup} className="auth-form">
      <h2>Sign up</h2>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
      <button type="submit">Sign up</button>
      <div className="auth-msg">{msg}</div>
    </form>
  );
};

export const Login: React.FC<{ onLogin?: (token: string) => void }> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg('');
    if (!supabase) {
      setMsg('Supabase not configured');
      return;
    }
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setMsg(error.message);
      return;
    }
    const token = data.session?.access_token;
    if (token && onLogin) onLogin(token);
    setMsg('Logged in');
  };

  return (
    <form onSubmit={handleLogin} className="auth-form">
      <h2>Log in</h2>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
      <button type="submit">Log in</button>
      <div className="auth-msg">{msg}</div>
    </form>
  );
};
