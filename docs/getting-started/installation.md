# Installation

## Prerequisites

=== "Docker Compose (recommended)"

    - [Docker Engine](https://docs.docker.com/engine/install/) ≥ 24
    - [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.20

=== "From source"

    - GCC ≥ 14 or Clang ≥ 17
    - CMake ≥ 3.25
    - Python ≥ 3.12
    - Node.js ≥ 22 (frontend only)

---

## Get the code

```bash
git clone https://github.com/morgangch/eventd.git
cd eventd
```

---

## Option A — Docker Compose

The fastest path to a running stack:

```bash
docker compose -f deploy/docker/docker-compose.yml up --build
```

| Service | URL |
|---------|-----|
| REST API | http://localhost:8000 |
| Dashboard | http://localhost:3000 |
| MCP server | http://localhost:8100 |

---

## Option B — Build the core from source

```bash
# Configure
cmake -S core -B core/build \
      -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build core/build --parallel

# Run smoke tests
ctest --test-dir core/build --output-on-failure

# Start the engine
./core/build/eventd-core
```

---

## Option C — CLI only

```bash
pip install -e ./cli
eventctl --help
```

---

## Verify the installation

```bash
# Engine starts and prints the banner
./core/build/eventd-core
# expected: "eventd-core starting: internal-monitor-engine"

# API responds
curl http://localhost:8000/status
```
