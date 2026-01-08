# 📊 Dashboard Backend - Complete Guide

## 🎯 What Was Built

A **production-grade dashboard backend** for real-time portfolio management and analytics, seamlessly integrated into the existing QuantResearch project.

### Key Features

✅ **Real-time Portfolio Analytics** - Track portfolio value, P/L, and returns with live market data  
✅ **Risk Metrics Engine** - Sharpe ratio, max drawdown, volatility, beta, alpha calculations  
✅ **Live Market Data Integration** - Finnhub API with intelligent caching (1min quotes, 24hr profiles)  
✅ **Position Management** - Track open positions with unrealized P/L and sector allocation  
✅ **Trade History** - Complete trade log with realized P/L tracking  
✅ **Company Intelligence** - Logos, sector data, market cap, and company profiles  
✅ **JWT Authentication** - Secure user authentication integrated with existing auth system  
✅ **Performance Optimizations** - Async/await, connection pooling, batch operations, smart caching  

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  React Frontend │ ───> │  FastAPI Backend │ ───> │  PostgreSQL DB  │
│  (Port 3004)    │      │   (Port 8000)    │      │   (Aiven)       │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                               │                             │
                               │                             │
                               ▼                             ▼
                         ┌──────────┐              ┌─────────────────┐
                         │  Redis   │              │   Finnhub API   │
                         │ (Valkey) │              │  (Live Prices)  │
                         └──────────┘              └─────────────────┘
```

### Technology Stack

- **FastAPI** - Async Python web framework
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **Pydantic** - Data validation and schemas
- **JWT** - Token-based authentication
- **Finnhub.io** - Real-time stock quotes and company data
- **PostgreSQL 17.7** - Primary database (Aiven cloud)
- **Redis/Valkey 8.1.4** - Caching and pub/sub

## 🚀 Quick Start

### Step 1: Setup Database & Demo Data

```bash
# One command setup (creates tables + seeds data)
python scripts/setup_dashboard.py
```

This creates:
- ✅ All database tables (users, portfolios, positions, trades, stock_quotes, company_profiles)
- ✅ Demo user account (`demo` / `demo123`)
- ✅ 5 sample stock positions (AAPL, MSFT, GOOGL, TSLA, NVDA)
- ✅ Trade history with P/L examples

### Step 2: Start Backend

```bash
cd src/quant_research_starter
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

### Step 3: Test the API

#### Option A: Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click **"Authorize"** button (top right)
3. Enter credentials:
   - **Username:** `demo`
   - **Password:** `demo123`
4. Click "Authorize" → "Close"
5. Test any endpoint (they're now authenticated)

#### Option B: Using PowerShell

```powershell
# 1. Login to get JWT token
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/token" `
  -Method POST `
  -ContentType "application/x-www-form-urlencoded" `
  -Body "username=demo&password=demo123"

$token = $loginResponse.access_token

# 2. Get portfolio overview
Invoke-RestMethod -Uri "http://localhost:8000/api/dashboard/overview" `
  -Headers @{ Authorization = "Bearer $token" } | ConvertTo-Json -Depth 10

# 3. Get all positions with live prices
Invoke-RestMethod -Uri "http://localhost:8000/api/dashboard/positions" `
  -Headers @{ Authorization = "Bearer $token" } | ConvertTo-Json -Depth 10

# 4. Get trade history
Invoke-RestMethod -Uri "http://localhost:8000/api/dashboard/trades?limit=10" `
  -Headers @{ Authorization = "Bearer $token" } | ConvertTo-Json -Depth 10

# 5. Get live quote for AAPL
Invoke-RestMethod -Uri "http://localhost:8000/api/dashboard/quote/AAPL" `
  -Headers @{ Authorization = "Bearer $token" } | ConvertTo-Json -Depth 10
```

## 📡 API Endpoints

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### 1. Portfolio Overview
```http
GET /api/dashboard/overview
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_value": 142850.00,
    "cash": 57937.50,
    "invested": 84912.50,
    "market_value": 95107.20,
    "unrealized_pnl": 10194.70,
    "total_return_percent": 12.00,
    "sharpe_ratio": 1.85,
    "max_drawdown": 8.45,
    "volatility": 18.32,
    "win_rate": 100.00
  }
}
```

### 2. All Positions (with live prices)
```http
GET /api/dashboard/positions
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "quantity": 50,
      "average_cost": 175.50,
      "current_price": 196.56,
      "market_value": 9828.00,
      "unrealized_pnl": 1053.00,
      "unrealized_pnl_pct": 12.00,
      "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AAPL.png",
      "sector": "Technology"
    }
  ]
}
```

### 3. Trade History
```http
GET /api/dashboard/trades?limit=50
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "symbol": "AMZN",
      "trade_type": "sell",
      "quantity": 10,
      "price": 158.50,
      "commission": 1.50,
      "trade_date": "2024-01-10T00:00:00",
      "realized_pnl": 200.00
    }
  ]
}
```

### 4. Live Stock Quote
```http
GET /api/dashboard/quote/{symbol}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "symbol": "AAPL",
    "current_price": 196.56,
    "change": 2.34,
    "percent_change": 1.20,
    "high": 197.80,
    "low": 195.20,
    "open": 195.50,
    "previous_close": 194.22,
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

### 5. Company Profile
```http
GET /api/dashboard/profile/{symbol}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "symbol": "MSFT",
    "name": "Microsoft Corporation",
    "country": "US",
    "currency": "USD",
    "exchange": "NASDAQ",
    "ipo": "1986-03-13",
    "market_cap": 2800000000000,
    "industry": "Technology",
    "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/MSFT.png",
    "website": "https://www.microsoft.com"
  }
}
```

### 6. Performance History
```http
GET /api/dashboard/performance?days=30
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "date": "2024-01-15",
      "total_value": 142850.00,
      "return_pct": 12.00,
      "sharpe_ratio": 1.85
    }
  ]
}
```

## 🗄️ Database Schema

### New Models Added

**Portfolio** - Portfolio snapshots with performance metrics
- `total_value`, `cash`, `invested`
- `sharpe_ratio`, `max_drawdown`, `volatility`
- Tracks performance over time

**Position** - Open stock positions
- `symbol`, `quantity`, `average_cost`
- `current_price`, `unrealized_pnl`
- Links to `stock_quotes` and `company_profiles`

**Trade** - Complete trade history
- `symbol`, `trade_type` (buy/sell), `quantity`, `price`
- `realized_pnl`, `commission`, `trade_date`

**StockQuote** - Cached live market data
- `symbol`, `current_price`, `change`, `percent_change`
- `updated_at` for cache expiration (60 second TTL)

**CompanyProfile** - Company metadata
- `name`, `logo`, `sector`, `industry`, `market_cap`
- `updated_at` for cache expiration (24 hour TTL)

### Relationships

```
users (1) ──── (many) portfolios
users (1) ──── (many) positions
users (1) ──── (many) trades

positions (many) ──── (1) stock_quotes (via symbol)
positions (many) ──── (1) company_profiles (via symbol)
```

## 📁 Files Created/Modified

### New Services
- `src/quant_research_starter/api/services/__init__.py`
- `src/quant_research_starter/api/services/finnhub.py` - Finnhub API client
- `src/quant_research_starter/api/services/dashboard.py` - Business logic

### New Router
- `src/quant_research_starter/api/routers/dashboard.py` - 6 API endpoints

### Modified Files
- `src/quant_research_starter/api/models.py` - Added 5 new models
- `src/quant_research_starter/api/main.py` - Imported dashboard router

### Scripts
- `scripts/setup_dashboard.py` - Complete setup (tables + data)
- `scripts/seed_dashboard.py` - Data seeding only
- `scripts/test_dashboard.py` - Verification tests
- `scripts/create_tables.py` - Table creation only

### Documentation
- `DASHBOARD_WORKING.md` - Quick start guide (this file)
- `TECHNICAL_DOCS.md` - Architecture and implementation details

## 🔐 Security Features

✅ **Password Hashing** - bcrypt with automatic salt generation  
✅ **JWT Tokens** - Secure authentication with expiration  
✅ **SQL Injection Protection** - SQLAlchemy ORM (no raw SQL)  
✅ **CORS Configuration** - Controlled cross-origin access  
✅ **SSL/TLS** - Encrypted database and Redis connections  
✅ **Input Validation** - Pydantic schemas for all requests  

## ⚡ Performance Features

✅ **Async/Await** - Non-blocking I/O throughout  
✅ **Connection Pooling** - SQLAlchemy async pools  
✅ **Smart Caching** - Database-backed cache with TTL  
✅ **Batch Operations** - Multiple API calls in single batch  
✅ **Rate Limiting** - Finnhub API throttling (30 req/sec)  
✅ **Database Indexes** - Optimized queries  

### Caching Strategy

**Stock Quotes:**
- Cache duration: 60 seconds
- Reason: Real-time trading data needs to be fresh
- Storage: `stock_quotes` table

**Company Profiles:**
- Cache duration: 24 hours
- Reason: Static data rarely changes
- Storage: `company_profiles` table

## 🧪 Testing

### Manual Testing

```bash
# Run comprehensive tests
python scripts/test_dashboard.py
```

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Authorize with demo/demo123
3. Test each endpoint interactively
4. View request/response schemas

## 📊 Sample Data

### Demo User
- **Username:** `demo`
- **Password:** `demo123`
- **ID:** 1

### Stock Positions (5)
| Symbol | Shares | Avg Cost | Current Price* | Unrealized P/L* |
|--------|--------|----------|----------------|-----------------|
| AAPL   | 50     | $175.50  | Live           | Live            |
| MSFT   | 30     | $380.25  | Live           | Live            |
| GOOGL  | 25     | $142.30  | Live           | Live            |
| TSLA   | 20     | $245.80  | Live           | Live            |
| NVDA   | 15     | $495.60  | Live           | Live            |

*Live prices fetched from Finnhub API

### Trade History
- **AMZN:** Bought 10 @ $144.00, Sold 10 @ $158.50 → Profit: $200 (+13.79%)

## 🚨 Troubleshooting

### "Database connection failed"
- Check `.env` file has correct `DATABASE_URL`
- Verify firewall allows connection to Aiven
- Confirm SSL mode is set to `require`

### "Finnhub API error"
- Verify `FINNHUB_API_KEY` is set in `.env`
- Check you haven't exceeded rate limit (60 calls/min free tier)
- Visit https://finnhub.io to check API status

### "401 Unauthorized"
- Get new JWT token (tokens expire after 30 minutes)
- Verify username/password are correct
- Check `JWT_SECRET` is set in `.env`

### "Positions not showing live prices"
- Check Finnhub API key is valid
- Verify internet connectivity
- Check `stock_quotes` table has recent data

## 📚 Additional Resources

- **Swagger UI:** http://localhost:8000/docs - Interactive API testing
- **ReDoc:** http://localhost:8000/redoc - Beautiful API documentation
- **Health Check:** http://localhost:8000/api/health - Backend status
- **Technical Docs:** [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md) - Architecture details
- **Main README:** [README.md](README.md) - Full project overview

## 🎯 Next Steps

### Frontend Integration
1. Build React components to consume dashboard API
2. Display portfolio cards with live data
3. Create position table with real-time updates
4. Add trade history timeline
5. Implement charts for performance visualization

### Additional Features
- [ ] WebSocket real-time price streaming
- [ ] Trade execution simulation
- [ ] Alert/notification system
- [ ] Watchlist functionality
- [ ] Portfolio optimization
- [ ] More factor models
- [ ] Cryptocurrency support

## 🤝 Contributing

This dashboard backend is part of the QuantResearch open source project. Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern async Python**
