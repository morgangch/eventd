# Contributing

We welcome contributions of all kinds — code, documentation, bug reports, and ideas.

## Development setup

```bash
git clone https://github.com/morgangch/eventd.git
cd eventd

# Start the full stack
docker compose -f deploy/docker/docker-compose.yml up --build
```

## Branch conventions

| Branch | Purpose |
|--------|---------|
| `main` | Always releasable |

| `feat/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation changes |
| `chore/<name>` | Tooling, CI, deps |

## Submitting changes

1. Fork the repository
2. Create a branch from `main`
3. Make your changes and ensure CI passes locally
4. Open a pull request with a clear description

## Reporting issues

Use the GitHub issue templates:

- [Bug report](https://github.com/morgangch/eventd/issues/new?template=bug_report.yml)
- [Feature request](https://github.com/morgangch/eventd/issues/new?template=feature_request.yml)
- [Documentation issue](https://github.com/morgangch/eventd/issues/new?template=docs.yml)

## Code style

| Language | Formatter / Linter |
|----------|-------------------|
| C++ | `clang-format` (`.clang-format` at root, LLVM style) |
| Python | `ruff` |
| TypeScript | `eslint` + `prettier` |

## Running tests locally

```bash
# C++ unit tests
cmake --build core/build --parallel
ctest --test-dir core/build --output-on-failure

# Python lint
pip install ruff
ruff check cli/ web/backend/ mcp/

# Frontend build
cd web/frontend && npm ci && npm run build
```
