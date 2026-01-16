# QuantResearch - Quick Reference Card

## 🎯 Currently Running

✅ **Backend**: http://localhost:8000 (FastAPI)  
✅ **Frontend**: http://localhost:3003 (React + Vite)  
✅ **Database**: Aiven PostgreSQL (Cloud)  
✅ **Redis**: Aiven Valkey (Cloud)  

---

## ⚡ Quick Commands

### Start Backend
```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch"
uvicorn src.quant_research_starter.api.main:app --reload --port 8000 --host 0.0.0.0
```

### Start Frontend
```bash
cd "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch\src\quant_research_starter\frontend\cauweb"
npm run dev
```

### Quick Test
```powershell
# Test Backend Health
Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing

# Test Assets API
Invoke-WebRequest -Uri "http://localhost:8000/api/assets/" -UseBasicParsing
```

---

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3003 | Main React Application |
| Backend | http://localhost:8000 | FastAPI Server |
| API Docs | http://localhost:8000/docs | Interactive API Documentation |
| Health | http://localhost:8000/api/health | API Health Check |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env` | Backend environment variables |
| `src/quant_research_starter/frontend/cauweb/.env` | Frontend environment variables |
| `src/quant_research_starter/api/main.py` | Backend entry point |
| `src/quant_research_starter/frontend/cauweb/src/App.tsx` | Frontend entry point |
| `SETUP_COMPLETE.md` | Full setup documentation |

---

## 🔑 Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection  
- `JWT_SECRET` - JWT signing key
- `CORS_ORIGINS` - Allowed origins
- `FINNHUB_API_KEY` - Market data API

### Frontend (cauweb/.env)
- `VITE_API_URL` - Backend API URL (http://localhost:8000)

---

## 📊 API Endpoints

### Public
- `GET /api/health` - Health check
- `GET /api/assets/` - Available assets

### Auth Required
- `POST /api/auth/register` - Register user
- `POST /api/auth/token` - Login
- `POST /api/backtest/` - Run backtest
- `GET /api/backtest/{id}/results` - Get results
- `GET /api/dashboard/*` - Dashboard data

---

## ✅ Verification Checklist

- ✅ Backend running on port 8000
- ✅ Frontend running on port 3003
- ✅ `/api/health` returns `{"status":"ok"}`
- ✅ `/api/assets/` returns data
- ✅ Frontend loads in browser
- ✅ No CORS errors
- ✅ Database connected
- ✅ Redis connected

---

## 🛠️ Troubleshooting

**Issue**: Port already in use  
**Fix**: Change port in command or kill existing process

**Issue**: CORS error  
**Fix**: Check CORS_ORIGINS in backend .env

**Issue**: API not found  
**Fix**: Verify VITE_API_URL in frontend .env

**Issue**: Database error  
**Fix**: Check DATABASE_URL and network connectivity

---

## 📚 Documentation

- Full Setup: `SETUP_COMPLETE.md`
- Backend: `BACKEND_SETUP.md`
- Dashboard: `DASHBOARD_README.md`
- Technical: `TECHNICAL_DOCS.md`

---

**Status**: ✅ FULLY OPERATIONAL  
**Version**: 0.1.0  
**Last Updated**: Jan 16, 2026
