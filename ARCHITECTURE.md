# eventd — Architecture

> Build a high-performance system event engine with an end-to-end pipeline:
>
> **OS → Events → Bus → Enrichment → Rule Engine → Actions → Output**

## Table of Contents

- [Global View](#global-view)
- [Runtime Flow](#runtime-flow)
- [Monorepo Layout](#monorepo-layout)
- [1. Event Collector](#1-event-collector)
- [2. Event Bus](#2-event-bus)
- [3. Enrichment Layer](#3-enrichment-layer)
- [4. Rule Engine](#4-rule-engine)
- [5. Action Executor](#5-action-executor)
- [6. Output Layer](#6-output-layer)
- [7. API / Backend](#7-api--backend)
- [8. Frontend Dashboard](#8-frontend-dashboard)
- [9. MCP Server](#9-mcp-server)
- [Technical Choices](#technical-choices)
- [Contracts (proto/)](#contracts-proto)
- [Delivery Strategy](#delivery-strategy)

---

## Objective

Build a system event engine with this end-to-end flow:

**OS → Events → Pipeline → Rules → Actions → Output (logs/webhooks/UI)**

## Global View

```
┌──────────────────────────────────────────────────────┐
│                    eventd pipeline                   │
│                                                      │
│  ┌─────────────┐     ┌─────────────┐                 │
│  │  Collector  │────▶│  Event Bus  │                 │
│  │  (C++ core) │     │ (async q.)  │                 │
│  └─────────────┘     └──────┬──────┘                 │
│   eBPF / /proc /             │                       │
│   pipes / journald           ▼                       │
│                       ┌─────────────┐                │
│                       │ Enrichment  │  /proc cache   │
│                       └──────┬──────┘                │
│                              │                       │
│                              ▼                       │
│                       ┌─────────────┐                │
│                       │ Rule Engine │  YAML DSL      │
│                       └──────┬──────┘                │
│                              │                       │
│                              ▼                       │
│                       ┌─────────────┐                │
│                       │   Action    │                │
│                       │  Executor   │                │
│                       └──────┬──────┘                │
│                              │                       │
│              ┌───────────────┼──────────────┐        │
│              ▼               ▼              ▼        │
│         [Console]        [JSON/file]    [Webhook]    │
│              │               │              │        │
│              └───────────────┴──────────────┘        │
│                              │                       │
│                              ▼                       │
│                    ┌──────────────────┐              │
│                    │  REST API / MCP  │              │
│                    └────────┬─────────┘              │
│                             ▼                        │
│                     ┌──────────────┐                 │
│                     │  Web Dashboard│                │
│                     └──────────────┘                 │
└──────────────────────────────────────────────────────┘
```

## Runtime Flow

```
Event → Bus → Enrichment → Rule Engine → Action → Output → API → Dashboard
```

---

## Monorepo Layout

| Path | Role |
|------|------|
| `core/` | Native event engine (C++17, CMake) |
| `cli/` | `eventctl` operator CLI (Python) |
| `web/backend/` | REST API and orchestration (FastAPI) |
| `web/frontend/` | Operator dashboard (React + Vite) |
| `mcp/` | Reserved MCP server integration space |
| `sdk/` | Language SDK stubs |
| `proto/` | JSON Schema contracts shared across components |
| `deploy/docker/` | Docker Compose stack |
| `deploy/systemd/` | Host service units (production) |
| `deploy/k8s/` | Kubernetes packaging (future) |
| `docs/` | Full project documentation (MkDocs) |
| `.github/workflows/` | CI/CD pipelines |

---

## 1. Event Collector

**Role:** Capture system events in real time and push them onto the event bus.

### Sources

| Source | Status | Notes |
|--------|--------|-------|
| subprocess + stdout/stderr | MVP | start here |
| `/proc` polling | MVP | metadata enrichment |
| journald | Phase 2 | systemd integration |
| eBPF | Phase 3 | kernel-level capture, lowest overhead |

### C++ Interface

```cpp
struct Event {
    std::string id;                              // UUID
    std::string type;                            // exec, stdout, stderr, net…
    int         pid;
    int         ppid;
    std::string data;                            // log line, args, syscall…
    std::chrono::system_clock::time_point ts;
};
```

### MVP Scope

- spawn and monitor a subprocess
- capture its `stdout` / `stderr` line by line
- publish each line as an `Event` onto the bus

---

## 2. Event Bus

**Role:** Decouple all pipeline stages. Every component communicates only through the bus.

### Interface

```cpp
class EventBus {
public:
    void publish(const Event& e);
    void subscribe(std::function<void(const Event&)> handler);
};
```

### Implementation

- thread-safe queue: `std::queue<Event>` protected by `std::mutex` + `std::condition_variable`
- model: 1 producer thread (collector), N consumer threads (enrichment, rule engine…)
- backpressure strategy: bounded queue with configurable max capacity (Phase 2)

---

## 3. Enrichment Layer

**Role:** Transform raw events into rich, actionable records by attaching process and container context.

### Enriched Event Schema

```json
{
  "id":           "uuid-v4",
  "type":         "stdout",
  "pid":          1234,
  "ppid":         1,
  "process_name": "python",
  "parent_name":  "systemd",
  "exe":          "/usr/bin/python3",
  "args":         ["server.py"],
  "container":    "docker",
  "cgroup":       "/docker/abc123",
  "timestamp":    1712759673
}
```

### Implementation

- read metadata from `/proc/<pid>/status`, `/proc/<pid>/cmdline`, `/proc/<pid>/exe`
- LRU cache per PID to limit `/proc` reads (TTL: 500 ms)
- container detection: inspect cgroup path for `docker/` or `containerd/`

---

## 4. Rule Engine

**Role:** Evaluate declarative YAML rules at runtime and trigger actions when conditions match.

### Rule DSL (YAML)

```yaml
name: detect-crash-loop
condition: "event.type == 'exit' and event.exit_code != 0"
action:
  type: webhook
  params:
    url: "https://hooks.example.com/alert"
    method: POST
```

### Internal Structure

```cpp
struct Condition { std::string expression; };
struct Action    { std::string type; std::map<std::string, std::string> params; };

class Rule {
public:
    std::string name;
    Condition   condition;
    Action      action;

    bool matches(const Event& event) const;
};
```

### Parsing

Library: [`yaml-cpp`](https://github.com/jbeder/yaml-cpp)

### Runtime Logic

```cpp
for (const auto& rule : loaded_rules) {
    if (rule.matches(enriched_event)) {
        executor.execute(rule.action, enriched_event);
    }
}
```

### Design Constraints

- strict separation between YAML parsing and runtime evaluation
- rules hot-reloadable at runtime (Phase 2): watch `rules/*.yml` with `inotify`
- condition language: start with simple field equality / regexp, evolve toward expression parser

### Contract

Rules are validated against `proto/rules.schema.json` before loading.

---

## 5. Action Executor

**Role:** Execute the action triggered by a matched rule, without blocking the pipeline.

### Action Types

| Type | Description | Status |
|------|-------------|--------|
| `log` | Write structured log entry | MVP |
| `webhook` | HTTP POST to external URL | MVP |
| `shell` | Run arbitrary shell command | MVP |
| `kill` | Send signal to process | Phase 2 |
| `restart` | Restart a systemd service | Phase 2 |

### Interface

```cpp
class ActionExecutor {
public:
    void execute(const Action& action, const Event& event);
};
```

### Constraint

All actions run on a dedicated thread pool — never on the bus thread — to avoid back-pressure on the pipeline.

---

## 6. Output Layer

**Role:** Expose pipeline execution state and matched events to operators.

### MVP

- console: structured, colored log lines via `stdout`
- file: append-only JSON-lines file at a configurable path

### Future

- REST streaming endpoint (SSE or WebSocket)
- time-series metrics (Prometheus-compatible)
- web dashboard integration

---

## 7. API / Backend

**Role:** HTTP bridge between the core engine and external consumers (dashboard, CLI, MCP).

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/events` | GET | Stream recent events (SSE) |
| `/rules` | GET/POST | List and create rules at runtime |
| `/status` | GET | Engine health and counters |

**Stack:** Python 3.12 + FastAPI + uvicorn  
**Location:** `web/backend/`

---

## 8. Frontend Dashboard

**Role:** Operator-facing web interface for real-time monitoring and rule management.

- live event feed (WebSocket / SSE)
- rule editor with YAML syntax highlighting
- process tree visualization

**Stack:** React + Vite + TypeScript  
**Location:** `web/frontend/`

---

## 9. MCP Server

**Role:** Reserved integration space for the [Model Context Protocol](https://modelcontextprotocol.io/) — exposes eventd context to AI agents and assistants.

**Location:** `mcp/`  
**Status:** placeholder, Phase 3

---

## Technical Choices

### Languages

| Layer | Language | Rationale |
|-------|----------|-----------|
| Core engine | C++17 | performance, direct OS access |
| CLI | Python 3.12 | rapid iteration, rich ecosystem |
| API backend | Python 3.12 + FastAPI | async, typed, OpenAPI out of the box |
| Dashboard | TypeScript + React | component model, strong typing |

### C++ Libraries

| Library | Use |
|---------|-----|
| [`yaml-cpp`](https://github.com/jbeder/yaml-cpp) | YAML rule parsing |
| [`nlohmann/json`](https://github.com/nlohmann/json) | JSON serialisation |
| [`cpr`](https://github.com/libcpr/cpr) / `libcurl` | HTTP webhooks |
| `std::thread` + `std::mutex` | thread-safe bus |

---

## Contracts (`proto/`)

All cross-component schemas are defined as [JSON Schema 2020-12](https://json-schema.org/) in `proto/`.

| File | Describes |
|------|-----------|
| `proto/events.schema.json` | Event wire format (id, type, timestamp, source, payload) |
| `proto/rules.schema.json` | Rule definition (name, condition expression, action type + params) |

Every component that reads or writes events/rules validates against these schemas.

---

## Delivery Strategy

### Phase 1 — MVP

- [x] Monorepo scaffold (core, cli, web, mcp, proto, deploy)
- [ ] Subprocess collector publishing to in-memory bus
- [ ] Basic `/proc` enrichment
- [ ] YAML rule parsing + simple condition matching
- [ ] Async action execution (log + webhook)
- [ ] Console + JSON file output
- [ ] CLI (`eventctl`) connecting to the API

### Phase 2 — Feature complete

- [ ] journald collector
- [ ] Richer condition language (regex, arithmetic)
- [ ] Rule hot-reload via `inotify`
- [ ] Webhook retries with exponential back-off
- [ ] REST API + first dashboard views
- [ ] Prometheus metrics endpoint

### Phase 3 — Advanced

- [ ] eBPF collector (Linux 5.8+, CO-RE)
- [ ] Behaviour scoring and anomaly detection
- [ ] SIEM-style timeline and correlation
- [ ] MCP server integration
- [ ] Kubernetes operator
