# QuantResearch

check out the [link](https://qrsopcode.netlify.app/)

> **QuantResearch** — research-grade quantitative strategy starter kit with an interactive React/TypeScript frontend (cauweb), Python backtesting core, and legacy Streamlit dashboards archived under `legacy/streamlit/`.

---

## Table of contents

* [Project overview](#project-overview)
* [What’s included](#whats-included)
* [Prerequisites](#prerequisites)
* [Quickstart (dev)](#quickstart-dev)

  * [Run backend (Python)](#run-backend-python)
  * [Run frontend (cauweb)](#run-frontend-cauweb)
  * [Run with mock WS / demo mode](#run-with-mock-ws--demo-mode)
* [Production build & docker](#production-build--docker)
* [Realtime contract & WS guide](#realtime-contract--ws-guide)
* [APIs & Data flows](#apis--data-flows)
* [Testing & CI](#testing--ci)
* [Streamlit (legacy) status & migration notes](#streamlit-legacy-status--migration-notes)
* [Developer workflow & conventions](#developer-workflow--conventions)
* [Contributing](#contributing)
* [Roadmap / recommended next issues](#roadmap--recommended-next-issues)
* [License & contact](#license--contact)

---

## Project overview

This repository provides a complete starter environment for research and prototyping in quantitative finance. It consists of:

* A **Python core** for factor computation, backtesting, and research workflows (packaged under `src/quant_research_starter/`).
* A modern **React + TypeScript frontend** at `src/quant_research_starter/frontend/cauweb/` for interactive dashboards, live visualizations, strategy management and job control.
* A legacy **Streamlit** UI archived under `legacy/streamlit/` (kept for reference and reproducibility).
* Tooling to support reproducible experiments, unit tests, linting, and CI automation.

This README explains how to run both components in dev and production, how realtime is wired, and how to extend the system.

---

## What’s included (high-level)

```
/ (repo root)
├─ src/quant_research_starter/
│  ├─ core/            # Python backtest + factors + utils
│  ├─ api/             # Python FastAPI or Flask endpoints (if present)
│  └─ frontend/
│     └─ cauweb/       # React + TS frontend
├─ legacy/streamlit/   # archived Streamlit apps (read-only)
├─ notebooks/          # Demo notebooks and reproducible examples
├─ tests/              # Unit tests (python) + frontend tests
├─ .github/            # CI workflows (build, tests, docs)
└─ pyproject.toml / package.json
```

---

## Prerequisites

* **Node**: v18.x or later (v23.3.0 recommended) — used by `cauweb` (frontend)
* **Yarn** or **npm**: prefer `npm ci` for CI reproducibility
* **Python**: 3.10 / 3.11+ (3.11.6 recommended)
* **Database**: PostgreSQL (Aiven Cloud or local)
* **Redis**: Redis/Valkey for caching and task queue
* Optional: **Docker** for containerized builds
* Optional: **VS Code** + Remote Containers if using `.devcontainer`

Ensure `NODE_ENV` and Python virtualenv are isolated per project.

### 🚀 Quick Setup (New!)

For a complete backend-frontend integration setup, see:
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Complete setup guide with architecture
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference card
- **[start.ps1](start.ps1)** - Windows PowerShell startup script

---

## Quickstart (dev)

Follow these steps to run the backend and frontend locally. The instructions assume you're at the repo root.

### 1) Set up Python env & install backend deps

```bash
# create venv (recommended)
python -m venv .venv
# Activate on Linux/macOS:
source .venv/bin/activate
# Activate on Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -U pip
pip install -e .
```

### 2) Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname?ssl=require
REDIS_URL=rediss://default:pass@host:port
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3003,http://localhost:3004,http://localhost:5173
FINNHUB_API_KEY=your-api-key
OUTPUT_DIR=output/
```

Create frontend environment file at `src/quant_research_starter/frontend/cauweb/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### 3) Start the Python backend (FastAPI)

```bash
# From repo root
uvicorn src.quant_research_starter.api.main:app --reload --port 8000 --host 0.0.0.0
```

The backend API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/health

### 4) Run cauweb (React + TS) in dev mode

Open a new terminal and run:

```bash
cd src/quant_research_starter/frontend/cauweb
npm install
npm run dev
```

The frontend will be available at:
- **App**: http://localhost:3003 (or next available port)

**Note**: The frontend is configured to connect to the backend at `http://localhost:8000` via the `VITE_API_URL` environment variable.

### ⚡ Alternative: Quick Start Script (Windows)

```powershell
.\start.ps1
```

This script will:
1. Check Python and Node.js installations
2. Show commands for both servers
3. Optionally start the backend server

For complete setup instructions, see [SETUP_COMPLETE.md](SETUP_COMPLETE.md).

---

## 🔌 Backend-Frontend Integration

The application features a complete full-stack integration:

### Architecture
```
React Frontend (Vite + TS)  ←→  FastAPI Backend  ←→  PostgreSQL + Redis
     Port 3003/3004                Port 8000            Aiven Cloud
```

### Key Features
- **REST API Communication**: Frontend calls backend via `/api/*` endpoints
- **Health Monitoring**: `/api/health` for service status
- **Asset Management**: `/api/assets/` for market data
- **Authentication**: JWT-based auth ready (token flow configured)
- **WebSocket Support**: Infrastructure for real-time updates
- **CORS Configured**: Proper cross-origin settings for development

### Verified Endpoints
- ✅ `GET /api/health` - Health check
- ✅ `GET /api/assets/` - Asset data with prices
- ✅ `POST /api/auth/register` - User registration
- ✅ `POST /api/auth/token` - Authentication
- ✅ `POST /api/backtest/` - Backtest execution
- ✅ `GET /api/dashboard/*` - Dashboard metrics

### Technology Stack
**Backend**: FastAPI 0.128.0, SQLAlchemy 2.0.45, Uvicorn 0.40.0, Celery 5.6.2  
**Frontend**: React 18, TypeScript 5.9, Vite 5.4, Tailwind CSS 4.1, Chart.js 4.5  
**Database**: PostgreSQL (Asyncpg), Redis/Valkey  
**Platform**: Python 3.11.6, Node.js 23.3.0

For detailed setup and API documentation, see [SETUP_COMPLETE.md](SETUP_COMPLETE.md).

<!-- ### 4) Optional: Run with mock WS server (dev/demo mode)

We provide a small mock WS generator for local demos. From `cauweb/`:

```bash
# run mock WS generator (node script)
node scripts/mock-ws-server.js --port 9000 --seed 42 --rate 50

# then start cauweb in mock mode (example query param)
npm run dev -- -- --open "http://localhost:3000/?mock=true&ws=http://localhost:9000"
```

The mock server emits `tick`, `heartbeat`, `order_update` events useful for UI development.

--- -->

## Production build & Docker

### Frontend static build

From `cauweb`:

```bash
npm ci
npm run build
# output directory typically `dist/` or `build/`
```
<!-- 
Test serve locally with `serve` or a small Nginx container:

```bash
npm install -g serve
serve -s dist -l 8080
``` -->

<!-- ### Build Docker image (frontend)

*Tip:* `Dockerfile.frontend` should be present. Build and run:

```bash
docker build -f Dockerfile.frontend -t qrs-cauweb:latest .
docker run -p 8080:80 qrs-cauweb:latest
``` -->

<!-- ### Backend production

Use your normal WSGI/ASGI server + env+secrets management. Example (uvicorn + systemd) or containerize with a `Dockerfile.backend`. -->

<!-- ### Full-stack deployment recommendations

* For static frontend hosting: **Vercel** or **Netlify** for quick deploys. Use `vercel.json` or `netlify.toml` for rewrites to the API.
* For containerized deploys: build images for backend and frontend; host in Kubernetes or ECS/Fargate with autoscaling. Use a managed Redis for pub/sub and secure the WS gateway.

--- -->

<!-- ## Realtime contract & WS guide

The frontend expects a stable WS message contract. A suggested minimal schema (example):

```json
{
  "schema_version": "1.0",
  "type": "tick",            # tick | snapshot | order_update | backtest_progress | heartbeat | error
  "topic": "price:AAPL",   # topic or room
  "payload": {
    "timestamp": "2025-11-14T12:34:56.789Z",
    "price": 192.45,
    "volume": 1200
  }
}
``` -->

<!-- Best practices:

* Use topic-based subscriptions: `subscribe(topic)` and `unsubscribe(topic)` so the server publishes minimal data to active clients.
* Include `schema_version` and a short `message_id` for idempotency and replay.
* Implement heartbeat/ping-pong for stale detection. -->

<!-- Where to find client code:

* `src/quant_research_starter/frontend/cauweb/src/lib/wsClient.ts` — typed, reconnecting WS client (if present) -->

<!-- Server responsibilities:

* Translate backend events (backtest updates, order events) into WS messages and publish to Redis pub/sub / message broker.
* Implement room/topic filtering and auth checks on subscribe.

---

## APIs & Data flows: to be updated

* **Backtest flow**: Frontend POSTs to `/api/backtest` with strategy config → backend enqueues job → backend emits progress to `backtest:{job_id}` → final results stored in DB and accessible via `/api/backtest/{job_id}/results`.
* **Strategy CRUD**: REST endpoints for strategy create / update / delete, with validation in Python core.
* **Data adapters**: optional connectors (yfinance, AlphaVantage) are in `src/quant_research_starter/core/data_adapters/`.

> See `src/quant_research_starter/api/README.md` (if present) for detailed endpoint docs.

--- -->

## Testing & CI: to be updated

<!-- ### Python unit tests

```bash
# from repo root
pytest -q
```

### Frontend tests

```bash
cd src/quant_research_starter/frontend/cauweb
npm ci
npm run test        # unit tests
npm run test:e2e    # Playwright / Selenium tests (if configured)
``` -->

<!-- ### Linting & types

```bash
# TS typecheck
npm run typecheck
# ESLint
npm run lint
# Prettier formatting
npm run format
```

CI workflows are in `.github/workflows/` — they typically run linters, unit tests and publish artifacts. -->

---

## Streamlit (legacy) — archived

The Streamlit dashboard is preserved under `legacy/streamlit/` for historical reference. It is **not** the primary UI anymore. If you need to run it:

```bash
cd legacy/streamlit
pip install -r requirements.txt
streamlit run app.py
```

Migration notes:

* Inventory features in `legacy/streamlit/` and decide which are high value to move into `cauweb`.
* Create REST endpoints for functions that were tightly coupled to Streamlit server-side Python handlers.
* Add React counterparts using `LiveChart`, tables and parameter UIs.

---

## Developer workflow & conventions

* **Branches**: `main` for release-ready code; feature branches `feat/...`, hotfixes `fix/...`.
* **Commits**: use Conventional Commits (type(scope): subject), refer: `.github/Contributor_Guide/commiting.md`
* **PRs**: include a description, screenshots, or link tests/lint status. Use the PR template in `.github/PULL_REQUEST_TEMPLATE.md`
* **Type-safety**: keep TS `strict` mode passing; add runtime validation at API boundaries using `zod` or `io-ts`.

<!-- ### Local debugging tips

* Use the mock WS server for UI debugging: `node src/quant_research_starter/frontend/cauweb/scripts/mock-ws-server.js`.
* For backend debugging, run `uvicorn api.main:app --reload` and then call the endpoints from Postman or `curl`. -->

---

## Contributing

1. Fork the repo and create a feature branch.
2. Run tests & linters locally.
3. Open a PR against `main` with a clear description, testing notes, and screenshots.
<!-- 4. If this change introduces schema changes, update `specs/realtime.schema.json` and document migration steps. -->

See `.github/Contributor_Guide/CONTRIBUTING.md` for code-style, review, and release guidance.

---

## Roadmap / recommended next contributions:

Suggested high-value items (already tracked in issues):

* Implement typed WS client in `src/quant_research_starter/frontend/cauweb` (reconnect, subscriptions).
* Migrate high-value Streamlit pages to `cauweb` React components.
* Add Playwright e2e tests for realtime flows with a mocked WS server.
* Implement a paper-trade sandbox UI and backend adapter.

See the Issues board for prioritized tasks and labels like `urgent`, `Type:___`, `Semver:___`.
<!-- 
---

## Troubleshooting

* **`npm run build` fails with TS errors**: run `npm run typecheck` to isolate type issues; ensure correct `NODE_VERSION` and run `npm ci` to use lockfile.
* **CORS / proxy errors**: ensure the frontend dev proxy is configured and backend running on expected host/port; check `.env.local`.
* **WS not connecting**: verify WS URL, check auth token in handshake, and inspect server logs for subscribe rejections.

If you hit an environment-specific issue, add a detailed issue with logs and reproduction steps.

--- -->

## License & contact

This project is licensed under the license in `LICENSE` (check root). For questions, open an issue or contact the maintainers listed in `AUTHORS` / `MAINTAINERS` files.

---
