# eventd Architecture (Bootstrap)

## Layers

- `core/`: native event processing engine (C++).
- `cli/`: operator commands (`eventctl`) for local and remote control.
- `web/backend/`: API and orchestration endpoints.
- `web/frontend/`: operator dashboard.
- `mcp/`: reserved MCP integration server.

## Contracts

JSON schemas in `proto/` define event and rule contracts across components.

## Deployment

- `deploy/systemd/`: host service units.
- `deploy/docker/`: compose stack for local integration.
- `deploy/k8s/`: future cluster packaging.
