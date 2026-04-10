<div align="center">

# eventd

**A lightweight, extensible system event engine with a declarative rule DSL.**

Track processes. React to events. Automate responses.

[![CI](https://github.com/morgangch/eventd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/morgangch/eventd/actions/workflows/ci-cd.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-0366d6?logo=readthedocs&logoColor=white)](https://morgangch.github.io/eventd/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![C++17](https://img.shields.io/badge/C%2B%2B-17-blue.svg?logo=cplusplus)](https://isocpp.org/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](deploy/docker/docker-compose.yml)

[Documentation](https://morgangch.github.io/eventd/) · [Architecture](ARCHITECTURE.md) · [Features](FEATURES.md) · [Report a bug](.github/ISSUE_TEMPLATE/bug_report.yml)

</div>

---

## What is eventd?

**eventd** is a native system event engine written in C++. It monitors OS-level events (processes, file I/O, network activity), enriches them with context, evaluates them against a YAML rule DSL, and executes configurable actions — all in a single, low-overhead pipeline.

```
OS events → Collector → Bus → Enrichment (/proc) → Rule Engine → Actions → Output
```

Use it to:
- detect anomalous process behaviour in real time
- automate responses (webhooks, shell commands, service restarts)
- build a custom SIEM pipeline without third-party agents

---

## Highlights

| Feature | Notes |
|---------|-------|
| **Native C++ core** | low-latency event capture and processing |
| **YAML rule DSL** | declare rules in plain text, hot-reloadable (Phase 2) |
| **Enriched events** | automatic `/proc` context on every event |
| **Pluggable actions** | log, webhook, shell, kill — async, non-blocking |
| **REST API** | FastAPI backend; OpenAPI spec included |
| **Web dashboard** | React + Vite operator interface |
| **MCP space** | reserved AI-agent integration layer |
| **Single compose** | full stack in one command |

---

## Quick Start

### Option A — Docker Compose (recommended)

```bash
git clone https://github.com/morgangch/eventd.git
cd eventd
docker compose -f deploy/docker/docker-compose.yml up --build
```

Services:
| Service | Address |
|---------|---------|
| Core engine | (daemon, no port) |
| REST API | http://localhost:8000 |
| Dashboard | http://localhost:3000 |
| MCP server | http://localhost:8100 |

### Option B — Build from source

**Core (C++17):**

```bash
cmake -S core -B core/build -DCMAKE_BUILD_TYPE=Release
cmake --build core/build --parallel
./core/build/eventd-core
```

**CLI:**

```bash
pip install -e ./cli
eventctl --help
```

**Backend:**

```bash
pip install -r web/backend/requirements.txt
uvicorn app.main:app --app-dir web/backend --reload
```

**Frontend:**

```bash
cd web/frontend && npm ci && npm run dev
```

---

## Writing your first rule

Create a YAML rule in `rules/` (feature fully available Phase 2):

```yaml
name: alert-on-crash
condition: "event.type == 'exit' and event.exit_code != 0"
action:
  type: webhook
  params:
    url: "https://hooks.example.com/eventd"
    method: POST
```

Rules are validated against [`proto/rules.schema.json`](proto/rules.schema.json).

---

## Monorepo Structure

```text
eventd/
├── core/                 # C++17 engine — collector, bus, enrichment, rule engine
├── cli/                  # eventctl CLI (Python)
├── web/
│   ├── backend/          # FastAPI REST API
│   └── frontend/         # React + Vite dashboard
├── mcp/                  # MCP server (Phase 3)
├── sdk/                  # Language SDK stubs
├── proto/                # JSON Schema contracts
├── deploy/
│   ├── docker/           # Docker Compose stack
│   ├── systemd/          # Host service units
│   └── k8s/              # Kubernetes (future)
├── docs/                 # MkDocs documentation source
├── tests/                # Integration tests
└── .github/workflows/    # CI/CD pipelines
```

---

## Contributing

1. Fork and clone
2. Create a branch: `git checkout -b feat/your-feature`
3. Open a PR against `main`

Use the [issue templates](.github/ISSUE_TEMPLATE/) for bug reports and feature requests.

---

## License

[MIT](LICENSE) — morgangch
