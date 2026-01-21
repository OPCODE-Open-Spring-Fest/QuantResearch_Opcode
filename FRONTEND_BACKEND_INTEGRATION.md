# Frontend-Backend Integration Guide

## Overview
This document provides the complete setup for connecting the React frontend with the FastAPI backend for the QuantResearch platform.

## Architecture

### Backend (FastAPI)
- **URL**: `http://localhost:8000`
- **Authentication**: JWT tokens
- **API Prefix**: `/api`

### Frontend (React + Vite)
- **URL**: `http://localhost:3003`
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite

## Setup Instructions

### 1. Backend Setup

#### Install Dependencies
```bash
cd c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch
pip install -r requirements-dev.txt
```

#### Configure Environment
Create/update `.env` in the root directory:
```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/qrs
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET=your-secret-key-change-this-in-production
ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# CORS - Allow frontend origins
CORS_ORIGINS=http://localhost:3003,http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
```

#### Start Backend
```bash
# Make sure PostgreSQL and Redis are running
# Then start the backend
uvicorn src.quant_research_starter.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd src\quant_research_starter\frontend\cauweb
```

#### Install Dependencies
```bash
npm install
```

#### Configure Environment
The `.env` file is already configured:
```env
# Backend API URL (must match where backend is running)
VITE_API_URL=http://localhost:8000

# WebSocket URL (for real-time updates)
VITE_WS_URL=ws://localhost:8000
```

#### Start Frontend
```bash
npm run dev
```

The frontend will be available at `http://localhost:3003`

## Key Files Updated

### 1. `src/utils/api.ts` - API Client
**Location**: `src/quant_research_starter/frontend/cauweb/src/utils/api.ts`

**Key Changes**:
- ✅ Uses environment variable `VITE_API_URL` instead of hardcoded URL
- ✅ Centralized error handling with `handleApiError()`
- ✅ Automatic token management from localStorage
- ✅ Auto-redirect to login on 401 Unauthorized

**Usage Example**:
```typescript
// Login
const data = await api.login(email, password);
localStorage.setItem('token', data.access_token);

// Fetch protected data
const positions = await api.getPositions();
```

### 2. `src/context/AuthContext.tsx` - Authentication Context
**Location**: `src/quant_research_starter/frontend/cauweb/src/context/AuthContext.tsx`

**Key Changes**:
- ✅ Removed Supabase dependency
- ✅ Pure JWT token-based authentication
- ✅ Persistent auth state via localStorage
- ✅ Simple API: `setAuthData()` and `clearAuth()`

**Usage Example**:
```typescript
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, setAuthData, clearAuth } = useAuth();
  
  // After login
  setAuthData(token, { id: 1, username: 'user@example.com', email: 'user@example.com' });
  
  // Logout
  clearAuth();
}
```

### 3. `src/main.tsx` - Application Entry
**Location**: `src/quant_research_starter/frontend/cauweb/src/main.tsx`

**Key Changes**:
- ✅ Wrapped app with `<AuthProvider>` for global auth state

### 4. Environment Files
- ✅ `.env` - Active environment configuration
- ✅ `.env.example` - Template for new setups

## API Endpoints Reference

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login (returns JWT token)
- `GET /api/auth/me` - Get current user info

### Dashboard
- `GET /api/dashboard/overview` - Dashboard statistics
- `GET /api/dashboard/positions` - User positions
- `GET /api/dashboard/trades` - Recent trades

### Trading
- `POST /api/positions/buy` - Buy stock
- `POST /api/positions/sell` - Sell stock
- `GET /api/positions` - Get all positions
- `GET /api/trades` - Get trade history

### Portfolio
- `GET /api/portfolio/balance` - Get portfolio balance
- `POST /api/portfolio/deposit` - Deposit cash
- `POST /api/portfolio/withdraw` - Withdraw cash

### Backtest
- `POST /api/backtest` - Run backtest
- `GET /api/backtest/{jobId}/results` - Get backtest results

### Watchlists
- `GET /api/watchlists` - Get all watchlists
- `POST /api/watchlists` - Create watchlist
- `POST /api/watchlists/{id}/symbols` - Add symbol to watchlist

### Alerts
- `GET /api/alerts` - Get all alerts
- `POST /api/alerts` - Create alert
- `DELETE /api/alerts/{id}` - Delete alert

### Strategies
- `GET /api/strategies` - Get all strategies
- `POST /api/strategies` - Create strategy
- `POST /api/strategies/{id}/activate` - Activate strategy
- `POST /api/strategies/{id}/deactivate` - Deactivate strategy

## Authentication Flow

### 1. Registration
```typescript
const response = await api.register('user@example.com', 'password123');
// User created, now login
```

### 2. Login
```typescript
const data = await api.login('user@example.com', 'password123');
localStorage.setItem('token', data.access_token);
localStorage.setItem('user', JSON.stringify({ email: 'user@example.com' }));
window.location.href = '/';
```

### 3. Protected Requests
All API requests automatically include the JWT token from localStorage:
```typescript
// Automatically includes: Authorization: Bearer <token>
const positions = await api.getPositions();
```

### 4. Token Expiry
When a token expires (401 Unauthorized), the app automatically:
1. Clears localStorage (token + user)
2. Redirects to `/login`
3. Shows "Session expired" message

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3003` (default frontend port)
- `http://localhost:3000` (alternative)
- `http://localhost:3004-3006` (for testing)

To add more origins, update `CORS_ORIGINS` in backend `.env`:
```env
CORS_ORIGINS=http://localhost:3003,http://localhost:3000,http://yourdomain.com
```

## Testing the Integration

### 1. Start Services
```bash
# Terminal 1 - Backend
cd c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch
uvicorn src.quant_research_starter.api.main:app --reload --port 8000

# Terminal 2 - Frontend
cd src\quant_research_starter\frontend\cauweb
npm run dev
```

### 2. Test Authentication
1. Open `http://localhost:3003`
2. Click "Register" and create account
3. Login with credentials
4. You should be redirected to dashboard

### 3. Test API Calls
Open browser DevTools Console and test:
```javascript
// Should show 401 without token
fetch('http://localhost:8000/api/dashboard/overview')

// Login first, then try again
// Should work with token in localStorage
```

## Troubleshooting

### Issue: "Cannot connect to backend"
**Solution**: 
- Verify backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env`
- Ensure no firewall blocking localhost:8000

### Issue: "401 Unauthorized"
**Solution**:
- Check if token exists: `localStorage.getItem('token')`
- Verify token is valid (not expired)
- Re-login to get fresh token

### Issue: CORS errors
**Solution**:
- Add frontend URL to `CORS_ORIGINS` in backend `.env`
- Restart backend after changing .env
- Clear browser cache

### Issue: "Session expired" loop
**Solution**:
- Clear localStorage: `localStorage.clear()`
- Register new account or login again
- Check JWT_EXPIRE_MINUTES in backend .env

## Production Deployment

### Backend
1. Set strong `JWT_SECRET` in production
2. Use production database URL
3. Set `CORS_ORIGINS` to actual frontend domain
4. Enable HTTPS

### Frontend
1. Build production bundle: `npm run build`
2. Update `VITE_API_URL` to production backend URL
3. Deploy `dist/` folder to static hosting (Vercel, Netlify, etc.)

## Environment Variables Summary

### Backend (.env in root)
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=change-this-to-random-secret
JWT_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3003
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env in frontend/cauweb)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Security Best Practices

1. ✅ **Never commit .env files** - Use .env.example as template
2. ✅ **Use strong JWT secrets** - Generate random 32+ character strings
3. ✅ **Set appropriate token expiry** - Balance security vs UX
4. ✅ **Validate all inputs** - Backend validates all requests
5. ✅ **Use HTTPS in production** - Never send tokens over HTTP
6. ✅ **Implement rate limiting** - Prevent brute force attacks
7. ✅ **Log security events** - Monitor authentication attempts

## Complete Working Flow

```
User Registration/Login
        ↓
Frontend sends credentials to /api/auth/token
        ↓
Backend validates & returns JWT token
        ↓
Frontend stores token in localStorage
        ↓
Frontend includes token in all API requests
        ↓
Backend validates token & processes request
        ↓
Frontend displays data to user
```

## Next Steps

1. ✅ Frontend and backend are connected
2. ✅ Authentication works with JWT tokens
3. ✅ All API endpoints are integrated
4. 🔜 Add real-time features with WebSockets
5. 🔜 Implement refresh tokens for better UX
6. 🔜 Add user profile management
7. 🔜 Deploy to production

---

**Status**: ✅ Frontend-Backend Integration Complete and Working!

Last Updated: January 2026
