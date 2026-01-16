# QuantResearch - Complete Setup Guide & Verification

## ✅ System Status

**Backend**: ✅ Running on http://localhost:8000  
**Frontend**: ✅ Running on http://localhost:3003  
**Database**: ✅ Connected to Aiven PostgreSQL  
**Redis**: ✅ Connected to Aiven Valkey  
**API**: ✅ All endpoints operational

---

## 📋 Project Architecture

### Backend (FastAPI + Python)
- **Location**: `src/quant_research_starter/api/`
- **Port**: 8000
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL (Aiven Cloud)
- **Cache/Queue**: Redis/Valkey (Aiven Cloud)
- **Features**:
  - User authentication (JWT tokens)
  - Backtest execution (Celery workers)
  - Asset data management
  - WebSocket support for real-time updates
  - Dashboard analytics

### Frontend (React + TypeScript + Vite)
- **Location**: `src/quant_research_starter/frontend/cauweb/`
- **Port**: 3003
- **Framework**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS v4
- **Charts**: Chart.js + react-chartjs-2
- **Routing**: React Router v6
- **Features**:
  - Dashboard with portfolio metrics
  - Backtest Studio for strategy testing
  - Research Lab for data analysis
  - Portfolio Analytics
  - Settings management

---

## 🚀 Quick Start

### 1. Start Backend Server

```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch"
uvicorn src.quant_research_starter.api.main:app --reload --port 8000 --host 0.0.0.0
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
✅ Redis listener connected successfully
```

### 2. Start Frontend Server

```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch\src\quant_research_starter\frontend\cauweb"
npm run dev
```

**Expected Output**:
```
VITE v5.4.21  ready in 1944 ms
➜  Local:   http://localhost:3003/
```

### 3. Access Application

- **Frontend**: http://localhost:3003
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/api/health

---

## 🔧 Environment Configuration

### Backend Environment (`.env`)
```env
# Database Configuration (Aiven PostgreSQL)
DATABASE_URL=postgresql+asyncpg://username:password@your-host:port/dbname?ssl=require

# Redis Configuration (Aiven Valkey)
REDIS_URL=rediss://default:password@your-redis-host:port

# JWT Configuration
JWT_SECRET=dev_prajwal_secret_123

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3004,http://localhost:3003,http://127.0.0.1:3003

# Output Directory
OUTPUT_DIR=output/

# Finnhub API (for market data)
FINNHUB_API_KEY=d5f5pdpr01qtf8iml9cgd5f5pdpr01qtf8iml9d0
```

### Frontend Environment (`src/quant_research_starter/frontend/cauweb/.env`)
```env
# Backend API URL
VITE_API_URL=http://localhost:8000

# Supabase Configuration (Optional)
# VITE_SUPABASE_URL=your-supabase-url
# VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

---

## 📡 API Endpoints

### Health & Status
- `GET /api/health` - Health check endpoint
- Returns: `{"status":"ok"}`

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login and get JWT token

### Assets
- `GET /api/assets/` - Get available assets/symbols
- Returns: Array of `{symbol, price}` objects

### Backtest
- `POST /api/backtest/` - Submit backtest job
- `GET /api/backtest/{job_id}/results` - Get backtest results
- `WS /api/backtest/ws/{job_id}` - WebSocket for real-time updates

### Dashboard
- `GET /api/dashboard/overview` - Portfolio overview metrics
- `GET /api/dashboard/positions` - Current positions
- `GET /api/dashboard/trades` - Trade history
- `GET /api/dashboard/quote/{symbol}` - Real-time quote
- `GET /api/dashboard/profile/{symbol}` - Symbol profile
- `GET /api/dashboard/performance` - Performance metrics

---

## ✅ Verification Tests

### Test Backend Health
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```
**Expected**: `{"status":"ok"}`

### Test Assets Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/assets/" -UseBasicParsing | Select-Object -ExpandProperty Content
```
**Expected**: Array of symbols with prices

### Test Frontend
1. Open http://localhost:3003 in browser
2. Navigate to different pages:
   - Dashboard (/)
   - Backtest Studio (/backtest)
   - Research Lab (/research)
   - Portfolio Analytics (/portfolio)
   - Settings (/settings)

---

## 🔌 Frontend-Backend Connection

### How it Works

1. **API Configuration** (`src/quant_research_starter/frontend/cauweb/src/utils/api.ts`):
   - Reads `VITE_API_URL` from environment
   - Falls back to mock data if no backend configured
   - Includes authentication headers automatically

2. **CORS Configuration** (Backend):
   - Configured to allow requests from frontend origins
   - Supports credentials for authentication

3. **Authentication Flow**:
   - JWT tokens stored in localStorage
   - Automatically included in API requests
   - Supabase integration available as alternative

---

## 📦 Dependencies

### Backend (Python 3.11+)
- FastAPI 0.128.0 - Web framework
- Uvicorn 0.40.0 - ASGI server
- SQLAlchemy 2.0.45 - ORM
- Asyncpg 0.31.0 - PostgreSQL driver
- Alembic 1.18.1 - Database migrations
- Celery 5.6.2 - Task queue
- Redis 7.1.0 - Caching/messaging
- Pandas 2.3.3 - Data analysis
- NumPy 2.4.1 - Numerical computing
- SciPy 1.17.0 - Scientific computing
- Scikit-learn 1.8.0 - Machine learning
- Optuna 4.6.0 - Hyperparameter optimization
- Matplotlib 3.10.8 - Plotting
- Plotly 6.5.2 - Interactive plots
- Python-Jose 3.5.0 - JWT handling
- Passlib 1.7.4 - Password hashing
- WebSockets 16.0 - WebSocket support

### Frontend (Node.js 23.3.0)
- React 18.2.0 - UI library
- React Router DOM 6.8.0 - Routing
- TypeScript 5.9.3 - Type safety
- Vite 5.0.0 - Build tool
- Tailwind CSS 4.1.17 - Styling
- Chart.js 4.5.1 - Charts
- React-Chartjs-2 5.3.1 - React wrapper for Chart.js
- Lucide React 0.263.1 - Icons
- @supabase/supabase-js 2.83.0 - Supabase client

---

## 🛠️ Development Workflow

### Making Changes

1. **Backend Changes**:
   - Edit files in `src/quant_research_starter/api/`
   - Server auto-reloads with `--reload` flag
   - Check logs in terminal

2. **Frontend Changes**:
   - Edit files in `src/quant_research_starter/frontend/cauweb/src/`
   - Vite HMR updates instantly
   - Check browser console for errors

### Adding New API Endpoints

1. Create router in `src/quant_research_starter/api/routers/`
2. Import and include in `main.py`
3. Add corresponding frontend API call in `utils/api.ts`

### Adding New Frontend Pages

1. Create page component in `src/pages/`
2. Add route in `App.tsx`
3. Update navigation in `components/Navigation.tsx`

---

## 🔒 Security Notes

### Current Status
- ✅ Environment variables for sensitive data
- ✅ JWT authentication implemented
- ✅ CORS configured properly
- ✅ SSL/TLS for database connections
- ⚠️ JWT_SECRET should be changed for production
- ⚠️ Additional rate limiting recommended

### Production Recommendations
1. Use strong, randomly generated JWT_SECRET
2. Enable HTTPS for all connections
3. Implement rate limiting
4. Add request validation
5. Enable database connection pooling
6. Configure proper CORS origins (remove *)
7. Use environment-specific configs
8. Enable logging and monitoring

---

## 📊 Database Schema

### Main Tables
- **users** - User accounts and authentication
- **backtest_jobs** - Backtest job tracking
- **backtest_results** - Backtest output data
- **assets** - Available trading symbols
- **positions** - Current portfolio positions
- **trades** - Trade history

### Migrations
Located in `src/quant_research_starter/api/alembic/versions/`

Run migrations:
```bash
python scripts/run_migrations.py
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Database connection error  
**Solution**: Check DATABASE_URL in .env and network connectivity to Aiven

**Problem**: Redis connection error  
**Solution**: Check REDIS_URL in .env and firewall settings

**Problem**: Port 8000 already in use  
**Solution**: Change port with `--port 8001` or stop other process

### Frontend Issues

**Problem**: Blank page or React errors  
**Solution**: Check browser console, verify backend is running

**Problem**: API calls failing  
**Solution**: Verify VITE_API_URL in .env, check CORS settings

**Problem**: Port 3003 already in use  
**Solution**: Edit `vite.config.ts` to change port

### Common Issues

**Problem**: CORS errors  
**Solution**: Ensure frontend origin is in CORS_ORIGINS in backend .env

**Problem**: Authentication errors  
**Solution**: Clear localStorage and re-login

---

## 🎯 Next Steps

1. **User Registration**: Create test users via `/api/auth/register`
2. **Run Backtests**: Use Backtest Studio to test strategies
3. **Explore Data**: Check Research Lab for data analysis
4. **Monitor Portfolio**: View Dashboard for portfolio metrics
5. **Customize Settings**: Adjust preferences in Settings page

---

## 📝 Additional Documentation

- [Backend Setup](BACKEND_SETUP.md) - Detailed backend configuration
- [Dashboard Documentation](DASHBOARD_README.md) - Dashboard features
- [Technical Documentation](TECHNICAL_DOCS.md) - Architecture details
- [Contributing Guide](CONTRIBUTING.md) - Contribution guidelines

---

## 🎉 Success Criteria

✅ Backend server running on port 8000  
✅ Frontend server running on port 3003  
✅ Database connected to Aiven PostgreSQL  
✅ Redis connected to Aiven Valkey  
✅ Health endpoint returning `{"status":"ok"}`  
✅ Assets endpoint returning data  
✅ Frontend loading in browser  
✅ All pages accessible  
✅ API calls working from frontend  
✅ CORS configured correctly  
✅ Environment variables set properly  

---

**Status**: ✅ **FULLY OPERATIONAL**

**Last Verified**: January 16, 2026  
**Version**: 0.1.0

---

## 🚀 Commands Reference

### Start Everything (Two Terminals Required)

**Terminal 1 - Backend**:
```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch"
uvicorn src.quant_research_starter.api.main:app --reload --port 8000 --host 0.0.0.0
```

**Terminal 2 - Frontend**:
```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch\src\quant_research_starter\frontend\cauweb"
npm run dev
```

### Optional - Celery Worker (for background tasks)

**Terminal 3 - Worker**:
```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch"
celery -A src.quant_research_starter.api.tasks.celery_app.celery_app worker --loglevel=info
```

---

**🎊 Your QuantResearch application is now fully connected and operational! 🎊**
