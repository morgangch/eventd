# eventd

Internal server monitoring platform with a native engine, CLI, web UI, SDKs, and deployment tooling.

## Monorepo Structure

```text
eventd/
├── core/                 # C++ engine
├── cli/                  # eventctl
├── web/                  # API + frontend
├── mcp/                  # Future MCP server space
├── sdk/                  # Language SDK placeholders
├── proto/                # System contracts/schemas
├── deploy/               # Deployment assets (systemd/docker/k8s)
├── docs/                 # Project documentation
├── tests/                # Integration and E2E tests
└── .github/workflows/    # CI/CD pipelines
```

## Quick Start

### Build core

```bash
cmake -S core -B core/build
cmake --build core/build
./core/build/eventd-core
```

### Run CLI

```bash
python -m pip install -e ./cli
eventctl --help
```

### Run backend

```bash
python -m pip install -r web/backend/requirements.txt
uvicorn app.main:app --app-dir web/backend --reload
```

### Run frontend

```bash
cd web/frontend
npm install
npm run dev
```

### Docker compose (dev)

```bash
docker compose -f deploy/docker/docker-compose.yml up --build
```
