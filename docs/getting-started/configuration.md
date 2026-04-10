# Configuration

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EVENTD_LOG_LEVEL` | `info` | Log verbosity (`debug`, `info`, `warning`, `error`) |
| `EVENTD_RULES_DIR` | `rules/` | Directory scanned for YAML rule files |
| `EVENTD_OUTPUT_FILE` | — | Path for JSON-lines output file (disabled if unset) |
| `BACKEND_PORT` | `8000` | FastAPI listening port |
| `MCP_PORT` | `8100` | MCP server listening port |

## Docker Compose overrides

Create `deploy/docker/docker-compose.override.yml` to customize without modifying the main file:

```yaml
services:
  core:
    environment:
      - EVENTD_LOG_LEVEL=debug
```

## Rule files

Rules are loaded from `EVENTD_RULES_DIR` on startup.  
Each file must be valid YAML and pass the [`proto/rules.schema.json`](https://github.com/morgangch/eventd/blob/main/proto/rules.schema.json) contract.

See the [Rule Engine reference](../components/rule-engine.md) for full DSL documentation.
