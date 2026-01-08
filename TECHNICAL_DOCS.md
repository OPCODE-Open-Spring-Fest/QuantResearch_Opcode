# 🎯 Dashboard Backend - Technical Documentation

## Architecture Overview

The dashboard backend follows a **Service Layer Architecture** pattern for clean separation of concerns and maintainability.

### Layers

```
┌─────────────────────────────────────────┐
│         API Layer (Routers)             │
│  - HTTP endpoints                       │
│  - Request/response handling            │
│  - Authentication                       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Service Layer (Business Logic)    │
│  - Dashboard calculations               │
│  - Risk metrics                         │
│  - External API integration             │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Data Layer (Models & DB)          │
│  - SQLAlchemy models                    │
│  - Database queries                     │
│  - Data persistence                     │
└─────────────────────────────────────────┘
```

## Key Components

### 1. Models (`src/quant_research_starter/api/models.py`)

**Portfolio Model**
- Stores portfolio snapshots with timestamp
- Tracks total value, cash, invested amounts
- Calculates returns and performance metrics
- Includes risk metrics (Sharpe, volatility, max drawdown)

**Position Model**
- Tracks open stock positions
- Real-time P/L calculation
- Sector and industry classification
- Links to company profiles

**Trade Model**
- Complete trade history
- Realized P/L tracking
- Buy/sell type identification
- Commission tracking

**StockQuote Model**
- Cached live market data
- Updates from Finnhub API
- 1-minute cache TTL
- Price, volume, change tracking

**CompanyProfile Model**
- Company metadata
- Logo, sector, industry
- Market cap, IPO date
- 24-hour cache TTL

### 2. Services

#### Finnhub Service (`src/quant_research_starter/api/services/finnhub.py`)

**Purpose:** External API integration with intelligent caching

**Features:**
- Async HTTP client (httpx)
- Rate limiting (30 req/sec)
- Smart caching strategy
- Error handling and retries
- Batch operations

**Key Methods:**
```python
async def get_quote(symbol: str) -> dict
async def get_company_profile(symbol: str) -> dict
async def update_cached_quote(db, symbol) -> StockQuote
async def batch_update_quotes(db, symbols) -> dict
```

**Caching Strategy:**
- Quotes: 60 seconds (real-time trading)
- Profiles: 24 hours (static data)
- Database-backed cache
- Automatic expiration

#### Dashboard Service (`src/quant_research_starter/api/services/dashboard.py`)

**Purpose:** Business logic and calculations

**Features:**
- Portfolio metrics calculation
- Risk analysis (Sharpe, volatility, max drawdown)
- Trade statistics (win rate, avg profit)
- Position enrichment with live data
- Historical performance analysis

**Key Methods:**
```python
async def calculate_portfolio_metrics(db, user_id) -> dict
async def get_positions_with_live_data(db, user_id) -> list
async def update_position_prices(db, position) -> Position
async def get_recent_trades(db, user_id, limit) -> list
```

**Risk Metrics Calculations:**

**Sharpe Ratio:**
```python
sharpe = (avg_return * 252) / (volatility * sqrt(252))
```

**Max Drawdown:**
```python
max_dd = max((peak - trough) / peak for all peaks)
```

**Volatility (Annualized):**
```python
volatility = stdev(daily_returns) * sqrt(252)
```

### 3. Routers (`src/quant_research_starter/api/routers/dashboard.py`)

**Purpose:** HTTP endpoint definitions

**Authentication:** All endpoints require JWT token

**Endpoints:**

| Endpoint | Method | Description | Cache |
|----------|--------|-------------|-------|
| `/overview` | GET | Complete portfolio metrics | No |
| `/positions` | GET | All positions + live prices | No |
| `/trades` | GET | Trade history | No |
| `/quote/{symbol}` | GET | Live stock quote | 60s |
| `/profile/{symbol}` | GET | Company profile | 24h |
| `/performance` | GET | Historical time series | No |

**Dependency Injection:**
```python
dashboard_service: DashboardService = Depends(get_dashboard_service)
current_user: User = Depends(get_current_user)
db: AsyncSession = Depends(get_session)
```

## Data Flow

### Example: Get Portfolio Overview

```
1. Client sends GET /api/dashboard/overview
   ↓
2. Router validates JWT token
   ↓
3. Router calls DashboardService.calculate_portfolio_metrics()
   ↓
4. Service queries all open positions from database
   ↓
5. Service calls FinnhubService.batch_update_quotes()
   ↓
6. Finnhub Service checks cache, fetches if expired
   ↓
7. Service calculates:
   - Total values (market value, cost basis)
   - Returns (absolute and percentage)
   - Risk metrics from historical snapshots
   - Trade statistics
   ↓
8. Service saves portfolio snapshot to database
   ↓
9. Router returns JSON response to client
```

## Database Schema

### Key Relationships

```sql
users (1) ──── (many) portfolios
users (1) ──── (many) positions
users (1) ──── (many) trades

positions (many) ──── (1) stock_quotes (symbol)
positions (many) ──── (1) company_profiles (symbol)
```

### Indexes

Performance-critical indexes:
- `positions.user_id` - Fast user position lookup
- `positions.symbol` - Quick symbol search
- `positions.status` - Filter open/closed
- `trades.user_id` - User trade history
- `trades.symbol` - Symbol trade history
- `trades.trade_date` - Chronological sorting
- `stock_quotes.symbol` - Quote lookup
- `stock_quotes.updated_at` - Cache expiration check

## Performance Considerations

### Async/Await Pattern

All I/O operations use async/await:
```python
async with db.begin():
    result = await db.execute(query)
    data = result.scalars().all()
```

### Connection Pooling

SQLAlchemy async pool configuration:
```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
```

### Batch Operations

Fetch multiple quotes in one batch:
```python
symbols = [p.symbol for p in positions]
quotes = await finnhub.batch_update_quotes(db, symbols)
```

### Caching Strategy

**Database-backed cache:**
- Store in `stock_quotes` table
- Check `updated_at` timestamp
- Return cached if fresh, fetch if stale

**Benefits:**
- Reduces API calls (costs)
- Faster response times
- Survives server restarts
- Shared across requests

## Error Handling

### Graceful Degradation

```python
try:
    quote = await finnhub.get_quote(symbol)
except Exception as e:
    logger.error(f"Finnhub error: {e}")
    # Return cached data or default values
    return cached_quote or default_quote
```

### Logging Levels

- **INFO**: Successful operations, cache hits
- **WARNING**: API failures, degraded service
- **ERROR**: Database errors, critical failures
- **DEBUG**: Detailed request/response data

## Security

### JWT Authentication

```python
@router.get("/overview")
async def get_overview(
    current_user: User = Depends(get_current_user)
):
    # current_user automatically populated from JWT
    # or 401 error if invalid/missing token
```

### SQL Injection Prevention

Using SQLAlchemy ORM (no raw SQL):
```python
# Safe - parameterized query
result = await db.execute(
    select(Position).where(Position.user_id == user_id)
)
```

### Password Security

- bcrypt hashing with salt
- Never store plain text
- Automatic salt generation

## Testing

### Unit Testing

Test individual components:
```python
# Test Finnhub service
async def test_get_quote():
    service = FinnhubService(api_key="test")
    quote = await service.get_quote("AAPL")
    assert quote["c"] > 0
```

### Integration Testing

Test complete flows:
```python
# Test dashboard endpoint
async def test_portfolio_overview():
    response = await client.get(
        "/api/dashboard/overview",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "total_value" in response.json()["data"]
```

## Monitoring & Observability

### Logging

Comprehensive logging for debugging:
```python
logger.info(f"Updated quote for {symbol}: ${price}")
logger.error(f"API error: {e}", exc_info=True)
```

### Metrics to Track

- API response times
- Cache hit/miss rates
- Database query performance
- External API call frequency
- Error rates by endpoint

## Deployment Checklist

- [ ] Set strong JWT_SECRET
- [ ] Use production database
- [ ] Enable SSL for all connections
- [ ] Set CORS_ORIGINS to production domain
- [ ] Configure proper logging
- [ ] Set up monitoring/alerts
- [ ] Enable database backups
- [ ] Use environment variables
- [ ] Configure rate limiting
- [ ] Set up health checks

## Troubleshooting

### Common Issues

**Database Connection Failed**
- Check DATABASE_URL format
- Verify firewall allows connection
- Confirm SSL mode matches server

**Finnhub API Errors**
- Check API key is valid
- Verify rate limiting not exceeded
- Check internet connectivity

**Authentication Fails**
- Verify JWT_SECRET matches
- Check token expiration
- Confirm user exists in database

**Slow Performance**
- Check database indexes exist
- Verify caching is working
- Monitor external API latency
- Check connection pool size

---

For more details, see the main [README.md](README.md) or [DASHBOARD_WORKING.md](DASHBOARD_WORKING.md).
