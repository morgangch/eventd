# Output Layer

## Role

Expose pipeline execution state, matched events, and action results to operators and external systems.

## Backends

| Backend | Status | Description |
|---------|--------|-------------|
| Console (stdout) | **MVP** | Structured, coloured log lines |
| JSON-lines file | **MVP** | Append-only, one JSON object per line |
| REST SSE stream | Phase 2 | `GET /events` server-sent events |
| WebSocket | Phase 2 | Real-time push to the dashboard |
| Prometheus metrics | Phase 2 | `GET /metrics` endpoint |

## Console format (MVP)

```
2026-04-10T15:34:01Z  INFO  [rule:detect-crash-loop]  pid=1234  process=python  action=webhook
```

## JSON-lines format (MVP)

```json
{"ts":"2026-04-10T15:34:01Z","rule":"detect-crash-loop","event":{"pid":1234,"process_name":"python"},"action":{"type":"webhook","status":"sent"}}
```

## Output file configuration

Set `EVENTD_OUTPUT_FILE=/var/log/eventd/events.jsonl` to enable file output.

## REST API (backend)

The Python FastAPI backend bridges the core output to HTTP consumers.  
See the [Backend API](../architecture.md#7-api--backend) section of the architecture doc.
