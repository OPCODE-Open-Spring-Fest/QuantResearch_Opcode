frontend/
│
├── core/                          # Shared logic library
│   ├── src/
│   │   ├── components/            # Shared React components
│   │   ├── hooks/                 # Shared React hooks (fetch, state mgmt)
│   │   ├── utils/                 # Reusable helper functions
│   │   ├── types/                 # Shared TypeScript types
│   │   └── index.ts               # Export all shared modules
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md

│
├── cauweb/                        # Main Web UI App
│   ├── src/
│   │   ├── pages/                 # UI Screens (Home, Dashboard, About)
│   │   ├── layouts/               # Shared layouts (Navbar, Sidebar)
│   │   ├── features/              # Domain features (Logs, Trading UI)
│   │   ├── assets/                # Images, icons, fonts
│   │   ├── styles/                # Global CSS/Tailwind configs
│   │   └── main.tsx               # App entry point
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md

│
├── cli/                           # Terminal UI (Node/React Ink CLI)
│   ├── src/
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json

│
├── metrics/                       # Data visual charts + API metrics
│   ├── src/
│   │   ├── charts/
│   │   ├── analytics/
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json

│
├── node_modules/                  # Shared dependencies root install
│
├── package.json                   # root scripts + global deps
├── pnpm-workspace.yaml            # defines workspace packages
├── tsconfig.base.json             # shared TS config
└── README.md
