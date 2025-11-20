import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn } from 'lucide-react';

// Render the CTA unconditionally to ensure visibility while debugging.
export const AuthFloatingButton: React.FC = () => {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate('/login')}
      aria-label="Login or Sign up"
      className="fixed bottom-6 right-6 z-50 flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
    >
      <LogIn className="w-4 h-4" />
      <span className="hidden sm:inline">Login / Sign up</span>
    </button>
  );
};

export default AuthFloatingButton;
